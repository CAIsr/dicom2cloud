from __future__ import print_function

import time

import docker
from dicom2cloud.config.dbquery import DBI


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

    dcc = DCCDocker()
    (c, timeout) = dcc.startDocker('test')
    print(c)
    while (not dcc.checkIfDone(c, timeout)):
        print("running")
    print("finished")
