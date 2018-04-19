from __future__ import print_function

import time

import docker


class DCCDocker():
    def __init__(self, container, input, output):
        self.client = docker.from_env()
        self.CONTAINER_NAME = container  # "ilent2/dicom2cloud"
        self.INPUT_TARGET = input  # "/home/neuro/"
        self.OUTPUT_TARGET = output  # "/home/neuro/" + self.OUTPUT_FILENAME

    def startDocker(self, dataSet):
        print('Running docker dummy:', dataSet)
        timeout = time.time() + 60 * .1
        return ('c1', timeout)

    def checkIfDone(self, container, timeout):
        timer = time.time()
        print(timer)
        if timer >= timeout:
            return True
        else:
            return False

    def getStatus(self, container):
        return 1

    def finalizeJob(self, container, outputDir):
        return 1

############################################################################################
if __name__ == '__main__':
    containername = "ilent2/dicom2cloud"
    input = "/home/neuro/"
    output = "/home/neuro/output.mnc"
    dcc = DCCDocker(containername, input, output)
    (c, timeout) = dcc.startDocker('test')
    print(c)
    while (not dcc.checkIfDone(c, timeout)):
        print("running")
    print("finished")
