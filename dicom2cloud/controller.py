from __future__ import print_function
import logging
import threading
import time
import shutil
import os
from glob import iglob
import tarfile
from logging.handlers import RotatingFileHandler
from multiprocessing import freeze_support, Pool
from os import access, R_OK, mkdir
from os.path import join, dirname, exists, split, splitext, expanduser
from config.dbquery import DBI
import datetime
import pydicom
from pydicom.errors import InvalidDicomError
from hashlib import sha256
from controller_utils import generateuid,checkhashed
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

##########################################################################################
class DicomThread(threading.Thread):
    def __init__(self, wxObject, filelist):
        threading.Thread.__init__(self)
        self.wxObject = wxObject
        self.filelist = filelist
        self.db = DBI()

    def run(self):
        print('Starting DICOM thread run')
        n = 1
        try:
            event.set()
            lock.acquire(True)
            for filename in self.filelist:
                try:
                    if not self.db.hasFile(filename):
                        dcm = pydicom.read_file(filename)
                        updatemsg = "Detecting DICOM data ... %d of %d" % (n, len(self.filelist))
                        wx.PostEvent(self.wxObject, DataEvent((updatemsg,[])))
                        #self.m_status.SetLabelText(updatemsg)
                        n += 1

                        # Check DICOM header info
                        series_num = str(dcm.SeriesInstanceUID)
                        uuid = generateuid(series_num)
                        imagetype = str(dcm.ImageType[2])
                        dicomdata = {'uuid': uuid,
                                     'patientid': str(dcm.PatientID),
                                     'patientname': str(dcm.PatientName),
                                     'seriesnum': series_num,
                                     'sequence': str(dcm.SequenceName),
                                     'protocol': str(dcm.ProtocolName),
                                     'imagetype': imagetype
                                     }

                        if not self.db.hasUuid(uuid):
                            self.db.addDicomdata(dicomdata)
                        if not self.db.hasFile(filename):
                            self.db.addDicomfile(uuid, filename)

                except InvalidDicomError:
                    logging.warning("Not valid DICOM - skipping: ", filename)
                    continue
            ############## Load Series Info
            for suid in self.db.getNewUuids():
                numfiles = self.db.getNumberFiles(suid)
                item = [True, self.db.getDicomdata(suid, 'patientname'),
                     self.db.getDicomdata(suid, 'sequence'),
                     self.db.getDicomdata(suid, 'protocol'),
                     self.db.getDicomdata(suid, 'imagetype'), str(numfiles),
                     self.db.getDicomdata(suid, 'seriesnum')]
                wx.PostEvent(self.wxObject, DataEvent((suid, item)))
        except Exception as e:
            updatemsg = 'ERROR encountered during DICOM thread: %s' % e.args[0]
            logging.error(updatemsg)
            wx.PostEvent(self.wxObject, DataEvent((updatemsg,[])))
        finally:
            n = len(self.db.getNewUuids())
            if n > 0:
                msg = "Total Series loaded: %d" % n
            else:
                msg = "Series already processed. Remove via Status Panel to repeat upload."
            if self.db.conn is not None:
                self.db.closeconn()
            logger.info(msg)
            wx.PostEvent(self.wxObject, DataEvent((msg,[])))
            # self.terminate()
            lock.release()
            event.clear()



