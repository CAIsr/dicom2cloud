from __future__ import print_function

import datetime
import shutil
import sys
import time
from glob import iglob
from os import W_OK, mkdir, access, walk
from os.path import join, isdir, split, exists, basename
from dicom2cloud.config.dbquery import DBI
from dicom2cloud.controller_utils import generateuid
from dicom2cloud.controller import EVT_DATA, EVT_RESULT, Controller
from dicom2cloud.gui.wxclientgui import *

__version__ = '0.1.alpha'

global_series = {}


########################################################################
class HomePanel(WelcomePanel):
    """
    This will be the first notebook tab
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        img = wx.Bitmap(1, 1)
        img.LoadFile(join('gui', 'MRI_img.bmp'), wx.BITMAP_TYPE_BMP)
        self.m_richText1.BeginAlignment(wx.TEXT_ALIGNMENT_CENTRE)
        # self.m_richText1.BeginFontSize(14)
        # welcome = "Welcome to the Dicom2Cloud Application"
        # self.m_richText1.WriteText(welcome)
        # self.m_richText1.EndFontSize()
        # self.m_richText1.Newline()
        self.m_richText1.BeginTextColour(wx.Colour(255, 255, 255))
        self.m_richText1.BeginFontSize(12)
        self.m_richText1.WriteText("Process your MRI scans with high performance functions in the cloud")

        self.m_richText1.Newline()
        self.m_richText1.WriteImage(img)
        self.m_richText1.Newline()
        self.m_richText1.BeginFontSize(12)
        welcome = "How to use this desktop application"
        self.m_richText1.WriteText(welcome)
        self.m_richText1.EndFontSize()
        self.m_richText1.Newline()
        self.m_richText1.Newline()
        self.m_richText1.BeginNumberedBullet(1, 100, 60)

        self.m_richText1.WriteText("1. Select a Folder containing one or more MRI scans to process in the Files Panel")
        self.m_richText1.EndNumberedBullet()
        self.m_richText1.Newline()
        self.m_richText1.BeginNumberedBullet(2, 100, 60)
        # self.m_richText1.Newline()
        self.m_richText1.WriteText("2. Select which processes to run and monitor their progress in the Process Panel")
        self.m_richText1.EndNumberedBullet()

        self.m_richText1.Newline()
        self.m_richText1.Newline()
        # self.m_richText1.AddParagraph(r"Created by Clinic2Cloud team at HealthHack 2017")
        self.m_richText1.BeginItalic()
        txt = "Copyright 2017 Dicom2Cloud Team (version %s)" % __version__
        self.m_richText1.WriteText(txt)
        self.m_richText1.EndItalic()
        self.m_richText1.Newline()
        # self.m_richText1.AddParagraph(
        #     r"This is free software, you may use/distribute it under the terms of the Apache license v2")
        self.m_richText1.EndAlignment()
        self.m_richText1.EndTextColour()


########################################################################
class Config(ConfigPanel):
    def __init__(self, parent):
        super(Config, self).__init__(parent)
        self.parent = parent
        self.dbi = DBI()
        self.OnLoadData()

    def OnLoadData(self):
        self.dbi.connect()
        #load config values
        conf = self.dbi.getServerConfig()
        if conf is not None:
            rownum=0
            for k in conf.keys():
                self.m_gridConfig.SetCellValue(rownum, 0, k)
                self.m_gridConfig.SetCellValue(rownum, 1, conf[k][0])
                if conf[k][1] is not None:
                    self.m_gridConfig.SetCellValue(rownum, 2, conf[k][1])
                rownum += 1
        self.dbi.closeconn()


    def OnSaveConfig(self, event):
        self.dbi.connect()
        #configid = self.cboConfigid.GetValue()
        configlist=[]
        data = self.m_gridConfig.GetTable()
        for rownum in range(0, data.GetRowsCount()):
            if not data.IsEmptyCell(rownum, 0):
                configlist.append((self.m_gridConfig.GetCellValue(rownum, 0),
                                   self.m_gridConfig.GetCellValue(rownum, 1),
                                   self.m_gridConfig.GetCellValue(rownum, 2)))
        print('Saved settings:', configlist)
        # Save to DB
        cnt = self.dbi.addServerConfig(configlist)

        #notification
        msg = "Settings saved: %s" % cnt
        self.m_txtStatus.SetLabelText(msg)
        self.dbi.closeconn()

    def OnAddRow(self, event):
        self.m_gridConfig.AppendRows(1, True)

########################################################################

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, panel, target):
        super(MyFileDropTarget, self).__init__()
        self.target = target
        self.droppedfiles = []
        self.panel = panel

    def OnDropFiles(self, x, y, filenames):
        for fname in filenames:
            if not isdir(fname):
                fname = split(fname)[0]
            self.panel.extractSeriesInfo(fname)
            # self.target.AppendItem([True, fname])  # TODO
        return len(filenames)


########################################################################
class FileSelectPanel(FilesPanel):
    def __init__(self, parent):
        super(FileSelectPanel, self).__init__(parent)
        self.filedrop = MyFileDropTarget(self, self.m_dataViewListCtrl1)
        self.m_tcDragdrop.SetDropTarget(self.filedrop)
        self.outputdir = ''
        EVT_DATA(self, self.UpdateStatus)
        self.controller = Controller()

    def OnInputdir(self, e):
        """ Open a file"""
        dlg = wx.DirDialog(self, "Choose a directory containing input files")
        if dlg.ShowModal() == wx.ID_OK:
            self.inputdir = str(dlg.GetPath())
            # self.statusbar.SetStatusText("Loaded: %s" % self.inputdir)
            self.txtInputdir.SetValue(self.inputdir)
            self.extractSeriesInfo(self.inputdir)

        dlg.Destroy()

    def OnOutputdir(self, e):
        """ Open a file"""
        dlg = wx.DirDialog(self, "Choose a directory for upload files")
        if dlg.ShowModal() == wx.ID_OK:
            self.outputdir = str(dlg.GetPath())
            self.txtOutputdir.SetValue(self.outputdir)
        dlg.Destroy()

    def UpdateStatus(self, event):
        print('Update status called')
        (updatemsg, item) = event.data
        if len(item) > 0:
            self.m_dataViewListCtrl1.AppendItem(item)
        self.m_status.SetLabelText(updatemsg)

    def extractSeriesInfo(self, inputdir):
        """
        Find all matching files in top level directory
        :param event:
        :return:
        """
        self.m_status.SetLabelText("Detecting DICOM data ... please wait")
        allfiles = [y for x in walk(inputdir) for y in iglob(join(x[0], '*.IMA'))]
        self.controller.parseDicom(self, allfiles)


    def OnSelectall(self, event):
        for i in range(0, self.m_dataViewListCtrl1.GetItemCount()):
            self.m_dataViewListCtrl1.SetToggleValue(event.GetSelection(), i, 0)
        print("Toggled selections to: ", event.GetSelection())

    def OnClearlist(self, event):
        print("Clear items in list")
        self.m_dataViewListCtrl1.DeleteAllItems()


########################################################################
class ProcessRunPanel(ProcessPanel):
    def __init__(self, parent):
        super(ProcessRunPanel, self).__init__(parent)
        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.progressfunc)
        # EVT_CANCEL(self, self.stopfunc)
        # Set timer handler
        self.start = {}
        self.toggleval = 0
        # self.server = ''
        self.controller = Controller()
        choices = self.controller.db.getCaptions()
        self.m_checkListProcess.AppendItems(choices)

    def progressfunc(self, msg):
        """
        Update progress bars in table - multithreaded
        :param count:
        :param row:
        :param col:
        :return:
        """
        (row, count, seriesid, process, statusmessage) = msg.data
        print("\nProgress updated: ", time.ctime())
        print('\tPROGRESS: count = ', count, " row=", row)
        # row = 0
        for item in range(self.m_dataViewListCtrlRunning.GetItemCount()):
            if self.m_dataViewListCtrlRunning.GetValue(row=item, col=1) == seriesid:
                row = item

        status = ''
        if count == 0:
            self.m_dataViewListCtrlRunning.AppendItem([process, seriesid, count, "Pending"])
            self.start[seriesid] = time.time()
        elif count < 0:
            if len(statusmessage) <= 0:
                statusmessage = "Unknown"
            self.m_dataViewListCtrlRunning.SetValue("ERROR: " + statusmessage, row=row, col=3)
            self.m_btnRunProcess.Enable()
            self.m_stOutputlog.SetLabelText(statusmessage)
        elif count < 100:
            if len(statusmessage) <= 0:
                statusmessage = "Running"
            self.m_dataViewListCtrlRunning.SetValue(statusmessage, row=row, col=3)
            self.m_dataViewListCtrlRunning.SetValue(count, row=row, col=2)
        else:
            if seriesid in self.start:
                endtime = time.time() - self.start[seriesid]
                status = "(%d secs)" % endtime
            print(status)
            self.m_dataViewListCtrlRunning.SetValue(100, row=row, col=2)
            self.m_dataViewListCtrlRunning.SetValue("Done " + status, row=row, col=3)
            self.m_btnRunProcess.Enable()

    def getFilePanel(self):
        """
        Get access to filepanel
        :return:
        """
        filepanel = None

        for fp in self.Parent.Children:
            if isinstance(fp, FileSelectPanel):
                filepanel = fp
                break
        return filepanel

    def OnCancelScripts(self, event):
        """
        Find a way to stop processes
        :param event:
        :return:
        """
        # self.shutdown()
        print("Cancel multiprocessor")
        event.Skip()

    def OnShowDescription(self, event):
        desc = self.controller.db.getDescription(event.String)
        self.m_stTitle.SetLabelText(event.String)
        self.m_stDescription.SetLabelText(desc)
        self.Layout()
        cbtn = event.GetEventObject()
        if len(cbtn.GetCheckedItems()) > 0:
            self.m_btnRunProcess.Enable()
        else:
            self.m_btnRunProcess.Disable()

    def OnRunScripts(self, event):
        """
        Run selected scripts sequentially - updating progress bars
        :param e:
        :return:
        """
        # initialize
        msg = ''
        filenames = []
        # Clear processing window
        self.m_dataViewListCtrlRunning.DeleteAllItems()
        # Disable Run button
        btn = event.GetEventObject()
        btn.Disable()
        # Get selected processes
        processes = self.m_checkListProcess.GetCheckedStrings()
        print("Processes selected: ", processes)
        # Get Cloud Server
        server = self.m_server.GetStringSelection().lower()
        # Get Output directory and File list
        filepanel = self.getFilePanel()
        try:
            if filepanel.outputdir is not None and len(filepanel.outputdir) > 0:
                targetdir = filepanel.outputdir
            else:
                targetdir = join(filepanel.inputdir, '..',
                                 'processed')  # check no files will be overwritten by creating subdir
                msg = "No outputdir provided - using subdir: %s" % targetdir
                print(msg)
            if not exists(targetdir):
                try:
                    mkdir(targetdir)
                except:
                    msg = 'Cannot create %s' % targetdir
                    raise IOError(msg)
            elif not access(targetdir, W_OK):
                msg = "Cannot access directory %s" % targetdir
                raise IOError(msg)

            num_files = filepanel.m_dataViewListCtrl1.GetItemCount()
            print('Selected Series:', num_files)

            if len(processes) > 0 and num_files > 0:
                # For each process, own thread per fileset
                row = 0
                for p in processes:
                    for i in range(0, num_files):
                        if filepanel.m_dataViewListCtrl1.GetToggleValue(i, 0):
                            seriesid = filepanel.m_dataViewListCtrl1.GetValue(i, 6)
                            # for each series, create temp dir and copy files
                            # self.m_stOutputlog.SetLabelText("Copying DICOM data %s ..." % seriesid)
                            uuid = generateuid(seriesid)
                            if self.copyseries(uuid, targetdir):
                                self.m_stOutputlog.SetLabelText("Uploading %s" % seriesid)
                                self.controller.RunProcess(self, targetdir, uuid, p, server, row)
                                row = row + 1

            else:
                if len(processes) == 0:
                    msg = "No processes selected"
                else:
                    msg = "No files selected - please go to Files Panel and add to list"
                raise ValueError(msg)
        except Exception as e:
            self.Parent.Warn(e.args[0])
        finally:
            # self.m_stOutputlog.SetLabelText("** Finished uploading to Cloud **")
            # Enable Run button
            self.m_btnRunProcess.Enable()

    def OnShowLog(self, event):
        """
        Load logfile into viewer
        :param event:
        :return:
        """
        dlg = LogViewer(self)
        dlg.OnLogRefresh(event)
        dlg.ShowModal()
        dlg.Destroy()

    def copyseries(self, suuid, targetdir):
        """
        Copy series to temp dir if doesn't exist and save location
        :param self:
        :param suuid: series uuid
        :param targetdir:
        :return: False if no files to copy or destination folder with copied files
        """
        seriesfiles = self.controller.db.getFiles(suuid)
        dest = False
        if seriesfiles is not None and len(seriesfiles) > 0:
            dest = join(targetdir, suuid)
            if not exists(dest):
                mkdir(dest)
            for f in seriesfiles:
                if not exists(join(dest, basename(f))):
                    shutil.copy(f, dest)
        return dest


#########################################################################
class LogViewer(dlgLogViewer):
    def __init__(self, parent):
        super(LogViewer, self).__init__(parent)
        self.logfile = parent.controller.logfile

    def OnLogRefresh(self, event):
        self.m_textLog.LoadFile(self.logfile)


########################################################################
class CloudRunPanel(CloudPanel):
    def __init__(self, parent):
        super(CloudRunPanel, self).__init__(parent)
        self.controller = Controller()

    def getStatus(self, code):
        status = {0: 'Failed', 1: 'Uploaded', 2: 'In progress', 3: 'Complete'}
        return status[code]

    def OnUpdate(self, event):
        """
        Load dummydatabase and for each seriesID - poll class
        :param event:
        :return:
        """
        # Check remote - TODO
        # Query database for status of processing
        # 2018-04-11 13:25:56.914000
        self.controller.checkRemote()
        seriesprocesses = self.controller.db.getActiveProcesses()
        self.m_dataViewListCtrlCloud.DeleteAllItems()
        for series in seriesprocesses:
            # time delta
            t1 = datetime.datetime.strptime(series[4], '%Y-%m-%d %H:%M:%S.%f')
            if series[5] is not None:
                t2 = datetime.datetime.strptime(series[5], '%Y-%m-%d %H:%M:%S.%f')
            else:
                t2 = datetime.datetime.now()
            tdiff = t2 - t1
            # Load to window
            self.m_dataViewListCtrlCloud.AppendItem(
                [False, series[0], series[1], series[2].upper(), self.getStatus(series[3]), str(tdiff)])

    def OnClearSelected(self, event):
        """
        Clears data from database and in output panel
        :param event:
        :return:
        """

        for i in range(self.m_dataViewListCtrlCloud.GetItemCount()):
            if self.m_dataViewListCtrlCloud.GetToggleValue(i, 0):
                series = self.m_dataViewListCtrlCloud.GetValue(i, 1)
                self.controller.db.deleteSeriesData(series)
                self.m_dataViewListCtrlCloud.DeleteItem(i)
                print('Row removed: ', i)


########################################################################
class AppMain(wx.Listbook):
    def __init__(self, parent):
        """Constructor"""
        wx.Listbook.__init__(self, parent, wx.ID_ANY, style=wx.BK_DEFAULT)

        self.InitUI()
        self.Centre(wx.BOTH)
        self.Show()

    def InitUI(self):

        # make an image list using the LBXX images
        il = wx.ImageList(32, 32)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_FRAME_ICON, (32, 32))
        il.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_FRAME_ICON, (32, 32))
        il.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_FRAME_ICON, (32, 32))
        il.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_FRAME_ICON, (32, 32))
        il.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_FRAME_ICON, (32, 32))
        il.Add(bmp)
        self.AssignImageList(il)

        pages = [(HomePanel(self), 'Welcome'),
                 (Config(self), 'Settings'),
                 (FileSelectPanel(self), "DICOM Files"),
                 (ProcessRunPanel(self), "Run in Cloud"),
                 (CloudRunPanel(self), "Check Status")]

        imID = 0
        for page, label in pages:
            self.AddPage(page, label, imageId=imID)
            # self.AddPage(page, label)
            imID += 1

        if sys.platform == 'win32':
            self.GetListView().SetColumnWidth(0, wx.LIST_AUTOSIZE)

            # self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
            # self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

    # ----------------------------------------------------------------------
    def OnPageChanged(self, event):
        # old = event.GetOldSelection()
        # new = event.GetSelection()
        # sel = self.GetSelection()
        # msg = 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        # print(msg)
        event.Skip()

    # ----------------------------------------------------------------------
    def OnPageChanging(self, event):
        # old = event.GetOldSelection()
        # new = event.GetSelection()
        # sel = self.GetSelection()
        # msg = 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
        # print(msg)
        event.Skip()

    def Warn(self, message, caption='Warning!'):
        dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, e):
        self.Close()

    def OnCloseWindow(self, e):

        dial = wx.MessageDialog(None, 'Are you sure you want to quit?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()


########################################################################
class ClinicApp(wx.Frame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Dicom2Cloud Desktop Application",
                          size=(700, 700)
                          )

        # self.timer = wx.Timer(self)
        # self.Bind(wx.EVT_TIMER, self.update, self.timer)
        panel = wx.Panel(self)

        notebook = AppMain(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
        self.Center(wx.BOTH)
        self.Show()


def main():
    app = wx.App()
    frame = ClinicApp()
    app.MainLoop()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
