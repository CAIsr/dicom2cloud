# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version May  3 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.dataview
import wx.richtext

###########################################################################
## Class ConfigPanel
###########################################################################

class ConfigPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText39 = wx.StaticText( self, wx.ID_ANY, u"Configuration Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		self.m_staticText39.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer16.Add( self.m_staticText39, 0, wx.ALL, 5 )
		
		self.m_staticline8 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer16.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_gridConfig = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_gridConfig.CreateGrid( 20, 3 )
		self.m_gridConfig.EnableEditing( True )
		self.m_gridConfig.EnableGridLines( True )
		self.m_gridConfig.EnableDragGridSize( False )
		self.m_gridConfig.SetMargins( 0, 0 )
		
		# Columns
		self.m_gridConfig.SetColSize( 0, 140 )
		self.m_gridConfig.SetColSize( 1, 140 )
		self.m_gridConfig.SetColSize( 2, 182 )
		self.m_gridConfig.EnableDragColMove( False )
		self.m_gridConfig.EnableDragColSize( True )
		self.m_gridConfig.SetColLabelSize( 30 )
		self.m_gridConfig.SetColLabelValue( 0, u"Name" )
		self.m_gridConfig.SetColLabelValue( 1, u"Value" )
		self.m_gridConfig.SetColLabelValue( 2, u"Description" )
		self.m_gridConfig.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_gridConfig.EnableDragRowSize( True )
		self.m_gridConfig.SetRowLabelSize( 80 )
		self.m_gridConfig.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_gridConfig.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		self.m_gridConfig.SetMinSize( wx.Size( 550,500 ) )
		
		bSizer16.Add( self.m_gridConfig, 0, wx.ALL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_btnSave = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnSave.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_btnSave.SetForegroundColour( wx.Colour( 255, 255, 0 ) )
		self.m_btnSave.SetBackgroundColour( wx.Colour( 0, 128, 128 ) )
		
		bSizer17.Add( self.m_btnSave, 0, wx.ALL, 5 )
		
		self.m_btnAdd = wx.Button( self, wx.ID_ANY, u"Add Row", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_btnAdd, 0, wx.ALL, 5 )
		
		self.m_btnAddProcess = wx.Button( self, wx.ID_ANY, u"Processes (Developers)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_btnAddProcess, 0, wx.ALL, 5 )
		
		self.m_txtStatus = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtStatus.Wrap( -1 )
		bSizer17.Add( self.m_txtStatus, 0, wx.ALL, 5 )
		
		
		bSizer16.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer16 )
		self.Layout()
		bSizer16.Fit( self )
		
		# Connect Events
		self.m_btnSave.Bind( wx.EVT_BUTTON, self.OnSaveConfig )
		self.m_btnAdd.Bind( wx.EVT_BUTTON, self.OnAddRow )
		self.m_btnAddProcess.Bind( wx.EVT_BUTTON, self.OnAddProcess )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSaveConfig( self, event ):
		event.Skip()
	
	def OnAddRow( self, event ):
		event.Skip()
	
	def OnAddProcess( self, event ):
		event.Skip()
	

###########################################################################
## Class ProcessPanel
###########################################################################

class ProcessPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 914,919 ), style = wx.TAB_TRAVERSAL )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText85 = wx.StaticText( self, wx.ID_ANY, u"Process DICOMs", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )
		self.m_staticText85.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		
		bSizer19.Add( self.m_staticText85, 0, wx.ALL, 5 )
		
		self.m_staticline7 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer19.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_stTitle = wx.StaticText( self, wx.ID_ANY, u"TITLE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stTitle.Wrap( -1 )
		self.m_stTitle.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		bSizer29.Add( self.m_stTitle, 0, wx.ALL, 5 )
		
		self.m_stDescription = wx.StaticText( self, wx.ID_ANY, u"Process Description", wx.DefaultPosition, wx.Size( -1,60 ), 0 )
		self.m_stDescription.Wrap( -1 )
		bSizer29.Add( self.m_stDescription, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer20.Add( bSizer29, 1, wx.EXPAND, 5 )
		
		self.m_staticText35 = wx.StaticText( self, wx.ID_ANY, u"Select processes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		bSizer20.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		m_checkListProcessChoices = []
		self.m_checkListProcess = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkListProcessChoices, wx.LB_SINGLE )
		bSizer20.Add( self.m_checkListProcess, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer20, 1, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txtCloudserver = wx.StaticText( self, wx.ID_ANY, u"Select Cloud server", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txtCloudserver.Wrap( -1 )
		bSizer11.Add( self.txtCloudserver, 0, wx.ALL, 5 )
		
		m_serverChoices = [ u"None", u"AWS", u"Google" ]
		self.m_server = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_serverChoices, 0 )
		self.m_server.SetSelection( 0 )
		bSizer11.Add( self.m_server, 0, wx.ALL, 5 )
		
		self.m_btnLog = wx.Button( self, wx.ID_ANY, u"View Log file", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_btnLog, 0, wx.ALL, 5 )
		
		self.m_btnDocker = wx.Button( self, wx.ID_ANY, u"Launch Docker", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_btnDocker, 0, wx.ALL, 5 )
		
		self.m_btnRunProcess = wx.Button( self, wx.ID_ANY, u"RUN", wx.DefaultPosition, wx.Size( 200,50 ), 0 )
		self.m_btnRunProcess.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_btnRunProcess.SetForegroundColour( wx.Colour( 255, 255, 0 ) )
		self.m_btnRunProcess.SetBackgroundColour( wx.Colour( 64, 128, 128 ) )
		self.m_btnRunProcess.Enable( False )
		
		bSizer11.Add( self.m_btnRunProcess, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_dataViewListCtrlRunning = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.FULL_REPAINT_ON_RESIZE )
		self.m_dataViewListCtrlRunning.SetMinSize( wx.Size( -1,400 ) )
		
		self.m_dataViewListColumnProcess = self.m_dataViewListCtrlRunning.AppendTextColumn( u"Process" )
		self.m_dataViewListColumnSeries = self.m_dataViewListCtrlRunning.AppendTextColumn( u"Series ID" )
		self.m_dataViewListColumnStatus = self.m_dataViewListCtrlRunning.AppendProgressColumn( u"Status" )
		self.m_dataViewListColumnOutput = self.m_dataViewListCtrlRunning.AppendTextColumn( u"Output" )
		bSizer21.Add( self.m_dataViewListCtrlRunning, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer21, 1, wx.EXPAND, 5 )
		
		self.m_stOutputlog = wx.StaticText( self, wx.ID_ANY, u"View processing output in log file", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stOutputlog.Wrap( -1 )
		bSizer19.Add( self.m_stOutputlog, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer19 )
		self.Layout()
		
		# Connect Events
		self.m_checkListProcess.Bind( wx.EVT_CHECKLISTBOX, self.OnShowDescription )
		self.m_btnLog.Bind( wx.EVT_BUTTON, self.OnShowLog )
		self.m_btnDocker.Bind( wx.EVT_BUTTON, self.OnLaunchDocker )
		self.m_btnRunProcess.Bind( wx.EVT_BUTTON, self.OnRunScripts )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnShowDescription( self, event ):
		event.Skip()
	
	def OnShowLog( self, event ):
		event.Skip()
	
	def OnLaunchDocker( self, event ):
		event.Skip()
	
	def OnRunScripts( self, event ):
		event.Skip()
	

###########################################################################
## Class CloudPanel
###########################################################################

class CloudPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 700,700 ), style = wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Cloud Processing Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		self.m_staticText18.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
		
		bSizer1.Add( self.m_staticText18, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND, 5 )
		
		self.m_staticText58 = wx.StaticText( self, wx.ID_ANY, u"Click update to refresh status of files processing in the cloud", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.m_staticText58.Wrap( 650 )
		self.m_staticText58.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer1.Add( self.m_staticText58, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_btnCompareRun = wx.Button( self, wx.ID_ANY, u"Update", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_btnCompareRun.SetForegroundColour( wx.Colour( 255, 255, 0 ) )
		self.m_btnCompareRun.SetBackgroundColour( wx.Colour( 0, 128, 64 ) )
		
		bSizer16.Add( self.m_btnCompareRun, 0, wx.ALL, 5 )
		
		self.m_button14 = wx.Button( self, wx.ID_ANY, u"Clear Selected Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button14.SetToolTip( u"Remove data from processing database" )
		
		bSizer16.Add( self.m_button14, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer16, 1, wx.EXPAND, 5 )
		
		self.m_dataViewListCtrlCloud = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.FULL_REPAINT_ON_RESIZE )
		self.m_dataViewListCtrlCloud.SetMinSize( wx.Size( 650,500 ) )
		
		self.m_columnSelect = self.m_dataViewListCtrlCloud.AppendToggleColumn( u"Select" )
		self.m_columnSeries = self.m_dataViewListCtrlCloud.AppendTextColumn( u"Series ID" )
		self.m_columnProcess = self.m_dataViewListCtrlCloud.AppendTextColumn( u"Process" )
		self.m_columnServer = self.m_dataViewListCtrlCloud.AppendTextColumn( u"Server" )
		self.m_columnStatus = self.m_dataViewListCtrlCloud.AppendTextColumn( u"Status" )
		self.m_columnTime = self.m_dataViewListCtrlCloud.AppendTextColumn( u"Time elapsed" )
		bSizer1.Add( self.m_dataViewListCtrlCloud, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_btnCompareRun.Bind( wx.EVT_BUTTON, self.OnUpdate )
		self.m_button14.Bind( wx.EVT_BUTTON, self.OnClearSelected )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnUpdate( self, event ):
		event.Skip()
	
	def OnClearSelected( self, event ):
		event.Skip()
	

###########################################################################
## Class WelcomePanel
###########################################################################

class WelcomePanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 688,763 ), style = wx.TAB_TRAVERSAL )
		
		self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Dicom 2 Cloud", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetFont( wx.Font( 14, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		bSizer18.Add( self.m_staticText23, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer18.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_richText1 = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER|wx.WANTS_CHARS, wx.DefaultValidator, u"welcome" )
		self.m_richText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
		self.m_richText1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer18.Add( self.m_richText1, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer18 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class FilesPanel
###########################################################################

class FilesPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 700,700 ), style = wx.TAB_TRAVERSAL )
		
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Select DICOMs for analysis", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetFont( wx.Font( 14, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer5.Add( self.m_staticText23, 0, wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Browse and/or Drag N Drop to select folder containing patient DICOM files then click select the required series. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		self.m_staticText25.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		
		bSizer5.Add( self.m_staticText25, 0, wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer5.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
		
		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, u"Patient DICOM directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		fgSizer4.Add( self.m_staticText26, 0, wx.ALL, 5 )
		
		self.txtInputdir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer4.Add( self.txtInputdir, 0, wx.ALL, 5 )
		
		self.m_button18 = wx.Button( self, wx.ID_ANY, u"Browse", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_button18, 0, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self, wx.ID_ANY, u"Output directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		fgSizer4.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.txtOutputdir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		fgSizer4.Add( self.txtOutputdir, 0, wx.ALL, 5 )
		
		self.m_button16 = wx.Button( self, wx.ID_ANY, u"Browse", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_button16, 0, wx.ALL, 5 )
		
		self.m_cbSelectall = wx.CheckBox( self, wx.ID_ANY, u"All Files", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_cbSelectall.SetValue(True) 
		fgSizer4.Add( self.m_cbSelectall, 0, wx.ALL, 5 )
		
		self.m_tcDragdrop = wx.TextCtrl( self, wx.ID_ANY, u"Drag DICOM folder here !", wx.DefaultPosition, wx.Size( 250,100 ), wx.TE_CENTRE|wx.TE_READONLY )
		self.m_tcDragdrop.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		fgSizer4.Add( self.m_tcDragdrop, 0, wx.ALIGN_CENTER, 5 )
		
		self.btnClearlist = wx.Button( self, wx.ID_ANY, u"Clear List", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.btnClearlist, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer5.Add( fgSizer4, 1, wx.ALIGN_TOP|wx.EXPAND, 5 )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_dataViewListCtrl1 = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.dataview.DV_MULTIPLE )
		self.m_dataViewListCtrl1.SetMinSize( wx.Size( -1,300 ) )
		
		self.col_selected = self.m_dataViewListCtrl1.AppendToggleColumn( u"Select" )
		self.col_patient = self.m_dataViewListCtrl1.AppendTextColumn( u"Patient" )
		self.col_sequence = self.m_dataViewListCtrl1.AppendTextColumn( u"Sequence" )
		self.col_protocol = self.m_dataViewListCtrl1.AppendTextColumn( u"Protocol" )
		self.col_imagetype = self.m_dataViewListCtrl1.AppendTextColumn( u"Image Type" )
		self.col_num = self.m_dataViewListCtrl1.AppendTextColumn( u"Num Files" )
		self.col_series = self.m_dataViewListCtrl1.AppendTextColumn( u"Series ID" )
		bSizer18.Add( self.m_dataViewListCtrl1, 0, wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
		
		self.m_status = wx.StaticText( self, wx.ID_ANY, u"Select required files then go to Run Processes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status.Wrap( -1 )
		bSizer18.Add( self.m_status, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		# Connect Events
		self.m_button18.Bind( wx.EVT_BUTTON, self.OnInputdir )
		self.m_button16.Bind( wx.EVT_BUTTON, self.OnOutputdir )
		self.m_cbSelectall.Bind( wx.EVT_CHECKBOX, self.OnSelectall )
		self.btnClearlist.Bind( wx.EVT_BUTTON, self.OnClearlist )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnInputdir( self, event ):
		event.Skip()
	
	def OnOutputdir( self, event ):
		event.Skip()
	
	def OnSelectall( self, event ):
		event.Skip()
	
	def OnClearlist( self, event ):
		event.Skip()
	

###########################################################################
## Class dlgLogViewer
###########################################################################

class dlgLogViewer ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Log Viewer", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText35 = wx.StaticText( self, wx.ID_ANY, u"Processing Log", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		self.m_staticText35.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		
		bSizer12.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		self.m_textLog = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self.m_textLog.SetMinSize( wx.Size( 400,500 ) )
		
		bSizer12.Add( self.m_textLog, 0, wx.ALL, 5 )
		
		self.m_btnRefresh = wx.Button( self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_btnRefresh, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer12 )
		self.Layout()
		bSizer12.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_btnRefresh.Bind( wx.EVT_BUTTON, self.OnLogRefresh )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnLogRefresh( self, event ):
		event.Skip()
	

###########################################################################
## Class dlgProcess
###########################################################################

class dlgProcess ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Process modules configuration", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.Size( 600,-1 ), wx.DefaultSize )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"Developers can add or edit process info but use with CAUTION", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		bSizer14.Add( self.m_staticText18, 0, wx.ALL, 5 )
		
		self.m_grid2 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		
		# Grid
		self.m_grid2.CreateGrid( 5, 11 )
		self.m_grid2.EnableEditing( True )
		self.m_grid2.EnableGridLines( True )
		self.m_grid2.EnableDragGridSize( False )
		self.m_grid2.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid2.EnableDragColMove( False )
		self.m_grid2.EnableDragColSize( True )
		self.m_grid2.SetColLabelSize( 30 )
		self.m_grid2.SetColLabelValue( 0, u"id" )
		self.m_grid2.SetColLabelValue( 1, u"ref" )
		self.m_grid2.SetColLabelValue( 2, u"process" )
		self.m_grid2.SetColLabelValue( 3, u"description" )
		self.m_grid2.SetColLabelValue( 4, u"module" )
		self.m_grid2.SetColLabelValue( 5, u"class" )
		self.m_grid2.SetColLabelValue( 6, u"container" )
		self.m_grid2.SetColLabelValue( 7, u"containerinputdir" )
		self.m_grid2.SetColLabelValue( 8, u"containeroutputdir" )
		self.m_grid2.SetColLabelValue( 9, u"outputfile" )
		self.m_grid2.SetColLabelValue( 10, u"filename" )
		self.m_grid2.SetColLabelValue( 11, wx.EmptyString )
		self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid2.EnableDragRowSize( True )
		self.m_grid2.SetRowLabelSize( 80 )
		self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer14.Add( self.m_grid2, 0, wx.ALL, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.mbtnSaveProcessChanges = wx.Button( self, wx.ID_ANY, u"Save changes", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.mbtnSaveProcessChanges, 0, wx.ALL, 5 )
		
		self.m_btnAddProcessRow = wx.Button( self, wx.ID_ANY, u"Add New", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_btnAddProcessRow, 0, wx.ALL, 5 )
		
		
		bSizer14.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		self.m_status = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_status.Wrap( -1 )
		bSizer14.Add( self.m_status, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer14 )
		self.Layout()
		bSizer14.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.mbtnSaveProcessChanges.Bind( wx.EVT_BUTTON, self.OnSaveProcess )
		self.m_btnAddProcessRow.Bind( wx.EVT_BUTTON, self.OnAddProcessRow )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSaveProcess( self, event ):
		event.Skip()
	
	def OnAddProcessRow( self, event ):
		event.Skip()
	