############################################################################
class ProcessThread(threading.Thread):
    """Multi Worker Thread Class."""
   # wxGui, processname, self.cmodules[processref], targetdir, uuid, server, filenames, row, containername
    # ----------------------------------------------------------------------
    def __init__(self, wxObject, processname, tarfile,uuid, server,row):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.wxObject = wxObject
        self.processname = processname
        self.tarfile = tarfile
        self.uuid = uuid
        self.server = server
        self.row = row
        self.db = DBI()
        self.db.connect()
        if self.db.conn is not None:
            # Dynamic process module
            pref = self.db.getProcessField('ref',processname)
            self.module_name = self.db.getProcessModule(pref)
            self.class_name = self.db.getProcessClass(pref)
            # Instantiate module
            module = importlib.import_module(self.module_name)
            class_ = getattr(module, self.class_name)
            # Docker details
            self.containername = self.db.getProcessField('container', processname)
            self.mountdir = self.db.getProcessField('containerinputdir', processname)
            self.outputfile = join(self.db.getProcessField('containeroutputdir', processname),
                          self.db.getProcessField('outputfile', processname))
            # Docker Class
            self.dcc = class_(self.containername, self.mountdir, self.outputfile)
        else:
            raise Exception('Cannot access Database')

    # ----------------------------------------------------------------------
    def run(self):
        print('Starting thread run')
        try:
            event.set()
            lock.acquire(True)
            (container, timeout) = self.dcc.startDocker(self.tarfile)
            if container is None:
                raise Exception("Unable to initialize Docker")
            ctr = 0
            while (not self.dcc.checkIfDone(container, timeout)):
                time.sleep(1)
                wx.PostEvent(self.wxObject, ResultEvent((self.row,ctr, self.uuid, self.processname, 'Converting')))
                ctr += 10

            # Check that everything ran ok
            if not self.dcc.getStatus(container):
                raise Exception("There was an error while anonomizing the dataset.")

            # Get the resulting mnc file back to the original directory
            self.dcc.finalizeJob(container, dirname(self.tarfile))

            # Upload MNC to server
            mncfile = join(dirname(self.tarfile), self.uuid + '.mnc')
            if access(mncfile, R_OK):
                uploaderClass = get_class(self.server)
                uploader = uploaderClass(self.uuid)
                uploader.upload(mncfile, self.processname)
                wx.PostEvent(self.wxObject, ResultEvent((self.row, ctr,self.uuid, self.processname, 'Uploading')))
                msg ="Uploaded file: %s to %s" % (mncfile, self.server)
                logging.info(msg)

        except Exception as e:
            print("ERROR:", e.args[0])
            wx.PostEvent(self.wxObject, ResultEvent((self.row, -1, self.uuid, self.processname,e.args[0])))

        finally:
            wx.PostEvent(self.wxObject, ResultEvent((self.row,100, self.uuid, self.processname,'Done')))
            msg = 'Finished ProcessThread'
            logger.info(msg)
            print(msg)
            lock.release()
            event.clear()

################################################################################################
class Controller():
    def __init__(self):
        self.logger = self.__loadLogger()
        self.db = DBI()
        if self.db.c is None:
            self.db.connect()

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
        # containername = self.db.getProcessField('container',processname)
        # mountdir = self.db.getProcessField('containerinputdir',processname)
        # output = join(self.db.getProcessField('containeroutputdir',processname),self.db.getProcessField('outputfile', processname))
        filenames = self.db.getFiles(uuid)
        try:
            if len(filenames) > 0:
                msg = "Load Process Threads: %s [row: %d]" %  (processname, row)
                print(msg)
                # Tar DICOM files to load to container for processing
                tarfilename = join(inputdir,uuid + '.tar')
                with tarfile.open(tarfilename, "w") as tar:
                    for f in filenames:
                        tar.add(f)
                tar.close()
                # Run thread
                t = ProcessThread(wxGui, processname, tarfilename, uuid, server, row)
                t.start()
                msg = "Running Thread: %s" % processname
                print(msg)
                #Load to database for remote monitoring
                self.db.setSeriesProcess(uuid,self.db.getProcessId(processname),server,1,datetime.datetime.now(), inputdir)
            else:
                msg = "No files to process"
                logger.error(msg)
                raise ValueError(msg)
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    def removeInputFiles(self,uuid,inputdir):
        """
        Remove temporary files in outputdir (assumes tar file created and uploaded to Docker)
        Remove file entries?
        :return:
        """

        files = iglob(join(inputdir,'*.IMA'))
        for f in files:
            os.remove(f)
        # remove database entry - dicomdata and dicomfiles
        self.db.deleteSeriesData(uuid)


    def checkRemote(self):
        #Check if cloud processing is done and update database
        seriesprocesses = self.db.getActiveProcesses()
        for series in seriesprocesses:
            seriesid = series[0]
            server = series[2].lower()
            outputdir = series[6]
            if outputdir is None or len(outputdir) <= 0:
                files = self.db.getFiles(seriesid)
                outputdir = dirname(files[0])
            # Get uploader class and query
            uploaderClass = get_class(server)
            uploader = uploaderClass(seriesid)
            if uploader.isDone():
                downloadfile = join(outputdir, seriesid, 'download.tar')
                uploader.download(downloadfile)
                msg = 'Series: %s \n\tSTATUS: Complete (%s)\n' % (seriesid, downloadfile)
                print(msg)
                self.db.setSeriesProcessFinished(seriesid)
                #Remove files in database
                self.db.deleteSeriesData(seriesid)
            else:
                #Still in progress
                self.db.setSeriesProcessInprogress(seriesid)

    def parseDicom(self, wxObject,filelist):
        '''
        Read DICOM headers for filelist and load series info to db
        :param filelist:
        :return:
        '''
        t = DicomThread(wxObject, filelist)
        t.start()