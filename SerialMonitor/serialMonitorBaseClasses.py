# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

parseOutputsTimerID = 1000

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"serialMonitor", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.Size( 600,400 ), wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.serialPortText = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Serial port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.serialPortText.Wrap( -1 )
		bSizer2.Add( self.serialPortText, 0, wx.ALL|wx.EXPAND, 5 )
		
		portChoiceChoices = []
		self.portChoice = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, portChoiceChoices, 0 )
		self.portChoice.SetSelection( 0 )
		self.portChoice.SetMinSize( wx.Size( 120,-1 ) )
		
		bSizer2.Add( self.portChoice, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.updatePortsButton = wx.Button( self.m_panel1, wx.ID_ANY, u"Update ports", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.updatePortsButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.disconnectButton = wx.Button( self.m_panel1, wx.ID_ANY, u"Disconnect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.disconnectButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.baudRateText = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Baud rate:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.baudRateText.Wrap( -1 )
		bSizer2.Add( self.baudRateText, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.baudRateTxtCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"19200", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer2.Add( self.baudRateTxtCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.readDelayText = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Read delay [ms]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.readDelayText.Wrap( -1 )
		bSizer2.Add( self.readDelayText, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.readDelayTxtCtrl = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"1000", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer2.Add( self.readDelayTxtCtrl, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.clearButton = wx.Button( self.m_panel1, wx.ID_ANY, u"Clear console", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.clearButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.rawOutputCheckbox = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Raw output", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rawOutputCheckbox.SetToolTip( u"Toggle between displaying complete lines terminated with an EOL char, or all received bytes as they arrive." )
		
		bSizer2.Add( self.rawOutputCheckbox, 0, wx.ALL, 5 )
		
		self.hexOutputCheckbox = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Hex output", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hexOutputCheckbox.SetToolTip( u"Tick to show hex codes of the received bytes. Only works with \"Raw output\"." )
		
		bSizer2.Add( self.hexOutputCheckbox, 0, wx.ALL, 5 )
		
		self.fileLogCheckbox = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Log to file", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fileLogCheckbox.SetToolTip( u"Tick to stream the log output to a chosen file." )
		
		bSizer2.Add( self.fileLogCheckbox, 0, wx.ALL, 5 )
		
		self.commandLineLabel = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Type command:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.commandLineLabel.Wrap( -1 )
		bSizer2.Add( self.commandLineLabel, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.logFileTextControl = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer10.Add( self.logFileTextControl, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.inputTextControl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer10.Add( self.inputTextControl, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		self.parseOutputsTimer = wx.Timer()
		self.parseOutputsTimer.SetOwner( self, parseOutputsTimerID )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.portChoice.Bind( wx.EVT_CHOICE, self.onChoseSerialPort )
		self.updatePortsButton.Bind( wx.EVT_BUTTON, self.onUpdatePorts )
		self.disconnectButton.Bind( wx.EVT_BUTTON, self.onDisconnect )
		self.baudRateTxtCtrl.Bind( wx.EVT_KILL_FOCUS, self.onUpdateBaudRate )
		self.baudRateTxtCtrl.Bind( wx.EVT_TEXT_ENTER, self.onUpdateBaudRate )
		self.readDelayTxtCtrl.Bind( wx.EVT_KILL_FOCUS, self.onUpdateReadDelay )
		self.readDelayTxtCtrl.Bind( wx.EVT_TEXT_ENTER, self.onUpdateReadDelay )
		self.clearButton.Bind( wx.EVT_BUTTON, self.onClearConsole )
		self.fileLogCheckbox.Bind( wx.EVT_CHECKBOX, self.onToggleLogFile )
		self.inputTextControl.Bind( wx.EVT_TEXT_ENTER, self.onSendInput )
		self.Bind( wx.EVT_TIMER, self.onParseOutputs, id=parseOutputsTimerID )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def onChoseSerialPort( self, event ):
		event.Skip()
	
	def onUpdatePorts( self, event ):
		event.Skip()
	
	def onDisconnect( self, event ):
		event.Skip()
	
	def onUpdateBaudRate( self, event ):
		event.Skip()
	
	
	def onUpdateReadDelay( self, event ):
		event.Skip()
	
	
	def onClearConsole( self, event ):
		event.Skip()
	
	def onToggleLogFile( self, event ):
		event.Skip()
	
	def onSendInput( self, event ):
		event.Skip()
	
	def onParseOutputs( self, event ):
		event.Skip()
	

