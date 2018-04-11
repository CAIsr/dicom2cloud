from __future__ import print_function
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
import datetime
from dicom2cloud.processmodules.testDocker import DCCDocker
#from dicom2cloud.processmodules.runDocker import startDocker, checkIfDone, getStatus, finalizeJob
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
class ProcessThread(threading.Thread):
    """Multi Worker Thread Class."""
   # wxGui, processname, self.cmodules[processref], targetdir, uuid, server, filenames, row, containername
    # ----------------------------------------------------------------------
    def __init__(self, wxObject, processname, module_name, class_name, mountdir,inputdir, uuid, output,server,row, containername):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject
        self.processname = processname
        self.targetdir = join(inputdir, uuid)       #dir containing dicom files to be processed
        self.uuid = uuid
        self.outputfile = output                   #full filename of mnc output file
        self.containername = containername          #docker image name
        #self.filenames = filenames
        self.server = server
        self.row = row
        # Dynamic process module
        self.module_name = module_name
        self.class_name = class_name
        # Instantiate module
        module = importlib.import_module(self.module_name)
        class_ = getattr(module, self.class_name)
        self.dcc = class_(self.containername, mountdir, output)

    # ----------------------------------------------------------------------
    def run(self):
        print('Starting thread run')
        try:
            event.set()
            lock.acquire(True)
            (container, timeout) = self.dcc.startDocker(self.targetdir)
            ctr = 0
            while (not self.dcc.checkIfDone(container, timeout)):
                time.sleep(1)
                wx.PostEvent(self.wxObject, ResultEvent((self.row,ctr, self.uuid, self.processname, 'Converting')))
                ctr += 10

            # Check that everything ran ok
            if not self.dcc.getStatus(container):
                raise Exception("There was an error while anonomizing the dataset.")

            # Get the resulting mnc file back to the original directory
            self.dcc.finalizeJob(container, self.targetdir)

            # Upload MNC to server
            mncfile = join(self.targetdir, self.outputfile)
            uploadfile = join(self.targetdir, self.uuid + '.mnc')
            if access(mncfile, R_OK):
                shutil.copyfile(mncfile, uploadfile)
                uploaderClass = get_class(self.server)
                uploader = uploaderClass(self.uuid)
                uploader.upload(uploadfile, self.processname)
                wx.PostEvent(self.wxObject, ResultEvent((self.row, ctr,self.uuid, self.processname, 'Uploading')))
                msg ="Uploaded file: %s to %s" % (uploadfile, self.server)
                print(msg)
            print("Finished ProcessThread")

        except Exception as e:
            print("ERROR:", e.args[0])
            wx.PostEvent(self.wxObject, ResultEvent((self.row, -1, self.uuid, self.processname,e.args[0])))

        finally:
            wx.PostEvent(self.wxObject, ResultEvent((self.row,100, self.uuid, self.processname,'Done')))
            logger.info('Finished ProcessThread')
            # self.terminate()
            lock.release()
            event.clear()

################################################################################################
class Controller():
    def __init__(self):
        self.logger = self.__loadLogger()
        self.db = DBI()
        if self.db.c is None:
            self.db.connect()
        self.cmodules = self.__loadProcesses()

    def __loadProcesses(self):
        pf = None
        try:
            self.processes = self.db.getRefs()
            cmodules={}
            for p in self.processes:
                msg = "Controller:LoadProcessors: loading %s" % self.db.getCaption(p)
                print(msg)
                # Dynamic loading
                module_name = self.db.getProcessModule(p) #self.processes[p]['modulename']
                class_name = self.db.getProcessClass(p) #self.processes[p]['classname']
                cmodules[p] =(module_name,class_name)
            return cmodules
        except Exception as e:
            raise e
        finally:
            if pf is not None:
                pf.close()

    def __loadLogger(self,outputdir=None):
        #### LoggingConfig
        logger.setLevel(logging.INFO)
        homedir = expanduser("~")
        if outputdir is not None and access(outputdir, R_OK):
            homedir = outputdir
        if not access(join(homedir, "logs"), R_OK):
            mkdir(join(homedir, "logs"))
        self.logfile = join(homedir, "logs", 'd2c.log')
        handler = RotatingFileHandler(filename=self.logfile, maxBytes=10000000, backupCount=10)
        formatter = logging.Formatter('[ %(asctime)s %(levelname)-4s ] %(filename)s %(lineno)d : (%(threadName)-9s) %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    # ----------------------------------------------------------------------
    def RunProcess(self, wxGui, inputdir, uuid, processname, server, row):
        """
        Run processing in a thread
        :param wxGui: Process Panel ref
        :param inputdir: Directory with DICOM files
        :param uuid: unique ID from series number
        :param processname: Process eg QSM
        :param server: Cloud server to use eg AWS
        :param row: Row number in progress table in Process Panel
        :return:
        """
        # Get info from database
        processref = self.db.getRef(processname)
        containername = self.db.getProcessField('container',processname)
        mountdir = self.db.getProcessField('containerinputdir',processname)
        output = join(self.db.getProcessField('containeroutputdir',processname),self.db.getProcessField('outputfile', processname))
        filenames = self.db.getFiles(uuid)
        if len(filenames) > 0:
            msg = "Load Process Threads: %s [row: %d]" %  (processname, row)
            print(msg)
            #wx.PostEvent(wxGui, ResultEvent((row,0, uuid, processname)))
            (module_name, class_name) = self.cmodules[processref]
            t = ProcessThread(wxGui, processname, module_name, class_name, mountdir,inputdir, uuid, output,server, row, containername)
            t.start()
            msg = "Running Thread: %s" % processname
            print(msg)
            #Load to database for remote monitoring
            self.db.setSeriesProcess(uuid,self.db.getProcessId(processname),server,1,datetime.datetime.now())
        else:
            msg = "No files to process"
            logger.error(msg)
            raise ValueError(msg)