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

import docker


class DCCDocker():
    def __init__(self, containername, input, output):
        self.client = docker.from_env()
        self.CONTAINER_NAME = containername  # "ilent2/dicom2cloud"
        self.INPUT_TARGET = input  # "/home/neuro/"
        self.OUTPUT_TARGET = output  # "/home/neuro/" + self.OUTPUT_FILENAME

    def startDocker(self, tarfile):
        """ Start a new docker instance and copy the data into the container.

        @param tarfile      The input DICOM files in a tarfile
        @return container   Reference to the created docker container.
        """

        # Check for updates to the docker image
        try:
            self.client.images.pull(self.CONTAINER_NAME)
            container = self.client.api.create_container(self.CONTAINER_NAME)
            self.client.api.put_archive(container, self.INPUT_TARGET, tarfile)
            self.client.api.start(container)
        except Exception as e:
            print(e.args[0])


        return container

    def waitUntilDone(self, container):
        """ Blocks until the docker container has processed the files.

        @param container    The container object returned by startDocker.
        @return jobStatus   Returns 0 if docker ran successfully.
        """

        return self.client.api.wait(container)

    def checkIfDone(self, container, timeout):
        """ Checks if the docker has processed the files (non-blocking).
        To get the jobStatus you will need to call get status.

        @param container    The container object returned by startDocker.
        @return done        Returns True if stopped, False if running.
        """

        inspect = self.client.api.inspect_container(container['Id'])
        return inspect['State']['Running'] == False

    def getStatus(self, container):
        """ Get the status of the docker job.

        @param container    The container object returned by startDocker.
        @return jobStatus   Returns 0 if docker ran successfully.
        """

        if not self.checkIfDone(container):
            raise Exception("Container not stopped.")

        inspect = self.client.api.inspect_container(container['Id'])
        return inspect['State']['ExitCode']

    def finalizeJob(self, container, outputDir):
        """ Copy data out of docker and free resources.

        @param container    The container object returned by startDocker.
        @param outputDir    Directory name for the output MINC file.
        @return None
        """

        with tempfile.NamedTemporaryFile() as tmpfile:
            strm, stat = self.client.api.get_archive(container, self.OUTPUT_TARGET)

            for d in strm:
                tmpfile.write(d)
            tmpfile.seek(0)

            tar = tarfile.open(fileobj=tmpfile)
            tar.extractall(path=outputDir)
            tar.close()


if __name__ == '__main__':
    import time
    from os.path import dirname
    CONTAINER_NAME = "ilent2/dicom2cloud"
    INPUT_TARGET = "/home/neuro/"
    OUTPUT_TARGET = "/home/neuro/output.mnc"
    inputdir = 'D:\\Data\\mridata\\exampleData\\output'
    tarfile = "ba3ef915bd7b885f3fffa433743451d1afa7d772027398353fd3f734f248d46f.tar"

    dcc = DCCDocker(CONTAINER_NAME,INPUT_TARGET,OUTPUT_TARGET)
    (container, timeout) = dcc.startDocker(tarfile)
    if container is None:
        raise Exception("Unable to initialize Docker")
    ctr = 0
    while (not dcc.checkIfDone(container, timeout)):
        time.sleep(1)
        print('Converting: ', ctr)
        ctr += 10

    # Check that everything ran ok
    if not dcc.getStatus(container):
        print("There was an error while anonomizing the dataset.")

    # Get the resulting mnc file back to the original directory
    dcc.finalizeJob(container, dirname(tarfile))