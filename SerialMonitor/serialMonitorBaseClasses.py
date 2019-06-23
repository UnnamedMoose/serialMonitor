# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Sep 19 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"serialMonitor", pos = wx.DefaultPosition, size = wx.Size( 600,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 600,550 ), wx.DefaultSize )

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

		bSizer2.Add( self.rawOutputCheckbox, 0, wx.ALL|wx.EXPAND, 5 )

		self.hexOutputCheckbox = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Hex output", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.hexOutputCheckbox.SetToolTip( u"Tick to show hex codes of the received bytes. Only works with \"Raw output\"." )

		bSizer2.Add( self.hexOutputCheckbox, 0, wx.ALL|wx.EXPAND, 5 )

		self.fileLogCheckbox = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Log to file", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.fileLogCheckbox.SetToolTip( u"Tick to stream the log output to a chosen file." )

		bSizer2.Add( self.fileLogCheckbox, 0, wx.ALL|wx.EXPAND, 5 )

		self.loggingLevelText = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Logging level:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.loggingLevelText.Wrap( -1 )

		bSizer2.Add( self.loggingLevelText, 0, wx.ALL|wx.EXPAND, 5 )

		loggingLevelChoiceChoices = [ u"ERROR", u"WARNING", u"INFO", u"DEBUG" ]
		self.loggingLevelChoice = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, loggingLevelChoiceChoices, 0 )
		self.loggingLevelChoice.SetSelection( 0 )
		bSizer2.Add( self.loggingLevelChoice, 0, wx.ALL, 5 )


		bSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.commandLineLabel = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Type command:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.commandLineLabel.Wrap( -1 )

		bSizer2.Add( self.commandLineLabel, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.logFileTextControl = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS|wx.BORDER_NONE )
		bSizer10.Add( self.logFileTextControl, 1, wx.EXPAND |wx.ALL, 5 )

		self.inputTextControl = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer10.Add( self.inputTextControl, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer10, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		self.parseOutputsTimer = wx.Timer()
		self.parseOutputsTimer.SetOwner( self, parseOutputsTimerID )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.fileMenu = wx.Menu()
		self.exitMenuItem = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.fileMenu.Append( self.exitMenuItem )

		self.m_menubar1.Append( self.fileMenu, u"File" )

		self.serialMenu = wx.Menu()
		self.serialMenuItem = wx.MenuItem( self.serialMenu, wx.ID_ANY, u"Edit serial details", wx.EmptyString, wx.ITEM_NORMAL )
		self.serialMenu.Append( self.serialMenuItem )

		self.m_menubar1.Append( self.serialMenu, u"Edit serial connection" )

		self.SetMenuBar( self.m_menubar1 )


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
		self.rawOutputCheckbox.Bind( wx.EVT_CHECKBOX, self.onRawOutputTicked )
		self.fileLogCheckbox.Bind( wx.EVT_CHECKBOX, self.onToggleLogFile )
		self.loggingLevelChoice.Bind( wx.EVT_CHOICE, self.onLoggingLevelChosen )
		self.inputTextControl.Bind( wx.EVT_TEXT_ENTER, self.onSendInput )
		self.Bind( wx.EVT_TIMER, self.onParseOutputs, id=parseOutputsTimerID )
		self.Bind( wx.EVT_MENU, self.onClose, id = self.exitMenuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.onEditSerialPort, id = self.serialMenuItem.GetId() )

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

	def onRawOutputTicked( self, event ):
		event.Skip()

	def onToggleLogFile( self, event ):
		event.Skip()

	def onLoggingLevelChosen( self, event ):
		event.Skip()

	def onSendInput( self, event ):
		event.Skip()

	def onParseOutputs( self, event ):
		event.Skip()


	def onEditSerialPort( self, event ):
		event.Skip()


###########################################################################
## Class serialDetailsDialog
###########################################################################

class serialDetailsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Edit serial connection details", pos = wx.DefaultPosition, size = wx.Size( 300,250 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Stop bits", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer5.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer5.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		stopBitsChoiceChoices = []
		self.stopBitsChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, stopBitsChoiceChoices, 0 )
		self.stopBitsChoice.SetSelection( 0 )
		bSizer5.Add( self.stopBitsChoice, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )

		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"Parity", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )

		bSizer51.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer51.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		parityChoiceChoices = []
		self.parityChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, parityChoiceChoices, 0 )
		self.parityChoice.SetSelection( 0 )
		bSizer51.Add( self.parityChoice, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer4.Add( bSizer51, 0, wx.EXPAND, 5 )

		bSizer52 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText52 = wx.StaticText( self, wx.ID_ANY, u"Byte size (bits)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )

		bSizer52.Add( self.m_staticText52, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer52.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		byteSizeChoiceChoices = []
		self.byteSizeChoice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, byteSizeChoiceChoices, 0 )
		self.byteSizeChoice.SetSelection( 0 )
		bSizer52.Add( self.byteSizeChoice, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer4.Add( bSizer52, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )


		bSizer13.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer11.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.okButton = wx.Button( self, wx.ID_OK, u"Okay", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.okButton, 0, wx.ALL, 5 )

		self.cancelButton = wx.Button( self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.cancelButton, 0, wx.ALL, 5 )


		bSizer11.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer13.Add( bSizer11, 1, wx.EXPAND, 5 )


		bSizer13.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		bSizer4.Add( bSizer13, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


