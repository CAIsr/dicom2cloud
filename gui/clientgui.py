import wx
from os import listdir, R_OK, path, mkdir, access, walk
from os.path import isdir, join
import argparse
import sys
import re
from glob import iglob
import shutil
import time
import dicom
from dicom.filereader import InvalidDicomError, read_file
from noname import *
series ={}


########################################################################
class HomePanel(WelcomePanel):
    """
    This will be the first notebook tab
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        super(HomePanel, self).__init__(parent)
        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        # text = wx.TextCtrl(self, style=wx.TE_MULTILINE,value=self.__loadContent())
        # hbox.Add(text, proportion=1, flag=wx.EXPAND)
        # self.SetSizer(hbox)
        self.m_richText1.AddParagraph(r'''***Welcome to the Clinic2Cloud App***''')
        self.m_richText1.AddParagraph(r''' An application to process your MRI scans in the cloud ''')
        # self.m_richText1.BeginNumberedBullet(1, 0.2, 0.2, wx.TEXT_ATTR_BULLET_STYLE)
        self.m_richText1.AddParagraph(
            r"1. Select a Folder containing one or more MRI scans to process in the Files Panel")
        self.m_richText1.AddParagraph(r"2. Select which processes to run and monitor their progress")

        self.m_richText1.AddParagraph(r"Created by Clinic2Cloud team at HealthHack 2017")
        self.m_richText1.AddParagraph(
            r"Copyright (2017) Apache license v2 ")

    def __loadContent(self):
        """
        Welcome text
        :return:
        """
        content = '''***Welcome to the MSD Automated Analysis App***
        To process your files: 
            1. Check the Configuration options, particularly the column names and filenames used for matching
            2. Select Files to process either with AutoFind from a top level directory and/or Drag and Drop
            3. Select which processes to run and monitor their progress
            4. Choose Compare Groups to run a statistical comparison of two groups after processing files have been generated

        '''
        return content

########################################################################
class ProcessRunPanel(ProcessPanel):
    def __init__(self, parent):
        super(ProcessRunPanel, self).__init__(parent)
        self.processes = [{'caption':'None','href': 'na',
             'description':''},
            {'caption': 'QSM', 'href': 'qsm',
             'description': 'Estimate quantitative susceptibility map from gradient echo data. Phase and magnitude images required.',
             },
            {'caption': 'Atlas', 'href': 'atlas',
             'description': 'Estimate atlas-based segmentation from T1-weighted image. Magnitude image required.',
             }
            ]

        processes = [p['caption'] for p in self.processes]
        #self.m_checkListProcess.AppendItems(processes)
        # Set up event handler for any worker thread results
        #EVT_RESULT(self, self.progressfunc)
        # EVT_CANCEL(self, self.stopfunc)
        # Set timer handler
        self.start = {}

    def OnShowDescription(self, event):
        print(event.String)
        desc = [p['description'] for p in self.processes if p['caption'] == event.String]

        # Load to GUI
        self.m_stTitle.SetLabelText(event.String)
        self.m_stDescription.SetLabelText(desc[0])
        self.Layout()

    def progressfunc(self, msg):
        """
        Update progress bars in table - multithreaded
        :param count:
        :param row:
        :param col:
        :return:
        """
        (count, row, i, total, process) = msg.data
        print("\nProgress updated: ", time.ctime())
        print('count = ', count)
        status = "%d of %d files " % (i, total)
        if count == 0:
            self.m_dataViewListCtrlRunning.AppendItem([process, count, "Pending"])
            self.start[process] = time.time()
        elif count < 0:
            self.m_dataViewListCtrlRunning.SetValue("ERROR in " + status, row=row, col=2)
            self.m_btnRunProcess.Enable()
        elif count < 100:
            self.m_dataViewListCtrlRunning.SetValue(count, row=row, col=1)
            self.m_dataViewListCtrlRunning.SetValue("Running " + status, row=row, col=2)
        else:
            if process in self.start:
                endtime = time.time() - self.start[process]
                status = "%s (%d secs)" % (status, endtime)
            print(status)
            self.m_dataViewListCtrlRunning.SetValue(count, row=row, col=1)
            self.m_dataViewListCtrlRunning.SetValue("Done " + status, row=row, col=2)
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
        self.shutdown()
        print("Cancel multiprocessor")
        event.Skip()

    def OnRunScripts(self, event):
        """
        Run selected scripts sequentially - updating progress bars
        :param e:
        :return:
        """
        # Clear processing window
        self.m_dataViewListCtrlRunning.DeleteAllItems()
        # Disable Run button
        # self.m_btnRunProcess.Disable()
        btn = event.GetEventObject()
        btn.Disable()
        # Get selected processes
        selections = self.m_checkListProcess.GetCheckedStrings()
        print("Processes selected: ", len(selections))
        # Get data from other panels
        filepanel = self.getFilePanel()
        filenames = []
        num_files = filepanel.m_dataViewListCtrl1.GetItemCount()
        print('All Files:', num_files)
        if len(selections) > 0 and num_files > 0:
            for i in range(0, num_files):
                if filepanel.m_dataViewListCtrl1.GetToggleValue(i, 0):
                    filenames.append(filepanel.m_dataViewListCtrl1.GetValue(i, 1))
            print('Selected Files:', len(filenames))
            row = 0
            # For each process
            for p in selections:
                print("Running:", p)
                i = [i for i in range(len(self.processes)) if p == self.processes[i]['caption']][
                    0]
                #self.RunProcess(self, filenames, i, outputdir, expt, row)
                row = row + 1
                print('Next process: row=', row)

            print("Completed processes")
        else:
            if len(selections) <= 0:
                msg = "No processes selected"
            else:
                msg = "No files selected - please go to Files Panel and add to list"
            self.Parent.Warn(msg)
            # Enable Run button
            self.m_btnRunProcess.Enable()

########################################################################
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, target):
        super(MyFileDropTarget, self).__init__()
        self.target = target

    def OnDropFiles(self, x, y, filenames):
        for fname in filenames:
            self.target.AppendItem([True, fname]) #TODO
        return len(filenames)


########################################################################
class FileSelectPanel(FilesPanel):
    def __init__(self, parent):
        super(FileSelectPanel, self).__init__(parent)
        self.filedrop = MyFileDropTarget(self.m_dataViewListCtrl1)
        self.m_tcDragdrop.SetDropTarget(self.filedrop)


    def OnInputdir(self, e):
        """ Open a file"""
        dlg = wx.DirDialog(self, "Choose a directory containing input files")
        if dlg.ShowModal() == wx.ID_OK:
            self.inputdir = str(dlg.GetPath())
            # self.statusbar.SetStatusText("Loaded: %s" % self.inputdir)
            self.txtInputdir.SetValue(self.inputdir)
            self.extractSeriesInfo(self.inputdir)

        dlg.Destroy()


    def extractSeriesInfo(self, inputdir):
        """
        Find all matching files in top level directory
        :param event:
        :return:
        """
        self.m_status.SetLabelText("Detecting DICOM data ... please wait")
        #allfiles = [y for y in iglob(join(inputdir, '*.IMA'))]
        allfiles = [y for x in walk(inputdir) for y in iglob(join(x[0], '*.IMA'))]
        #series = {}
        for filename in allfiles:
            try:
                dcm = dicom.read_file(filename)
            except InvalidDicomError:
                print("Not DICOM - skipping: ", filename)
                continue

            #Check DICOM header info

            series_num = str(dcm.SeriesInstanceUID)
            imagetype = str(dcm.ImageType[2])
            dicomdata = {'patientid': str(dcm.PatientID),
                     'patientname': str(dcm.PatientName),
                    'series_num': series_num,
                    'sequence': str(dcm.SequenceName),
                     'protocol':str(dcm.ProtocolName),
                    'imagetype':imagetype
                     }
            if series_num not in series:
                series[series_num] = {'dicomdata':dicomdata, 'files':[]}
            series[series_num]['files'].append(filename)

        #Load for selection
        for s in series.items():
            s = s[1]['dicomdata']
            self.m_dataViewListCtrl1.AppendItem([True,s['patientid'],s['sequence'], s['protocol'],s['imagetype'],s['series_num']])

        #self.col_file.SetMinWidth(wx.LIST_AUTOSIZE)
        msg = "Total Series loaded: %d" % self.m_dataViewListCtrl1.GetItemCount()
        self.m_status.SetLabelText(msg)


    def OnSelectall(self, event):
        for i in range(0, self.m_dataViewListCtrl1.GetItemCount()):
            self.m_dataViewListCtrl1.SetToggleValue(event.GetSelection(), i, 0)
        print("Toggled selections to: ", event.GetSelection())

    def OnClearlist(self, event):
        print("Clear items in list")
        self.m_dataViewListCtrl1.DeleteAllItems()

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
        # il = wx.ImageList(32, 32)
        # # for x in [wx.ArtProvider.]:
        # #     obj = getattr(images, 'LB%02d' % (x + 1))
        # #     bmp = obj.GetBitmap()
        # #     il.Add(bmp)
        # bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP_SETTINGS, wx.ART_FRAME_ICON, (16, 16))
        # il.Add(bmp)
        # bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_FRAME_ICON, (16, 16))
        # il.Add(bmp)
        # bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_FRAME_ICON, (16, 16))
        # il.Add(bmp)
        # self.AssignImageList(il)

        pages = [(HomePanel(self),'Welcome'),
                 #(ConfigPanel(self), "Configure"),
                 (FileSelectPanel(self), "Select Files"),
                 (ProcessRunPanel(self), "Run Processes"),
                 (ComparePanel(self), "Compare Groups")]


        imID = 0
        for page, label in pages:
            # self.AddPage(page, label, imageId=imID)
            self.AddPage(page, label)
            imID += 1

        self.GetListView().SetColumnWidth(0, wx.LIST_AUTOSIZE)

        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGING, self.OnPageChanging)

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
                          "Clinic2Cloud App",
                          size=(900, 900)
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


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = ClinicApp()
    app.MainLoop()
