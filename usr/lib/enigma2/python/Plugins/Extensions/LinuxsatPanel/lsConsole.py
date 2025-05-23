#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
# ═════════════════════════════════════════════════════════════════════
# 📦 LinuxsatPanel Plugin
#
# 👨‍💻 Original Developers: RAED & mfaraj57 &  (c) 2018
# ✍️ Rewritten by: Lululla (2024-07-20)
#
# ⚖️ License: GNU General Public License (v2 or later)
#    You must NOT remove credits and must share modified code.
# ═════════════════════════════════════════════════════════════════════
from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from enigma import getDesktop
import sys
import codecs
import os

plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('LinuxsatPanel'))
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def getDesktopSize():
	s = getDesktop(0).size()
	return (s.width(), s.height())


def isHD():
	desktopSize = getDesktopSize()
	return desktopSize[0] == 1280


if isHD():
	skin_path = plugin_path + '/skins/hd'
else:
	skin_path = plugin_path + '/skins/fhd'


class lsConsole(Screen):

	def __init__(self, session, title='Linuxsat-support Console', cmdlist=None, finishedCallback=None, closeOnSuccess=False, showStartStopText=True, skin=None):
		Screen.__init__(self, session)
		self.finishedCallback = finishedCallback
		self.closeOnSuccess = closeOnSuccess
		self.showStartStopText = showStartStopText

		skin = os.path.join(skin_path, 'lsConsole.xml')
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()

		self.errorOcurred = False
		self['text'] = ScrollLabel('')
		self['key_red'] = Label('Cancel')
		self['key_green'] = Label('Hide/Show')
		self['key_blue'] = Label('Restart')

		self["actions"] = ActionMap(
			["WizardActions", "DirectionActions", "ColorActions"],
			{
				"ok": self.cancel,
				"up": self["text"].pageUp,
				"down": self["text"].pageDown,
				"red": self.cancel,
				"green": self.toggleHideShow,
				"blue": self.restartenigma,
				"exit": self.cancel,
			},
			-1
		)

		self.newtitle = title == 'Linuxsat-support Console' and ('Console') or title
		self.cmdlist = isinstance(cmdlist, list) and cmdlist or [cmdlist]
		self.cancel_msg = None
		self.onShown.append(self.updateTitle)
		self.container = eConsoleAppContainer()
		self.run = 0
		self.finished = False
		try:
			self.container.appClosed.append(self.runFinished)
			self.container.dataAvail.append(self.dataAvail)
		except:
			self.container.appClosed_conn = self.container.appClosed.connect(self.runFinished)
			self.container.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
		self.onLayoutFinish.append(self.startRun)

	def updateTitle(self):
		self.setTitle(self.newtitle)

	def startRun(self):
		if self.showStartStopText:
			self['text'].setText('Execution progress\n\n')
		print('[Console] executing in run', self.run, ' the command:', self.cmdlist[self.run])
		print("[Console] Executing command:", self.cmdlist[self.run])  # Aggiungi questo print
		if self.container.execute(self.cmdlist[self.run]):
			self['text'].setText(self.cmdlist[self.run])
			self.runFinished(-1)

	def runFinished(self, retval):
		if retval:
			self.errorOcurred = True
			self.show()
		self.run += 1
		if self.run != len(self.cmdlist):
			if self.container.execute(self.cmdlist[self.run]):
				self.runFinished(-1)
		else:
			self.show()
			self.finished = True
			"""
			# try:
				# lastpage = self['text'].isAtLastPage()
			# except:
				# lastpage = self['text']
			"""
			if self.cancel_msg:
				self.cancel_msg.close()
			if self.showStartStopText:
				self['text'].appendText('Execution finished!!')
			if self.finishedCallback is not None:
				self.finishedCallback()
			if not self.errorOcurred and self.closeOnSuccess:
				self.closeConsole()
			else:
				self['text'].appendText('\nPress OK or Exit to abort!')
				self['key_red'].setText('Exit')
				self['key_green'].setText('')

	def toggleHideShow(self):
		if self.finished:
			return
		if self.shown:
			self.hide()
		else:
			self.show()

	def cancel(self):
		if self.finished:
			self.closeConsole()
		else:
			self.cancel_msg = self.session.openWithCallback(self.cancelCallback, MessageBox, 'Cancel execution?', type=MessageBox.TYPE_YESNO, default=False)

	def cancelCallback(self, ret=None):
		self.cancel_msg = None
		if ret:
			try:
				self.container.appClosed.remove(self.runFinished)
				self.container.dataAvail.remove(self.dataAvail)
			except:
				self.container.appClosed_conn = None
				self.container.dataAvail_conn = None
			self.container.kill()
			self.close()

	def closeConsole(self):
		if self.finished:
			try:
				self.container.appClosed.remove(self.runFinished)
				self.container.dataAvail.remove(self.dataAvail)
			except:
				self.container.appClosed_conn = None
				self.container.dataAvail_conn = None
			self.close()
		else:
			self.show()

	def dataAvail(self, str):
		if PY3:
			data = str.decode()
		else:
			data = str
		print("[Console] Data received: ", data)
		self['text'].appendText(data)

	def restartenigma(self):
		from Screens.Standby import TryQuitMainloop
		self.session.open(TryQuitMainloop, 3)
