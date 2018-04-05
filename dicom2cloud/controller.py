import logging
import threading
import time
import shutil
from glob import iglob
from logging.handlers import RotatingFileHandler
from multiprocessing import freeze_support, Pool
from os import access, R_OK, mkdir
from os.path import join, dirname, exists, split, splitext, expanduser
from config.dbquery import DBI
from dicom2cloud.processmodules.runDocker import startDocker, checkIfDone, getStatus, finalizeJob
from dicom2cloud.processmodules.uploadScripts import get_class
import wx

import importlib



# Required for dist
freeze_support()
########################################################################
# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()
EVT_DATA_ID = wx.NewId()

logger = logging.getLogger()
lock = threading.Lock()
event = threading.Event()
hevent = threading.Event()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


def EVT_DATA(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_DATA_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class DataEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_DATA_ID)
        self.data = data

############################################################################
class DockerThread(threading.Thread):
    """Multi Worker Thread Class."""

    # ----------------------------------------------------------------------
    def __init__(self, wxObject, targetdir, seriesid, processname, server):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject
        self.processname = processname
        self.targetdir = targetdir
        self.seriesid = seriesid
        self.server = server

    # ----------------------------------------------------------------------
    def run(self):
        i = 0
        try:
            # event.set()
            # lock.acquire(True)
            # Do work
            container = startDocker(self.targetdir)
            ctr = 0
            print "Started"
            while (not checkIfDone(container)):
                time.sleep(5)
                wx.PostEvent(self.wxObject, ResultEvent((ctr, self.seriesid, self.processname)))
                ctr = 1

            # Check that everything ran ok
            if getStatus(container) != 0:
                raise Exception("There was an error while anonomizing the dataset.")

            # Get the resulting mnc file back to the original directory
            finalizeJob(container, self.targetdir)

            # Upload MNC to server
            mncfile = join(self.targetdir, 'output.mnc')
            uploadfile = join(self.targetdir, self.seriesid + '.mnc')
            if access(mncfile, R_OK):
                shutil.copyfile(mncfile, uploadfile)
                uploaderClass = get_class(self.server)
                uploader = uploaderClass(self.seriesid)
                uploader.upload(uploadfile, self.processname)
                wx.PostEvent(self.wxObject, ResultEvent((2, self.seriesid, self.processname)))
                print "Uploaded file: %s to %s" % (uploadfile, self.server)
            print "Finished DockerThread"

        except Exception as e:
            wx.PostEvent(self.wxObject, ResultEvent((-1, self.seriesid, self.processname)))

        finally:
            wx.PostEvent(self.wxObject, ResultEvent((10, self.seriesid, self.processname)))
            # logger.info('Finished FilterThread')
            # self.terminate()
            # lock.release()
            # event.clear()

################################################################################################
class Controller():
    def __init__(self):
        self.logger = self.loadLogger()
        self.db = DBI()
        if self.db.c is None:
            self.db.getconn()
        self.cmodules = self.loadProcesses()

    def loadProcesses(self):
        pf = None
        try:
            self.processes = self.db.getCaptions()
            cmodules={}
            for p in self.processes:
                msg = "Controller:LoadProcessors: loading %s" % p
                print(msg)
                # TODO Dynamic loading
                module_name = self.db.getProcessModule() #self.processes[p]['modulename']
                class_name = self.db.getProcessClass() #self.processes[p]['classname']
                cmodules[p] =(module_name,class_name)
            return cmodules
        except Exception as e:
            raise e
        finally:
            if pf is not None:
                pf.close()

    def loadLogger(self,outputdir=None, expt=''):
        #### LoggingConfig
        logger.setLevel(logging.INFO)
        homedir = expanduser("~")
        if outputdir is not None and access(outputdir, R_OK):
            homedir = outputdir
        if len(expt) >0:
            expt = expt + "_"
        if not access(join(homedir, "logs"), R_OK):
            mkdir(join(homedir, "logs"))
        self.logfile = join(homedir, "logs", expt+'analysis.log')
        handler = RotatingFileHandler(filename=self.logfile, maxBytes=10000000, backupCount=10)
        formatter = logging.Formatter('[ %(asctime)s %(levelname)-4s ] %(filename)s %(lineno)d : (%(threadName)-9s) %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger