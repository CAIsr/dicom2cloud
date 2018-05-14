from __future__ import print_function

import time
import docker
from os.path import join
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
        self.timeout = time.time() + 60 * .1
        return 'c1'

    def checkIfDone(self, container):
        timer = time.time()
        print(timer)
        return timer >= self.timeout

    def getExitStatus(self, container):
        return 0

    def finalizeJob(self, container, outputDir, uuid,outputasfile):
        print('Test docker: finalized')
        return join(outputDir,uuid)


############################################################################################
if __name__ == '__main__':

    dcc = DCCDocker()
    (c, timeout) = dcc.startDocker('test')
    print(c)
    while (not dcc.checkIfDone(c, timeout)):
        print("running")
    print("finished")
