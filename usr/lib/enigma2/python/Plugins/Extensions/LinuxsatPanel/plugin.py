#!/usr/bin/python
# -*- coding: utf-8 -*-


# import zlib, base64
# exec zlib.decompress(base64.b64decode(''))
from . import (
    _,
    wgetsts,
    AgentRequest,
    isFHD,
    isHD,
    infourl,
    abouturl,
    xmlurl,
    descplug,
)
from .Console import Console
from . Lcn import (
    LCN,
    terrestrial,
    ReloadBouquets,
)
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryText, MultiContentEntryPixmapAlphaTest)
from Components.Pixmap import (Pixmap, MovingPixmap)
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import (SCOPE_PLUGINS, resolveFilename, fileExists)
from os import path as os_path
import codecs
import os
import re
import ssl
import sys
# import six
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    eListboxPythonMultiContent,
    eTimer,
    # getDesktop,
    gFont,
    loadPNG,
)


# ======================================================================
# LinuxsatPanel Plugin
# Coded by masterG - oktus - pcd
#
# rewritten by Lululla at 20240720
#
# ATTENTION PLEASE...
# This is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
# You must not remove the credits at
# all and you must make the modified
# code open to everyone. by Lululla
# ======================================================================

global setx
currversion = '2.0'
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('LinuxsatPanel'))
PY3 = sys.version_info.major >= 3
_session = ""
setx = 0
if PY3:
    from urllib.request import (urlopen, Request)
    unicode = str
    PY3 = True
else:
    from urllib2 import (urlopen, Request)


if sys.version_info >= (2, 7, 9):
    try:
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None


try:
    wgetsts()
except:
    pass


def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False


if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


if isFHD():
    skin_path = plugin_path + '/skins/fhd/'
    picfold = plugin_path + "/LSicons2/"
    pngx = plugin_path + "/icons2/link.png"
    blpic = picfold + "Blank.png"

if isHD():
    skin_path = plugin_path + '/skins/hd/'
    picfold = plugin_path + "/LSicons/"
    pngx = plugin_path + "/icons/link.png"
    blpic = picfold + "Blank.png"


class LPSlist(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if isFHD():
            self.l.setItemHeight(50)
            textfont = int(34)
            self.l.setFont(0, gFont('lmsat', textfont))
        if isHD():
            self.l.setItemHeight(35)
            textfont = int(22)
            self.l.setFont(0, gFont('lmsat', textfont))


def LPListEntry(name, item):
    # #fec51b
    res = [(name, item)]
    if fileExists(pngx):
        if isFHD():
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngx)))
            res.append(MultiContentEntryText(pos=(55, 0), size=(950, 50), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 7), size=(30, 30), png=loadPNG(pngx)))
            res.append(MultiContentEntryText(pos=(45, 0), size=(635, 35), font=0, text=name, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def LPshowlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(LPListEntry(name, icount))
        icount += 1
        list.setList(plist)


class LinuxsatPanel(Screen):

    def __init__(self, session, data):
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        Screen.__init__(self, session)
        self.data = data

        if isFHD():
            self.pos = []
            self.pos.append([80, 200])
            self.pos.append([310, 200])
            self.pos.append([520, 200])
            self.pos.append([730, 200])
            self.pos.append([940, 200])

            self.pos.append([80, 425])
            self.pos.append([310, 425])
            self.pos.append([520, 425])
            self.pos.append([730, 425])
            self.pos.append([940, 425])

            self.pos.append([80, 635])
            self.pos.append([310, 635])
            self.pos.append([520, 635])
            self.pos.append([730, 635])
            self.pos.append([940, 635])

            self.pos.append([80, 845])
            self.pos.append([310, 845])
            self.pos.append([520, 845])
            self.pos.append([730, 845])
            self.pos.append([940, 845])

        if isHD():
            self.pos = []
            self.pos.append([60, 125])
            self.pos.append([200, 125])
            self.pos.append([345, 125])
            self.pos.append([490, 125])
            self.pos.append([620, 125])

            self.pos.append([60, 265])
            self.pos.append([200, 265])
            self.pos.append([345, 265])
            self.pos.append([490, 265])
            self.pos.append([620, 265])

            self.pos.append([60, 405])
            self.pos.append([200, 405])
            self.pos.append([345, 405])
            self.pos.append([490, 405])
            self.pos.append([620, 405])

            self.pos.append([60, 545])
            self.pos.append([200, 545])
            self.pos.append([345, 555])
            self.pos.append([490, 545])
            self.pos.append([620, 545])

        list = []
        self.pics = []
        self.titles = []

        list.append("Backup ")  # ok
        self.titles.append("Backup")  # ok
        self.pics.append(picfold + "Backup.png")  # ok

        list.append("Bouquets ")  # ok
        self.titles.append("Bouquets ")  # ok
        self.pics.append(picfold + "Bouquets.png")  # ok

        list.append("Library ")  # ok
        self.titles.append("Library ")  # ok
        self.pics.append(picfold + "Library.png")  # ok

        list.append("Dvb-Usb ")  # ok
        self.titles.append("Dvb-Usb ")  # ok
        self.pics.append(picfold + "usb-tuner-drivers.png")  # ok

        list.append("Epg ")  # ok
        self.titles.append("Epg-Tools ")  # ok
        self.pics.append(picfold + "plugin-epg.png")  # ok

        list.append("Feeds Image ")  # OK
        self.titles.append("Feeds Oe2.0 ")  # OK
        self.pics.append(picfold + "Feeds2.0.png")  # OK

        list.append("Feeds Image ")  # OK
        self.titles.append("Feeds Oe2.5/2.6 ")  # OK
        self.pics.append(picfold + "Feeds2.2.png")  # OK

        list.append("Games ")  # ok
        self.titles.append("Games ")  # ok
        self.pics.append(picfold + "Game.png")  # ok

        list.append("Iptv ")  # ok
        self.titles.append("Iptv ")  # ok
        self.pics.append(picfold + "iptv-streaming.png")  # ok

        list.append("Channel List ")
        self.titles.append("Channel List")
        self.pics.append(picfold + "Channel-list.png")

        list.append("Kiddac Oe2.0 ")
        self.titles.append("Kiddac Zone Oe2.0 ")
        self.pics.append(picfold + "KiddaC1.png")  # ok Lululla Zone

        list.append("Kiddac Oe2.5/2.6 ")
        self.titles.append("Kiddac Zone Oe2.5/2.6 ")
        self.pics.append(picfold + "KiddaC2.png")  # ok Lululla Zone

        list.append("Lululla Zone Oe2.0 ")
        self.titles.append("Lululla Zone Oe2.0 ")
        self.pics.append(picfold + "oe2.0.png")  # ok Lululla Zone

        list.append("Lululla Zone Oe2.5/2.6 ")
        self.titles.append("Lululla Zone Oe2.5/2.6 ")
        self.pics.append(picfold + "oe2.5-2.6.png")  # ok Lululla Zone

        list.append("Oe2.5/2.6 Plugins ")
        self.titles.append("Oe2.5/2.6 Plugins ")
        self.pics.append(picfold + "OE2.2-Plugins.png")

        list.append("Mediaplayer-Youtube ")  # ok
        self.titles.append("MP-YT ")  # ok
        self.pics.append(picfold + "mediayou.png")  # ok

        list.append("MultiBoot ")  # ok
        self.titles.append("MultiBoot ")  # ok
        self.pics.append(picfold + "multiboot.png")  # ok

        list.append("Multimedia ")  # ok
        self.titles.append("Multimedia ")  # ok
        self.pics.append(picfold + "Multimedia.png")  # ok

        list.append("Panels Addons ")  # ok
        self.titles.append("Panels Addons ")  # ok
        self.pics.append(picfold + "Panels.png")  # ok

        list.append("Picons ")  # ok
        self.titles.append("Picons-Tools ")  # ok
        self.pics.append(picfold + "picons.png")  # ok

        list.append("Radio ")  # ok
        self.titles.append("Radio-Tools ")  # ok
        self.pics.append(picfold + "Radio.png")  # ok

        list.append("Skins | FHD ")  # ok
        self.titles.append("Skins | FHD")  # ok
        self.pics.append(picfold + "SkinFHD.png")  # ok

        list.append("Skins | HD ")  # ok
        self.titles.append("Skins | HD ")  # ok
        self.pics.append(picfold + "SkinHD.png")  # ok

        list.append("Skins Fhd-Hd Oe2.5/2.6 ")
        self.titles.append("Skins Oe2.5/2.6 ")
        self.pics.append(picfold + "OE2.2-Skins.png")

        list.append("Softcams ")  # ok
        self.titles.append("SoftcamsOE2.0 ")  # ok
        self.pics.append(picfold + "SOE20.png")  # ok

        list.append("Softcams ")  # ok
        self.titles.append("SoftcamsOe2.5/2.6 ")  # ok
        self.pics.append(picfold + "SOE22.png")  # ok

        list.append("Keys Tools Oe2.0 ")
        self.titles.append("SoftCam-Tools2.0 ")  # ok
        self.pics.append(picfold + "key-updater.png")  # ok

        list.append("Keys Tools Oe2.5/2.6 ")
        self.titles.append("SoftCam-Tools2.2 ")  # ok
        self.pics.append(picfold + "key-updater1.png")  # ok

        list.append("Sport ")  # ok
        self.titles.append("Sport ")  # ok
        self.pics.append(picfold + "sport.png")  # ok

        list.append("Streamlink ")  # ok
        self.titles.append("Streamlink ")  # ok
        self.pics.append(picfold + "streamlink.png")  # ok

        list.append("Utility ")  # ok
        self.titles.append("Utiliy ")  # ok
        self.pics.append(picfold + "utility.png")  # ok

        list.append("Vpn Oe2.0 ")  # ok
        self.titles.append("Vpn-Oe2.0 ")  # ok
        self.pics.append(picfold + "vpn.png")  # ok

        list.append("Weather ")  # ok
        self.titles.append("Weather-Tools ")  # OK
        self.pics.append(picfold + "weather.png")  # OK

        list.append("Forecast ")  # ok
        self.titles.append("Weather-Foreca")  # OK
        self.pics.append(picfold + "weather-forecast.png")  # OK

        list.append("Webcam ")  # ok
        self.titles.append("Webcam ")  # ok
        self.pics.append(picfold + "webcam.png")  # ok

        list.append("Adult Oe2.0 ")  # ok Lululla Zone
        self.titles.append("Adult Oe2.0 ")  # ok
        self.pics.append(picfold + "18+deb.png")  # ok

        list.append("Adult Oe2.5/2.6 ")  # ok Lululla Zone
        self.titles.append("Adult Oe2.5/2.6 ")  # ok
        self.pics.append(picfold + "18+.png")  # ok

        list.append("Other Oe2.0 ")
        self.titles.append("Other Oe2.0 ")
        self.pics.append(picfold + "Other.png")

        list.append("Other Oe2.5/2.6 ")
        self.titles.append("Other Oe2.5/2.6 ")
        self.pics.append(picfold + "Other1.png")

        list.append("Information ")  # ok
        self.titles.append("Information ")  # ok
        self.pics.append(picfold + "Information.png")  # ok

        list.append("About ")  # ok
        self.titles.append("About ")  # ok
        self.pics.append(picfold + "about.png")  # ok

        self.names = list
        self["frame"] = MovingPixmap()
        i = 0
        while i < 20:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     "EPGSelectActions",
                                     "EPGSelectActions",
                                     "InfoActions",],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        ln = len(self.names)
        self.npage = int(float(ln / 20)) + 1
        self.index = 0
        self.maxentry = len(list) - 1
        self.ipage = 1
        self.icount = 0
        self.onLayoutFinish.append(self.openTest)

    '''
    def list_sort(self):  # for future
        self.names.sort(key=lambda i: i[0], reverse=True)
        self.names.reverse()
        self.openTest()
    '''

    def paintFrame(self):
        try:
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            # information
            ifr = self.index - (20 * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('error  in paintframe: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (20 * self.ipage) - 1
            self.minentry = (self.ipage - 1) * 20

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * 20
            i1 = 0
            # while i1 < 24:
            while i1 < 20:
                self["label" + str(i1 + 1)].setText(" ")
                self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(blpic)
                i1 += 1
        self.npics = len(self.pics)
        i = 0
        i1 = 0
        self.picnum = 0
        ln = self.maxentry - (self.minentry - 1)
        while i < ln:
            idx = self.minentry + i
            # self["label" + str(i + 1)].setText(self.names[idx])
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        if not self.index <= 0:
            self.index -= 1
            # self.paintFrame()
        self.paintFrame()
        '''
        # # test
        # else:
            # self.paintFrame()
        '''

    def key_right(self):
        i = self.npics - 1
        if self.index == i:
            self.index = 0
            self.ipage = 1
            self.openTest()
        self.index += 1
        if self.index > self.maxentry:
            # # self.index = 0  # att test
            self.key_down()
        else:
            # self.index = 0
            self.paintFrame()

    def key_up(self):
        self.index = self.index - 5
        if self.index < (self.minentry):
            if self.ipage > 1:
                self.ipage = self.ipage - 1
                self.openTest()
            elif self.ipage == 1:
                return
            else:
                self.index = 0
            self.paintFrame()
        else:
            self.paintFrame()

    def key_down(self):
        self.index = self.index + 5
        if self.index > (self.maxentry):
            if self.ipage < self.npage:
                self.ipage = self.ipage + 1
                self.openTest()
            elif self.ipage == self.npage:
                self.index = 0
                self.ipage = 1
                self.openTest()
            else:
                # self.index = 0 # try add test
                self.paintFrame()
        else:
            self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        return

    def key_info(self):
        self.session.open(LSinfo, "Information ")

    def okbuttonClick(self):
        self.idx = self.index
        if self.idx is None:
            return
        name = self.names[self.idx]
        if name == "Information ":
            self.session.open(LSinfo, name)
        elif name == "About ":
            self.session.open(LSinfo, name)

        elif name == "Channel List ":
            self.session.open(LSChannel, name)

        else:
            title = self.titles[self.idx]
            n1 = self.data.find(title, 0)
            n2 = self.data.find("</plugins>", n1)
            fxml = self.data[n1:n2]
            fxml = self.data[n1:n2]
            self.session.open(addInstall, fxml, name, None)


class LSChannel(Screen):

    def __init__(self, session, name):
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        Screen.__init__(self, session)
        self.name = name

        if isFHD():
            self.pos = []
            self.pos.append([80, 200])
            self.pos.append([310, 200])
            self.pos.append([520, 200])
            self.pos.append([730, 200])
            self.pos.append([940, 200])

            self.pos.append([80, 425])
            self.pos.append([310, 425])
            self.pos.append([520, 425])
            self.pos.append([730, 425])
            self.pos.append([940, 425])

            self.pos.append([80, 635])
            self.pos.append([310, 635])
            self.pos.append([520, 635])
            self.pos.append([730, 635])
            self.pos.append([940, 635])

            self.pos.append([80, 845])
            self.pos.append([310, 845])
            self.pos.append([520, 845])
            self.pos.append([730, 845])
            self.pos.append([940, 845])

        if isHD():
            self.pos = []
            self.pos.append([60, 125])
            self.pos.append([200, 125])
            self.pos.append([345, 125])
            self.pos.append([490, 125])
            self.pos.append([620, 125])

            self.pos.append([60, 265])
            self.pos.append([200, 265])
            self.pos.append([345, 265])
            self.pos.append([490, 265])
            self.pos.append([620, 265])

            self.pos.append([60, 405])
            self.pos.append([200, 405])
            self.pos.append([345, 405])
            self.pos.append([490, 405])
            self.pos.append([620, 405])

            self.pos.append([60, 545])
            self.pos.append([200, 545])
            self.pos.append([345, 555])
            self.pos.append([490, 545])
            self.pos.append([620, 545])

        list = []
        self.pics = []
        self.titles = []

        list.append("CIEFP ")  # ok
        self.titles.append("CIEFP")  # ok
        self.pics.append(picfold + "ciefp.png")  # ok

        list.append("CYRUS ")  # ok
        self.titles.append("CYRUS ")  # ok
        self.pics.append(picfold + "cyrus.png")  # ok

        list.append("MANUTEK ")  # ok
        self.titles.append("MANUTEK ")  # ok
        self.pics.append(picfold + "manutek.png")  # ok

        list.append("MORPHEUS ")  # ok
        self.titles.append("MORPHEUS ")  # ok
        self.pics.append(picfold + "morpheus883.png")  # ok

        list.append("VHANNIBAL 1 ")  # OK
        self.titles.append("VHANNIBAL 1 ")  # OK
        self.pics.append(picfold + "vhannibal1.png")  # OK

        list.append("VHANNIBAL 2 ")  # OK
        self.titles.append("VHANNIBAL 2 ")  # OK
        self.pics.append(picfold + "vhannibal2.png")  # OK

        self.names = list
        self["frame"] = MovingPixmap()
        i = 0
        while i < 20:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     "EPGSelectActions",
                                     "EPGSelectActions",
                                     "InfoActions",],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        ln = len(self.names)
        self.npage = int(float(ln / 20)) + 1
        self.index = 0
        self.maxentry = len(list) - 1
        self.ipage = 1
        self.icount = 0
        self.onLayoutFinish.append(self.openTest)

    '''
    def list_sort(self):  # for future
        self.names.sort(key=lambda i: i[0], reverse=True)
        self.names.reverse()
        self.openTest()
    '''

    def paintFrame(self):
        try:
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            # information
            ifr = self.index - (20 * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('error  in paintframe: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (20 * self.ipage) - 1
            self.minentry = (self.ipage - 1) * 20

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * 20
            i1 = 0
            # while i1 < 24:
            while i1 < 20:
                self["label" + str(i1 + 1)].setText(" ")
                self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(blpic)
                i1 += 1
        self.npics = len(self.pics)
        i = 0
        i1 = 0
        self.picnum = 0
        ln = self.maxentry - (self.minentry - 1)
        while i < ln:
            idx = self.minentry + i
            # self["label" + str(i + 1)].setText(self.names[idx])
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        if not self.index <= 0:
            self.index -= 1
            # self.paintFrame()
        self.paintFrame()
        '''
        # ###test
        # else:
            # self.paintFrame()
        '''

    def key_right(self):
        i = self.npics - 1
        if self.index == i:
            self.index = 0
            self.ipage = 1
            self.openTest()
        self.index += 1
        if self.index > self.maxentry:
            # # self.index = 0  # att test
            self.key_down()
        else:
            # self.index = 0
            self.paintFrame()

    def key_up(self):
        self.index = self.index - 5
        if self.index < (self.minentry):
            if self.ipage > 1:
                self.ipage = self.ipage - 1
                self.openTest()
            elif self.ipage == 1:
                return
            else:
                self.index = 0
            self.paintFrame()
        else:
            self.paintFrame()

    def key_down(self):
        self.index = self.index + 5
        if self.index > (self.maxentry):
            if self.ipage < self.npage:
                self.ipage = self.ipage + 1
                self.openTest()
            elif self.ipage == self.npage:
                self.index = 0
                self.ipage = 1
                self.openTest()
            else:
                # self.index = 0 # try add test
                self.paintFrame()
        else:
            self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        return

    def key_info(self):
        self.session.open(LSinfo, "Information ")

    def okbuttonClick(self):
        self.idx = self.index
        if self.idx is None:
            return
        name = self.names[self.idx]

        if 'ciefp' in name.lower():
            url = 'https://github.com/ciefp/ciefpsettings-enigma2-zipped'

        if 'cyrus' in name.lower():
            url = 'http://www.cyrussettings.com/Set_29_11_2011/Dreambox-IpBox/Config.xml'

        if 'manutek' in name.lower():
            url = 'http://www.manutek.it/isetting/index.php'

        if 'morpheus' in name.lower():
            url = 'https://github.com/morpheus883/enigma2-zipped'

        if 'vhannibal 1' in name.lower():
            url = 'https://www.vhannibal.net/asd.php'

        if 'vhannibal 2' in name.lower():
            url = 'http://sat.alfa-tech.net/upload/settings/vhannibal/'

        self.session.open(addInstall, url, name, '')


class addInstall(Screen):

    def __init__(self, session, data, name, dest):

        skin = os.path.join(skin_path, 'addInstall.xml')
        if os.path.exists('/var/lib/dpkg/info'):
            skin = os.path.join(skin_path, 'addInstall-os.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        Screen.__init__(self, session)
        self.fxml = str(data)
        self.name = name
        self.dest = dest
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Install'))
        self['key_yellow'] = Button(_('Remove'))
        self['key_blue'] = Button(_('Restart enigma'))
        self['key_yellow'].hide()
        self['key_blue'].hide()
        self['key_green'].hide()

        self.LcnOn = False
        if os.path.exists('/etc/enigma2/lcndb'):
            self['key_yellow'].show()
            self['key_yellow'] = Button('Lcn')
            self.LcnOn = True
            print('LcnOn = True')

        self.list = []
        self["list"] = LPSlist([])
        self['fspace'] = Label()
        self['fspace'].setText(_('Please Wait...'))
        self['info'] = Label()
        self['info'].setText(_('Load Category...'))
        self.icount = 0
        self.downloading = False
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'],
                                    {'ok': self.message,
                                     'green': self.message,
                                     'cancel': self.close,
                                     'red': self.close,
                                     'blue': self.restart,
                                     'yellow': self.remove}, -2)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.getfreespace)
        else:
            self.timer.callback.append(self.getfreespace)
        self.timer.start(1000, 1)

        if self.dest is not None:
            self.onLayoutFinish.append(self.downxmlpage)
        else:
            self.onLayoutFinish.append(self.openTest)

    def getfreespace(self):
        try:
            self['info'].setText(_('Category: ') + self.name)
            fspace = freespace()
            self['fspace'].setText(str(fspace))
        except Exception as e:
            print(e)

    def openTest(self):
        print('self.xml: ', self.fxml)
        regex = '<plugin name="(.*?)".*?url>"(.*?)"</url'
        match = re.compile(regex, re.DOTALL).findall(self.fxml)
        self.names = []
        self.urls = []
        for name, url in match:
            self.names.append(name)
            self.urls.append(url)
        LPshowlist(self.names, self["list"])
        self['key_green'].show()
        self['key_yellow'].show()
        self['key_blue'].show()

    def message(self):
        if self.dest is not None:
            print('go okRun')
            self.okRun()
        else:
            idx = self["list"].getSelectionIndex()
            self.url = self.urls[idx]
            n1 = self.url.rfind("/")
            self.plug = self.url[(n1 + 1):]
            self.iname = ''
            if ".deb" in self.plug:
                if not os.path.exists('/var/lib/dpkg/info'):
                    self.session.open(MessageBox,
                                      _('Unknow Image!'),
                                      MessageBox.TYPE_INFO,
                                      timeout=5)
                    return
                n2 = self.plug.find("_", 0)
                self.iname = self.plug[:n2]

            if ".ipk" in self.plug:
                if os.path.exists('/var/lib/dpkg/info'):
                    self.session.open(MessageBox,
                                      _('Unknow Image!'),
                                      MessageBox.TYPE_INFO,
                                      timeout=5)
                    return
                n2 = self.plug.find("_", 0)
                self.iname = self.plug[:n2]
            elif ".zip" in self.plug:
                self.iname = self.plug
            elif ".tar" in self.plug or ".gz" in self.plug or "bz2" in self.plug:
                self.iname = self.plug

            self.session.openWithCallback(self.okClicked,
                                          MessageBox, _("Do you want to install %s?") % self.iname,
                                          MessageBox.TYPE_YESNO)

    def okClicked(self, answer=False):
        if answer:
            dest = "/tmp"
            # cmd1 = "wget -P '" + dest + "' '" + self.url + "'"
            cmd1 = ("wget --no-check-certificate -U '%s' -P '" + dest + "' '" + self.url + "'") % AgentRequest
            if ".deb" in self.plug:
                cmd2 = "dpkg -i '/tmp/" + self.plug + "'"
            if ".ipk" in self.plug:
                cmd2 = "opkg install --force-overwrite '/tmp/" + self.plug + "'"
            elif ".zip" in self.plug:
                cmd2 = "unzip -o -q '/tmp/" + self.plug + "' -d /"
            elif ".tar" in self.plug and "gz" in self.plug:
                cmd2 = "tar -xvf '/tmp/" + self.plug + "' -C /"
            elif ".bz2" in self.plug and "gz" in self.plug:
                cmd2 = "tar -xjvf '/tmp/" + self.plug + "' -C /"
            cmd3 = "rm '/tmp/" + self.plug + "'"
            cmd = cmd1 + " && " + cmd2 + " && " + cmd3
            title = (_("Installing %s\nPlease Wait...") % self.iname)
            self.session.open(Console, _(title), [cmd], closeOnSuccess=False)

    def downxmlpage(self):
        self.downloading = False
        data = checkGZIP(self.fxml)
        r = data
        self.names = []
        self.urls = []
        try:
            if 'ciefp' in self.name.lower():
                n1 = r.find('title="README.txt', 0)
                n2 = r.find('href="#readme">', n1)
                r = r[n1:n2]
                regex = 'title="ciefp-E2-(.*?).zip".*?href="(.*?)"'
                match = re.compile(regex).findall(r)
                print('match:', match)
                for name, url in match:
                    if url.find('.zip') != -1:
                        url = url.replace('blob', 'raw')
                        url = 'https://github.com' + url
                        self.names.append(name.strip())
                        self.urls.append(url.strip())
                        self.downloading = True
            if 'cyrus' in self.name.lower():
                n1 = r.find('name="Sat">', 0)
                n2 = r.find("/ruleset>", n1)
                r = r[n1:n2]
                regex = 'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
                match = re.compile(regex).findall(r)
                print('match:', match)
                for name, url, date in match:
                    if url.find('.zip') != -1:
                        if 'ddt' in name.lower():
                            continue
                        if 'Sat' in name.lower():
                            continue
                        name = name + ' ' + date
                        self.names.append(name.strip())
                        self.urls.append(url.strip())
                        self.downloading = True

            if 'manutek' in self.name.lower():
                regex = 'href="/isetting/.*?file=(.+?).zip">'
                match = re.compile(regex).findall(r)
                print('match:', match)
                for url in match:
                    name = url
                    url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
                    name = name.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")
                    self.urls.append(url.strip())
                    self.names.append(name.strip())
                    self.downloading = True

            if 'morpheus' in self.name.lower():
                regex = 'name":"E2_Morph883_(.*?).zip".*?path":"(.*?)"'
                match = re.compile(regex).findall(r)
                # print('match:', match)
                for name, url in match:
                    if url.find('.zip') != -1:
                        url = url.replace('blob', 'raw')
                        url = 'https://github.com/morpheus883/enigma2-zipped/raw/master/' + url
                        name = 'Morph883 ' + name
                        self.names.append(name.strip())
                        self.urls.append(url.strip())
                        self.downloading = True

            if 'vhannibal 1' in self.name.lower():
                match = re.compile('<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL).findall(data)
                # print('match:', match)
                for url, name, date in match:
                    name = name.replace('Vhannibal', '').replace('&#127381;', '') + ' ' + date
                    url = "https://www.vhannibal.net/" + url
                    self.names.append(name.strip())
                    self.urls.append(url.strip())
                    self.downloading = True

            if 'vhannibal 2' in self.name.lower():
                regex = '<a href="Vhannibal(.*?).zip".*?right">(.*?) </td'
                match = re.compile(regex).findall(data)
                # print('match:', match)
                for url, date in match:
                    if '.php' in url.lower():
                        continue
                    name = url
                    name = name.replace('&#127381;', '').replace("%20", " ") + ' ' + date
                    url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + '.zip'
                    self.names.append(name.strip())
                    self.urls.append(url.strip())
                    self.downloading = True

            self['key_green'].show()
            LPshowlist(self.names, self["list"])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def Lcn(self):
        setx = 0
        if self.LcnOn:
            lcn = LCN()
            lcn.read()
            if len(lcn.lcnlist) >= 1:
                lcn.writeBouquet()
                lcn.ReloadBouquets(setx)
                self.session.open(MessageBox, _('Sorting Terrestrial channels with Lcn rules Completed'),
                                  MessageBox.TYPE_INFO,
                                  timeout=5)

    def okRun(self):
        self.session.openWithCallback(self.okRun1,
                                      MessageBox,
                                      _("Do you want to install?"),
                                      MessageBox.TYPE_YESNO)

    def okRun1(self, answer):
        dest = "/tmp/settings.zip"
        if answer:
            global setx
            # setx = 0
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                '''
                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)
                '''
                with open(dest, 'wb') as f:
                    f.write(checkGZIP(url))
                    f.close()

                if os.path.exists(dest) and '.zip' in dest:
                    fdest1 = "/tmp/unzipped"
                    fdest2 = "/etc/enigma2"
                    if os.path.exists("/tmp/unzipped"):
                        os.system('rm -rf /tmp/unzipped')
                    os.makedirs('/tmp/unzipped')
                    cmd2 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
                    os.system(cmd2)
                    for root, dirs, files in os.walk(fdest1):
                        for name in dirs:
                            self.namel = name
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    os.system('rm -rf /etc/enigma2/*.del')
                    os.system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)

                    title = (_("Installing %s\nPlease Wait...") % self.name)
                    self.session.openWithCallback(self.yes, Console, title=_(title),
                                                  cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"],
                                                  closeOnSuccess=False)

            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def yes(self):
        ReloadBouquets(setx)

    def remove(self):
        if self.dest is not None:
            self.Lcn()
        else:
            self.session.openWithCallback(self.removenow,
                                          MessageBox,
                                          _("Do you want to remove?"),
                                          MessageBox.TYPE_YESNO)

    def removenow(self, answer=False):
        if answer:
            idx = self["list"].getSelectionIndex()
            url = self.urls[idx]
            n1 = url.rfind("/")
            ipk = url[(n1 + 1):]
            if ".zip" in ipk:
                return
            n2 = ipk.find("_", 0)
            self.iname = ipk[:n2]
            cmd = "opkg remove '" + self.iname + "'"
            title = (_("Removing %s") % self.iname)
            self.session.open(Console, _(title), [cmd])

    def restart(self):
        self.session.openWithCallback(self.restartnow,
                                      MessageBox,
                                      _("Do you want to restart Gui Interface?"),
                                      MessageBox.TYPE_YESNO)

    def restartnow(self, answer=False):
        if answer:
            self.session.open(TryQuitMainloop, 3)


class LSinfo(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LSinfo.xml')
        if os.path.exists('/var/lib/dpkg/info'):
            skin = os.path.join(skin_path, 'LSinfo-os.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        titlex = descplug + ' V.' + currversion
        self.name = name
        info = _('Please Wait...')
        self.labeltext = ('')
        self['list'] = ScrollLabel(info)
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions'], {'cancel': self.close,
                                                           'red': self.close,
                                                           'ok': self.ok,
                                                           'up': self.Up,
                                                           'down': self.Down,
                                                           'left': self.Up,
                                                           'right': self.Down,
                                                           }, -1)

        self.setTitle(titlex)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.startRun)
        else:
            self.timer.callback.append(self.startRun)
        self.timer.start(1000, 1)
        # self.onLayoutFinish.append(self.startRun)

    def startRun(self):
        try:
            if self.name == "Information ":
                self.infoBox()
            else:
                url = abouturl
                ab = checkGZIP(url)
                self['list'].setText(ab)
        except Exception as e:
            print(e)
            self['list'].setText(_('Unable to download updates!'))

    def cancel(self):
        self.close()

    def ok(self):
        self.close()

    def Down(self):
        self['list'].pageDown()

    def Up(self):
        self['list'].pageUp()

    def arckget(self):
        zarcffll = ''
        try:
            if os.path.exists('/var/lib/dpkg/info'):
                zarcffll = os.popen('dpkg --print-architecture | grep -iE "arm|aarch64|mips|cortex|sh4|sh_4"').read().strip('\n\r')
            else:
                zarcffll = os.popen('opkg print-architecture | grep -iE "arm|aarch64|mips|cortex|h4|sh_4"').read().strip('\n\r')
        except Exception as e:
            print("Error ", e)
        return str(zarcffll)

    def infoBox(self):
        try:
            arkFull = ''
            if self.arckget():
                arkFull = self.arckget()
                print('arkget= ', arkFull)
            img = os.popen('cat /etc/issue').read().strip('\n\r')
            img = img.replace('\\l', '')
            arc = os.popen('uname -m').read().strip('\n\r')
            ifg = os.popen('wget -qO - ifconfig.me').read().strip('\n\r')
            libs = os.popen('ls -l /usr/lib/libss*.*').read().strip('\n\r')
            if libs:
                libsssl = libs
            info = '%s V.%s\n\n' % (descplug, currversion)
            info += 'Suggested by: @masterG - @oktus - @pcd\n'
            info += 'All code was rewritten by @Lululla maintener\n'
            info += 'Date 2024.07.20\n'
            info += 'Designs and Graphics by @oktus\n'
            info += 'Support on: Linuxsat-support.com\n\n'
            info += 'Current IP Wan: %s\nImage: %sCpu: %s\nArch. Info: %s\nLibssl(oscam):\n%s\n' % (ifg, img, arc, arkFull, libsssl)
        except Exception as e:
            print("Error ", e)
            info = checkGZIP(infourl)
            print('info =: ', info)
        self['list'].setText(info)


def add_skin_font():
    from enigma import addFont
    FNTPath = os_path.join(plugin_path + "/fonts")
    # addFont(filename, name, scale, isReplacement, render)
    addFont((FNTPath + '/ls-regular.ttf'), 'lsat', 100, 1)
    addFont((FNTPath + '/ls-medium.ttf'), 'lmsat', 100, 1)
    addFont((FNTPath + '/ls-medium.ttf'), 'lbsat', 100, 1)


def checkGZIP(url):
    from io import StringIO
    import gzip
    import requests
    hdr = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'}
    response = None
    request = Request(url, headers=hdr)
    try:
        response = urlopen(request, timeout=10)
        if response.info().get('Content-Encoding') == 'gzip':
            buffer = StringIO(response.read())
            deflatedContent = gzip.GzipFile(fileobj=buffer)
            if PY3:
                return deflatedContent.read().decode('utf-8')
            else:
                return deflatedContent.read()
        else:
            if PY3:
                return response.read().decode('utf-8')
            else:
                return response.read()
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except Exception as e:
        print("Unexpected error:", e)
    return None


def CheckConn(host='www.google.com', port=80, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print('error: ', e)
        return False


# KiddaC code
def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


# KiddaC code
def freespace():
    try:
        stat = os.statvfs('/')
        free_bytes = stat.f_bfree * stat.f_bsize
        total_bytes = stat.f_blocks * stat.f_bsize
        fspace = convert_size(float(free_bytes))
        total_space = convert_size(float(total_bytes))
        spacestr = _("Free Space:") + " " + str(fspace) + " " + _("of") + " " + str(total_space)
        return spacestr
    except Exception as e:
        print("Error getting disk space:", e)
        return _("Free Space:") + " -?- " + _("of") + " -?-"


def menustart():
    try:
        if CheckConn():
            xml = xmlurl
            data = checkGZIP(xml)
            _session.open(LinuxsatPanel, data)
        else:
            _session.open(MessageBox,
                          _('Check Connection!'),
                          MessageBox.TYPE_INFO,
                          timeout=5)
    except:
        import traceback
        traceback.print_exc()
        pass


def main(session, **kwargs):
    try:
        global _session
        _session = session
        # add_skin_font()
        menustart()
    except:
        import traceback
        traceback.print_exc()
        pass


def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        from Tools.BoundFunction import boundFunction
        return [(_('Linuxsat Panel'),
                 boundFunction(main, showExtentionMenuOption=True),
                 descplug,
                 -1)]
    else:
        return []


def Plugins(**kwargs):
    add_skin_font()
    return [PluginDescriptor(name="Linuxsat Panel",
                             description=descplug,
                             icon="LinuxsatPanel.png",
                             where=PluginDescriptor.WHERE_PLUGINMENU,
                             fnc=main),
            PluginDescriptor(name="Linuxsat Panel",
                             description=descplug,
                             where=PluginDescriptor.WHERE_MENU,
                             fnc=menu)]
