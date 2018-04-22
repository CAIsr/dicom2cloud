#!/usr/bin/python
#
# runDocker.py - Functions to run and interact with the docker container.
#
# Copyright 2017 Dicom2cloud Team
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import tarfile
import tempfile
from dicom2cloud.config.dbquery import DBI
import docker


class DCCDocker():
    def __init__(self):
        self.client = docker.from_env()
        db = DBI()
        db.connect()
        self.CONTAINER_NAME = db.getServerConfigByName('DOCKER_CONTAINER')
        self.INPUT_TARGET = db.getServerConfigByName('DOCKER_INPUTDIR')
        self.OUTPUT_TARGET = db.getServerConfigByName('DOCKER_OUTPUTDIR')
        self.OUTPUT = db.getServerConfigByName('DOCKER_OUTPUTFILE')

        db.closeconn()
        # self.CONTAINER_NAME = containername  # "ilent2/dicom2cloud"
        # self.INPUT_TARGET = input  # "/home/neuro/"
        # self.OUTPUT_TARGET = output  # "/home/neuro/" + self.OUTPUT_FILENAME

    def startDocker(self, dataset):
        """ Start a new docker instance and copy the data into the container.

        @param dataset      The input DICOM files in a directory
        @return container   Reference to the created docker container.
        """

        # Check for updates to the docker image
        containerId = None
        try:
            print('Starting docker')
            self.client.images.pull(self.CONTAINER_NAME)
            container = self.client.api.create_container(self.CONTAINER_NAME)
            if container is not None:
                containerId = container['Id']
                print('created container:', containerId)
                with docker.utils.tar(dataset) as tar:
                    rtn = self.client.api.put_archive(containerId, self.INPUT_TARGET, tar)
                #self.client.api.put_archive(container, self.INPUT_TARGET, tarfile)
                print('loaded archive')
                self.client.api.start(containerId)
                print('container is running')
            else:
                raise Exception("Container not created")
        except Exception as e:
            print(e)

        return containerId

    def waitUntilDone(self, containerId):
        """ Blocks until the docker container has processed the files.

        @param container    The container object returned by startDocker.
        @return jobStatus   Returns 0 if docker ran successfully.
        """

        return self.client.api.wait(containerId)

    def checkIfDone(self, containerId):
        """ Checks if the docker has processed the files (non-blocking).
        To get the jobStatus you will need to call get status.

        @param container    The container object returned by startDocker.
        @return done        Returns True if stopped, False if running.
        """

        inspect = self.client.api.inspect_container(containerId)
        return inspect['State']['Running'] == False

    def getStatus(self, containerId):
        """ Get the status of the docker job.

        @param container    The container object returned by startDocker.
        @return jobStatus   Returns 0 if docker ran successfully.
        """
        #TODO - GET TIME inspect['State']['StartedAt'] - inspect['State']['FinishedAt']

        if not self.checkIfDone(containerId):
            raise Exception("Container not stopped.")

        inspect = self.client.api.inspect_container(containerId)
        return inspect['State']['ExitCode']

    def finalizeJob(self, containerId, outputDir):
        """ Copy data out of docker and free resources.

        @param container    The container object returned by startDocker.
        @param outputDir    Directory name for the output MINC file.
        @return None
        """
        #stat {u'linkTarget': u'', u'mode': 2147484096L, u'mtime': u'2018-04-20T06:10:52.56896119Z', u'name': u'neuro', u'size': 20480}
        #TODO Replace with a direct copy - otherwise fills up disk
        with tempfile.SpooledTemporaryFile() as tmpfile:
            strm, stat = self.client.api.get_archive(containerId, self.OUTPUT_TARGET)

            for d in strm:
                tmpfile.write(d)
            tmpfile.seek(0)

            tar = tarfile.open(fileobj=tmpfile)
            tar.extractall(path=outputDir)
            tar.close()


if __name__ == '__main__':
    import time
    from os.path import dirname,join

    inputdir = 'D:\\Data\\mridata\\exampleData\\output'
    uuid ='ba3ef915bd7b885f3fffa433743451d1afa7d772027398353fd3f734f248d46f'
    #tarfile = "ba3ef915bd7b885f3fffa433743451d1afa7d772027398353fd3f734f248d46f.tar"

    dcc = DCCDocker()
    containerId = dcc.startDocker(join(inputdir,uuid))
    if containerId is None:
        raise Exception("Unable to initialize Docker")
    ctr = 0
    while (not dcc.checkIfDone(containerId)):
        time.sleep(5)
        print('Converting: ', ctr)
        ctr += 5

    # Check that everything ran ok
    if not dcc.getStatus(containerId):
        print("There was an error while anonomizing the dataset.")

    # Get the resulting mnc file back to the original directory
    dcc.finalizeJob(containerId, inputdir)