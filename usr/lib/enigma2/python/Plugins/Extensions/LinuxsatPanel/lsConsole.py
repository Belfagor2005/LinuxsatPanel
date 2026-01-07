#!/usr/bin/python
# -*- coding: utf-8 -*-
# RAED & mfaraj57 &  (c) 2018
# mod Lululla 20251113

from __future__ import print_function
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
import gettext
_ = gettext.gettext

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

    def __init__(self, session, title='Linuxsat-support Console', cmdlist=None, finishedCallback=None, closeOnSuccess=False, showStartStopText=True, skin=None, callback=None):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.callback = callback  # Add this
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
            ["WizardActions", "DirectionActions", 'ColorActions'],
            {
                "ok": self.cancel,
                "up": self["text"].pageUp,
                "down": self["text"].pageDown,
                "red": self.cancel,
                "green": self.toggleHideShow,
                "blue": self.restartenigma,
                "exit": self.cancel,
            }, -1
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
            self['text'].setText(_('Execution progress\n\n'))
        print('[Console] executing in run', self.run, ' the command:', self.cmdlist[self.run])
        print("[Console] Executing command:", self.cmdlist[self.run])
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
            return  # Exit early

        # All commands have finished
        self.show()
        self.finished = True
        
        if self.cancel_msg:
            self.cancel_msg.close()
            
        if self.showStartStopText:
            self['text'].appendText('Execution finished!!')
        
        if self.callback:
            self.callback(not self.errorOcurred)
        
        if self.finishedCallback:
            self.finishedCallback()
        
        if self.errorOcurred or not self.closeOnSuccess:
            self['text'].appendText('\nPress OK or Exit to abort!')
            self['key_red'].setText('Exit')
            self['key_green'].setText('')
        else:
            self.closeConsole()

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
            self.cancel_msg = self.session.openWithCallback(self.cancelCallback, MessageBox, _('Cancel execution?'), type=MessageBox.TYPE_YESNO, default=False)

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

    def dataAvail(self, data):
        try:
            if isinstance(data, str):
                text = data
            else:
                try:
                    text = data.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        text = data.decode('latin-1')
                    except:
                        try:
                            text = data.decode('utf-8', errors='ignore')
                        except:
                            text = data.decode('utf-8', errors='replace')

            print("[Console] Data received: ", text)
            self['text'].appendText(text)

        except Exception as e:
            print("Error in dataAvail:", str(e))
            try:
                if isinstance(data, bytes):
                    self['text'].appendText(data.decode('utf-8', errors='ignore'))
                else:
                    self['text'].appendText(str(data))
            except:
                self['text'].appendText("Data output")

    def restartenigma(self):
        from Screens.Standby import TryQuitMainloop
        self.session.open(TryQuitMainloop, 3)
