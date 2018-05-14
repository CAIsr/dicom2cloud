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
from __future__ import print_function
import tarfile
import tempfile
from dicom2cloud.config.dbquery import DBI
import docker
from io import BytesIO
from os.path import join


class DCCDocker():
    def __init__(self, process=None):
        self.client = docker.from_env()
        db = DBI()
        db.connect()
        #DEFAULTS
        self.CONTAINER_NAME = db.getServerConfigByName('DOCKER_CONTAINER')
        self.INPUT_TARGET = db.getServerConfigByName('DOCKER_INPUTDIR')
        self.OUTPUT_TARGET = db.getServerConfigByName('DOCKER_OUTPUTDIR')
        self.OUTPUT = db.getServerConfigByName('DOCKER_OUTPUTFILE')
        #Load specific process configs if set
        self.process = process
        if process is not None:
            container = db.getServerConfigByName(db.getProcessField('container',process))
            if container is not None:
                self.CONTAINER_NAME = container

            input = db.getServerConfigByName(db.getProcessField('containerinputdir',process))
            if input is not None:
                self.INPUT_TARGET = input
            outputd = db.getServerConfigByName(db.getProcessField('containeroutputdir',process))
            if outputd is not None:
                self.OUTPUT_TARGET = outputd

            ofile = db.getServerConfigByName(db.getProcessField('filename',process))
            if ofile is not None:
                self.OUTPUT = ofile


        db.closeconn()


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
        rtn = False
        inspect = self.client.api.diff(containerId)
        #looking for file: output.mnc
        for p in inspect:
            if self.OUTPUT in p['Path']:
                print(p['Path'])
                rtn = True
        return rtn
        # inspect = self.client.api.inspect_container(containerId)
        # return inspect['State']['Running'] == False

    def getExitStatus(self, containerId):
        """ Get the status of the docker job.

        @param container    The container object returned by startDocker.
        @return jobStatus   Returns 0 if docker ran successfully.
        """
        #TODO - GET TIME inspect['State']['StartedAt'] - inspect['State']['FinishedAt']

        inspect = self.client.api.inspect_container(containerId)
        return inspect['State']['ExitCode']

    def finalizeJob(self, containerId, outputDir,uuid,outputasfile):
        """ Copy data out of docker and free resources.

        @param container    The container object returned by startDocker.
        @param outputDir    Directory name for the output MINC file.
        @return outputfile name
        """
        #stat {u'linkTarget': u'', u'mode': 2147484096L, u'mtime': u'2018-04-20T06:10:52.56896119Z', u'name': u'neuro', u'size': 20480}
        #testoutput = '00001_tfl3d1_ns_C_A32.IMA'
        # can copy whole directory or just output file
        if outputasfile:
            outputfile = join(self.OUTPUT_TARGET,self.OUTPUT)
        else:
            outputfile = self.OUTPUT_TARGET
        datastream, stat = self.client.api.get_archive(containerId, outputfile)
        print('File retrieved from Docker: ', stat)
        f = BytesIO(datastream.data)
        outfile=join(outputDir,uuid + '.tar')
        with open(outfile, 'wb') as out:
            out.write(f.read())
        f.close()
        print('Tarfile written to: ', outfile)
        # # Tar DICOM files to load to container for processing
        procdir = 'processed'
        if self.process is not None:
            procdir += "_" + self.process
        tarfiledir = join(outputDir,uuid,procdir)
        with tarfile.open(outfile, "r") as tar:
            tar.extractall(path=tarfiledir)
        tar.close()
        print('Output written to: ', tarfiledir)
        return tarfiledir



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

    # Check that everything ran ok - returns O if success
    if dcc.getExitStatus(containerId):
        print("There was an error while anonomizing the dataset.")

    # Get the resulting mnc file back to the original directory
    dcc.finalizeJob(containerId, inputdir, uuid,1)