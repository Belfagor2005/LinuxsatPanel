#!/usr/bin/python
# -*- coding: utf-8 -*-

# import zlib, base64
# exec zlib.decompress(base64.b64decode(''))
from . import (
    _,
    add_skin_font,
    wgetsts,
    AgentRequest,
    isFHD,
    isHD,
    infourl,
    abouturl,
    xmlurl,
    descplug,
    freespace,
    CheckConn,
    installer_url,
    developer_url,
)
from .Console import Console
from .Lcn import (
    LCN,
    terrestrial,
    ReloadBouquets,
    keepiptv,
    copy_files_to_enigma2,
)
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
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
# from os import path as os_path
from datetime import datetime
import codecs
import json
import os
import re
# import shutil
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
    ePicLoad,
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


def make_request(url):
    try:
        import requests
        response = requests.get(url, verify=False, timeout=5)
        if response.status_code == 200:
            link = requests.get(url, headers={'User-Agent': AgentRequest}, timeout=10, verify=False, stream=True).text
            return link
    except ImportError:
        req = Request(url)
        req.add_header('User-Agent', 'E2 Plugin Lululla')
        response = urlopen(req, None, 10)
        link = response.read().decode('utf-8')
        response.close()
        return link
    return


def refreshPlugins():
    from Components.PluginComponent import plugins
    from Tools.Directories import SCOPE_PLUGINS, resolveFilename
    plugins.clearPluginList()
    plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))


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
            self.l.setFont(0, gFont('lsat', textfont))
        if isHD():
            self.l.setItemHeight(35)
            textfont = int(22)
            self.l.setFont(0, gFont('lsat', textfont))


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

    def __init__(self, session):
        # def __init__(self, session, data):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.data = checkGZIP(xmlurl)
        # self.data = data
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

        list.append("Backup ")
        self.titles.append("Backup")
        self.pics.append(picfold + "Backup.png")

        list.append("Bouquets ")
        self.titles.append("Bouquets ")
        self.pics.append(picfold + "Bouquets.png")

        list.append("Dvb-Usb ")
        self.titles.append("Dvb-Usb ")
        self.pics.append(picfold + "usb-tuner-drivers.png")

        list.append("Epg ")
        self.titles.append("Epg-Tools ")
        self.pics.append(picfold + "plugin-epg.png")

        list.append("Feeds Image ")
        self.titles.append("Feeds Oe2.0 ")
        self.pics.append(picfold + "Feeds2.0.png")

        list.append("Feeds Image ")
        self.titles.append("Feeds Oe2.5/2.6 ")
        self.pics.append(picfold + "Feeds2.2.png")

        list.append("Games ")
        self.titles.append("Games ")
        self.pics.append(picfold + "Game.png")

        list.append("Iptv ")
        self.titles.append("Iptv ")
        self.pics.append(picfold + "iptv-streaming.png")

        list.append("Channel List ")
        self.titles.append("Channel List")
        self.pics.append(picfold + "Channel-list.png")

        list.append("Kiddac Oe2.0 ")
        self.titles.append("Kiddac Zone Oe2.0 ")
        self.pics.append(picfold + "KiddaC1.png")

        list.append("Kiddac Oe2.5/2.6 ")
        self.titles.append("Kiddac Zone Oe2.5/2.6 ")
        self.pics.append(picfold + "KiddaC2.png")

        list.append("Lululla Zone Oe2.0 ")
        self.titles.append("Lululla Zone Oe2.0 ")
        self.pics.append(picfold + "oe2.0.png")

        list.append("Lululla Zone Oe2.5/2.6 ")
        self.titles.append("Lululla Zone Oe2.5/2.6 ")
        self.pics.append(picfold + "oe2.5-2.6.png")

        list.append("Oe2.5/2.6 Plugins ")
        self.titles.append("Oe2.5/2.6 Plugins ")
        self.pics.append(picfold + "OE2.2-Plugins.png")

        list.append("Mediaplayer-Youtube ")
        self.titles.append("MP-YT ")
        self.pics.append(picfold + "mediayou.png")

        list.append("MultiBoot ")
        self.titles.append("MultiBoot ")
        self.pics.append(picfold + "multiboot.png")

        list.append("Multimedia ")
        self.titles.append("Multimedia ")
        self.pics.append(picfold + "Multimedia.png")

        list.append("Panels Addons ")
        self.titles.append("Panels Addons ")
        self.pics.append(picfold + "Panels.png")

        list.append("Picons ")
        self.titles.append("Picons-Tools ")
        self.pics.append(picfold + "picons.png")

        list.append("Python Library ")
        self.titles.append("Python Library ")
        self.pics.append(picfold + "Library.png")

        list.append("Radio ")
        self.titles.append("Radio-Tools ")
        self.pics.append(picfold + "Radio.png")

        list.append("Skins | FHD ")
        self.titles.append("Skins | FHD")
        self.pics.append(picfold + "SkinFHD.png")

        list.append("Skins | HD ")
        self.titles.append("Skins | HD ")
        self.pics.append(picfold + "SkinHD.png")

        list.append("Skins Fhd-Hd Oe2.5/2.6 ")
        self.titles.append("Skins Oe2.5/2.6 ")
        self.pics.append(picfold + "OE2.2-Skins.png")

        list.append("Keys Tools Oe2.0 ")
        self.titles.append("SoftCam-Tools2.0 ")
        self.pics.append(picfold + "key-updater.png")

        list.append("Keys Tools Oe2.5/2.6 ")
        self.titles.append("SoftCam-Tools2.2 ")
        self.pics.append(picfold + "key-updater1.png")

        list.append("Softcams ")
        self.titles.append("SoftcamsOE2.0 ")
        self.pics.append(picfold + "SOE20.png")

        list.append("Softcams ")
        self.titles.append("SoftcamsOe2.5/2.6 ")
        self.pics.append(picfold + "SOE22.png")

        list.append("Sport ")
        self.titles.append("Sport ")
        self.pics.append(picfold + "sport.png")

        list.append("Streamlink ")
        self.titles.append("Streamlink ")
        self.pics.append(picfold + "streamlink.png")

        list.append("Utility ")
        self.titles.append("Utiliy ")
        self.pics.append(picfold + "utility.png")

        list.append("Vpn Oe2.0 ")
        self.titles.append("Vpn-Oe2.0 ")
        self.pics.append(picfold + "vpn.png")

        list.append("Weather ")
        self.titles.append("Weather-Tools ")
        self.pics.append(picfold + "weather.png")

        list.append("Weather Forecast ")
        self.titles.append("Weather-Foreca")
        self.pics.append(picfold + "weather-forecast.png")

        list.append("Webcam ")
        self.titles.append("Webcam ")
        self.pics.append(picfold + "webcam.png")

        list.append("Adult Oe2.0 ")
        self.titles.append("Adult Oe2.0 ")
        self.pics.append(picfold + "18+deb.png")

        list.append("Adult Oe2.5/2.6 ")
        self.titles.append("Adult Oe2.5/2.6 ")
        self.pics.append(picfold + "18+.png")

        list.append("Other Oe2.0 ")
        self.titles.append("Other Oe2.0 ")
        self.pics.append(picfold + "Other.png")

        list.append("Other Oe2.5/2.6 ")
        self.titles.append("Other Oe2.5/2.6 ")
        self.pics.append(picfold + "Other1.png")

        list.append(" Information ")
        self.titles.append("Information ")
        self.pics.append(picfold + "Information.png")

        list.append(" About ")
        self.titles.append("About ")
        self.pics.append(picfold + "about.png")

        self.names = list
        self.combined_data = zip(self.names, self.titles, self.pics)

        self["frame"] = MovingPixmap()
        i = 0
        while i < 20:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort'))
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     "EPGSelectActions",
                                     "EPGSelectActions",
                                     "InfoActions",],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "0": self.list_sort,
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

    def list_sort(self):  # for future
        # self.combined_data = zip(self.names, self.titles, self.pics)
        sorted_data = sorted(self.combined_data, key=lambda x: x[0])
        sorted_list, sorted_titles, sorted_pics = zip(*sorted_data)
        print("Lista ordinata:", sorted_list)
        print("Titoli ordinati:", sorted_titles)
        print("Immagini ordinate:", sorted_pics)

        # self.combined_data = sorted_data

        self.names = sorted_list
        self.titles = sorted_titles
        self.pics = sorted_pics

        self.openTest()

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
        self.session.open(LSinfo, " Information ")

    def okbuttonClick(self):
        self.idx = self.index
        if self.idx is None:
            return
        name = self.names[self.idx]
        if name == " Information ":
            self.session.open(LSinfo, name)
        elif name == " About ":
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
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
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

        list.append("CIEFP ")
        self.titles.append("CIEFP")
        self.pics.append(picfold + "ciefp.png")

        list.append("CYRUS ")
        self.titles.append("CYRUS ")
        self.pics.append(picfold + "cyrus.png")

        list.append("MANUTEK ")
        self.titles.append("MANUTEK ")
        self.pics.append(picfold + "manutek.png")

        list.append("MORPHEUS ")
        self.titles.append("MORPHEUS ")
        self.pics.append(picfold + "morpheus883.png")

        list.append("VHANNIBAL 1 ")
        self.titles.append("VHANNIBAL 1 ")
        self.pics.append(picfold + "vhannibal1.png")

        list.append("VHANNIBAL 2 ")
        self.titles.append("VHANNIBAL 2 ")
        self.pics.append(picfold + "vhannibal2.png")

        self.names = list

        self.combined_data = zip(self.names, self.titles, self.pics)

        self["frame"] = MovingPixmap()
        i = 0
        while i < 20:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort'))
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     "EPGSelectActions",
                                     "InfoActions",],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "0": self.list_sort,
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

    def list_sort(self):  # for future

        # self.combined_data = zip(self.names, self.titles, self.pics)
        sorted_data = sorted(self.combined_data, key=lambda x: x[0])
        sorted_list, sorted_titles, sorted_pics = zip(*sorted_data)
        print("Lista ordinata:", sorted_list)
        print("Titoli ordinati:", sorted_titles)
        print("Immagini ordinate:", sorted_pics)
        # self.combined_data = sorted_data

        self.names = sorted_list
        self.titles = sorted_titles
        self.pics = sorted_pics

        self.openTest()

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
        self.session.open(LSinfo, " Information ")

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
            url = 'http://github.com/morpheus883/enigma2-zipped'

        if 'vhannibal 1' in name.lower():
            url = 'https://www.vhannibal.net/asd.php'

        if 'vhannibal 2' in name.lower():
            url = 'http://sat.alfa-tech.net/upload/settings/vhannibal/'

        self.session.open(addInstall, url, name, '')


class addInstall(Screen):

    def __init__(self, session, data, name, dest):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'addInstall.xml')
        if os.path.exists('/var/lib/dpkg/info'):
            skin = os.path.join(skin_path, 'addInstall-os.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
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
                                     'cancel': self.exitnow,
                                     'red': self.exitnow,
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
        items = []
        for name, url in match:

            item = name + "###" + url
            items.append(item)
        items.sort()
        for item in items:
            name = item.split('###')[0]
            url = item.split('###')[1]

            self.names.append(name)
            self.urls.append(url)
        LPshowlist(self.names, self["list"])
        self['key_green'].show()
        self['key_yellow'].show()
        self['key_blue'].show()

    '''
    # def openTest(self):
        # print('self.xml: ', self.fxml)
        # regex = '<plugin name="(.*?)".*?url>"(.*?)"</url'
        # match = re.compile(regex, re.DOTALL).findall(self.fxml)
        # self.names = []
        # self.urls = []
        # for name, url in match:
            # self.names.append(name)
            # self.urls.append(url)
        # LPshowlist(self.names, self["list"])
        # self['key_green'].show()
        # self['key_yellow'].show()
        # self['key_blue'].show()
    '''

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

    def retfile(self, dest):
        import requests
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(dest, 'wb') as f:
                f.write(response.content)
            print(f"File {dest} scaricato correttamente.")
            return True
        else:
            print(f"Errore durante il download del file. Codice di stato: {response.status_code}")
        return False

    def okClicked(self, answer=False):
        if answer:
            dest = "/tmp"
            # cmd1 = "wget -P '" + dest + "' '" + self.url + "'"
            # cmd1 = ("wget --no-check-certificate -U '%s' -P '" + dest + "' '" + self.url + "'") % AgentRequest

            folddest = dest + '/' + self.plug
            if self.retfile(folddest):
                print('folddest:', folddest)
                # print('cmd1=', cmd1)

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
                # cmd = str(cmd1) + " && " + cmd2 + " && " + cmd3
                cmd = cmd2 + " && " + cmd3
                print('cmd2 okclicked:', cmd2)
                print('cmd okclicked:', cmd)

                title = (_("Installing %s\nPlease Wait...") % self.iname)
                self.session.open(Console, _(title), [cmd], closeOnSuccess=False)

    def downxmlpage(self):
        self.downloading = False
        r = make_request(self.fxml)
        if PY3:
            import six
            r = six.ensure_str(r)
        self.names = []
        self.urls = []
        items = []
        # a = 0
        name = url = date = ''
        try:
            # if a == 0:
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
                        name = name
                        self.downloading = True
                    item = name + "###" + url
                    items.append(item)
                    items.sort()

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
                        self.downloading = True
                    item = name + "###" + url
                    items.append(item)
                    items.sort()

            if 'manutek' in self.name.lower():
                regex = 'href="/isetting/.*?file=(.+?).zip">'
                match = re.compile(regex).findall(r)
                print('match:', match)
                for url in match:
                    name = url
                    name = name.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")
                    url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
                    self.downloading = True
                    item = name + "###" + url
                    items.append(item)
                    items.sort()

            if 'morpheus' in self.name.lower():
                regex = 'title="E2_Morph883_(.*?).zip".*?href="(.*?)"'
                # n1 = r.find('title="README.txt', 0)
                # n2 = r.find('href="#readme">', n1)
                # r = r[n1:n2]
                match = re.compile(regex).findall(r)
                print('match:', match)
                for name, url in match:
                    if url.find('.zip') != -1:
                        name = 'Morph883 ' + name
                        url = url.replace('blob', 'raw')
                        url = 'https://github.com' + url
                        self.downloading = True
                    item = name + "###" + url
                    items.append(item)
                    items.sort()

            if 'vhannibal 1' in self.name.lower():
                match = re.compile('<td><a href="(.+?)">(.+?)</a></td>.*?<td>(.+?)</td>', re.DOTALL).findall(r)
                print('match:', match)
                for url, name, date in match:
                    # name = str(name) + ' ' + date
                    name = url.replace('&#127381;', '').replace("%20", " ") + ' ' + date
                    url = "https://www.vhannibal.net/" + url
                    print('url vhan1:', url)
                    self.downloading = True
                    item = name + "###" + url
                    items.append(item)
                    items.sort()

            if 'vhannibal 2' in self.name.lower():
                regex = '<a href="Vhannibal(.*?).zip".*?right">(.*?) </td'
                match = re.compile(regex).findall(r)
                print('match:', match)
                for url, date in match:
                    if '.php' in url.lower():
                        continue
                    name = url.replace('&#127381;', '').replace("%20", " ") + ' ' + date
                    url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + '.zip'
                    print('url vhan2:', url)
                    self.downloading = True
                    # self.names.append(name.strip())
                    # self.urls.append(url.strip())

                    item = name + "###" + url
                    items.append(item)
                    items.sort()

            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]
                if name in self.names:
                    continue
                self.names.append(name.strip())
                self.urls.append(url.strip())

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
                ReloadBouquets(setx)
                self.session.open(MessageBox, _('Sorting Terrestrial channels with Lcn rules Completed'),
                                  MessageBox.TYPE_INFO,
                                  timeout=5)

    def okRun(self):
        self.session.openWithCallback(self.okRun1,
                                      MessageBox,
                                      _("Do you want to install?"),
                                      MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
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
                if keepiptv():
                    print('-----save iptv channels-----')
                '''
                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)
                '''
                '''
                # with open(dest, 'w') as f:
                    # f.write(checkGZIP(url))
                    # # f.write(make_request(url))
                    # f.close()
                '''
                '''
                # write_file(url, dest)
                # import requests
                # r = requests.get(url)
                # with open(dest, 'wb') as f:
                    # f.write(r.content)
                '''
                from six.moves.urllib.request import urlretrieve
                urlretrieve(url, dest)
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
                    os.system("rm -rf /tmp/unzipped")
                    os.system("rm -rf /tmp/settings.zip")
                    title = (_("Installing %s\nPlease Wait...") % self.name)
                    self.session.openWithCallback(self.yes, Console, title=_(title),
                                                  cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"],
                                                  closeOnSuccess=False)
                    '''
                    # self.session.openWithCallback(self.yes, Console, title=_(title),
                                                  # cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"],
                                                  # finishedCallback=self.yes,
                                                  # closeOnSuccess=False)
                    '''
            else:
                self['info'].setText(_('Settings Not Installed ...'))

    def pas(self, call=None):
        pass

    def yes(self, call=None):
        print('^^^^^^^^^^^^^^ add file to bouquet ^^^^^^^^^^^^^^')
        copy_files_to_enigma2()
        print('^^^^^^^^^^^^^^^ reloads bouquets ^^^^^^^^^^^^^^^')
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

    def exitnow(self):
        if not os.path.exists('/var/lib/dpkg/info'):
            refreshPlugins()
        self.close()


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
        self['key_green'] = Button(_('Update'))
        self['key_green'].hide()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'ChannelSelectBaseActions'], {'ok': self.close,
                                                                   'back': self.close,
                                                                   'cancel': self.close,
                                                                   'up': self.Up,
                                                                   'down': self.Down,
                                                                   'left': self.Up,
                                                                   'right': self.Down,
                                                                   'yellow': self.update_me,
                                                                   'green': self.update_dev,
                                                                   'yellow_long': self.update_dev,
                                                                   'info_long': self.update_dev,
                                                                   'infolong': self.update_dev,
                                                                   'showEventInfoPlugin': self.update_dev,
                                                                   'red': self.close}, -1)

        self.setTitle(titlex)
        self.Update = False
        self.timerz = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timerz_conn = self.timerz.timeout.connect(self.check_vers)
        else:
            self.timerz.callback.append(self.check_vers)
        self.timerz.start(200, 1)

        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/info'):
            self.timer_conn = self.timer.timeout.connect(self.startRun)
        else:
            self.timer.callback.append(self.startRun)
        self.timer.start(1000, 1)
        # self.onLayoutFinish.append(self.startRun)

    def check_vers(self):
        print('check version online')
        remote_version = '0.0'
        remote_changelog = ''
        req = Request(b64decoder(installer_url), headers={'User-Agent': AgentRequest})
        page = urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        print('self.new_version =', remote_version)
        print('self.new_changelog =', remote_changelog)
        print('currversion=', currversion)
        # if float(currversion) < float(remote_version):
        if currversion < remote_version:
            self.Update = True
            print('new version onine')
            self.mbox = self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress yellow button to start updating') % (self.new_version, self.new_changelog), MessageBox.TYPE_INFO, timeout=5)
            self['key_green'].show()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update, MessageBox, _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") % (self.new_version, self.new_changelog), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _("Congrats! You already have the latest version..."),  MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        req = Request(b64decoder(developer_url), headers={'User-Agent': AgentRequest})
        page = urlopen(req).read()
        data = json.loads(page)
        remote_date = data['pushed_at']
        strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
        remote_date = strp_remote_date.strftime('%Y-%m-%d')
        self.session.openWithCallback(self.install_update, MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date), MessageBox.TYPE_YESNO)

    def install_update(self, answer=False):
        if answer:
            self.session.open(Console, 'Upgrading...', cmdlist=('wget -q "--no-check-certificate" ' + b64decoder(installer_url) + ' -O - | /bin/sh'), finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),  MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def startRun(self):
        try:
            if self.name == " Information ":
                self.infoBox()
            elif self.name == " About ":
                url = abouturl
                ab = checkGZIP(url)
                self['list'].setText(ab)
            else:
                return
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
            python = os.popen('python -V').read().strip('\n\r')
            arc = os.popen('uname -m').read().strip('\n\r')
            ifg = os.popen('wget -qO - ifconfig.me').read().strip('\n\r')
            libs = os.popen('ls -l /usr/lib/libss*.*').read().strip('\n\r')
            if libs:
                libsssl = libs
            info = '%s V.%s\n\n' % (descplug, currversion)
            info += 'Suggested by: @masterG - @oktus - @pcd\n'
            info += 'All code was rewritten by @Lululla - Date 2024.07.20\n'
            info += 'Designs and Graphics by @oktus\n'
            info += 'Support on: Linuxsat-support.com\n\n'
            info += 'Current IP Wan: %s\nImage: %sCpu: %s\nPython Version: %s\nArch. Info: %s\nLibssl(oscam):\n%s\n' % (ifg, img, arc, python, arkFull, libsssl)
        except Exception as e:
            print("Error ", e)
            info = checkGZIP(infourl)
            print('info =: ', info)
        self['list'].setText(info)


class startLP(Screen):
    def __init__(self, session):
        self.session = session
        global _session, first
        _session = session
        first = True
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'startLP.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self["poster"] = Pixmap()
        self["version"] = Label('Wait Please... Linuxsat Panel V."' + currversion)
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.clsgo, 'cancel': self.clsgo}, -1)
        # self.texts = ["Load plugin...", "Linuxsat Panel V." + currversion, "WELCOME!!!"]
        # self.current_text_index = 0
        self.onLayoutFinish.append(self.loadDefaultImage)

    '''
    # def change_text(self):
        # import threading
        # def update_text():
            # self.current_text_index = (self.current_text_index + 1) % len(self.texts)
            # self['version'].setText(self.texts[self.current_text_index])
            # print('current_text_index:', self.current_text_index)

        # threading.Timer(2.0, update_text).start()
        # currversion = '1'
        # self.texts = ["Load plugin...", "Linuxsat Panel V." + currversion, "WELCOME!!!"]
        # self.current_text_index = 0

        # from time import sleep

        # def starters():
            # for text in self.texts:
                # print('text=', text)
                # # print('texts:', self.texts)
                # self['version'].setText(self.texts[self.current_text_index])
                # self.current_text_index = (self.current_text_index + 1) % len(self.texts)
                # # self.current_text_index += 1
                # sleep(3.0)

                # if self.current_text_index == len(self.texts) - 1:
                    # print("timer threading work!")
                    # # data = checkGZIP(xmlurl)
                    # self.session.open(LinuxsatPanel)
                    # # self.session.openWithCallback(self.passe, LinuxsatPanel)
                # self.close()
        # starters()
        '''

    def clsgo(self):
        if first is True:
            self.session.openWithCallback(self.passe, LinuxsatPanel)
        else:
            self.close()

    def passe(self, rest=None):
        global first
        first = False
        self.close()

    def loadDefaultImage(self):
        self.fldpng = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/icons/pageLogo.png".format('LinuxsatPanel'))
        self.timer = eTimer()
        if fileExists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.decodeImage)
        else:
            self.timer.callback.append(self.decodeImage)
        self.timer.start(100, True)

        self.timerx = eTimer()
        if fileExists('/var/lib/dpkg/status'):
            self.timerx_conn = self.timerx.timeout.connect(self.clsgo)
        else:
            self.timerx.callback.append(self.clsgo)
        self.timerx.start(3000, True)
        '''
        # import threading
        # def update_text():
            # self.current_text_index = (self.current_text_index + 1) % len(self.texts)
            # self['version'].setText(self.texts[self.current_text_index])
            # print('current_text_index:', self.current_text_index)
            # if self.current_text_index == len(self.texts) - 1:
                # print("timer threading work!")
                # self.clsgo()
        # threading.Timer(2.0, update_text).start()
        # self.change_text()
        '''

    def decodeImage(self):
        pixmapx = self.fldpng
        if fileExists(pixmapx):
            size = self['poster'].instance.size()
            self.picload = ePicLoad()
            self.scale = AVSwitch().getFramebufferScale()
            self.picload.setPara([size.width(), size.height(), self.scale[0], self.scale[1], 0, 1, '#00000000'])
            # _l = self.picload.PictureData.get()
            # del self.picload
            if fileExists("/var/lib/dpkg/status"):
                self.picload.startDecode(pixmapx, False)
            else:
                self.picload.startDecode(pixmapx, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()
        return


def checkGZIP(url):
    url = url
    from io import StringIO
    import gzip
    import requests
    import sys
    if sys.version_info[0] == 3:
        from urllib.request import (urlopen, Request)
        # unicode = str
        # PY3 = True
    else:
        from urllib2 import (urlopen, Request)
    hdr = {"User-Agent": AgentRequest}
    response = None
    request = Request(url, headers=hdr)
    try:
        response = urlopen(request, timeout=10)
        if response.info().get('Content-Encoding') == 'gzip':
            buffer = StringIO(response.read())
            deflatedContent = gzip.GzipFile(fileobj=buffer)
            if sys.version_info[0] == 3:
                return deflatedContent.read().decode('utf-8')
            else:
                return deflatedContent.read()
        else:
            if sys.version_info[0] == 3:
                return response.read().decode('utf-8')
            else:
                return response.read()

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except Exception as e:
        print("Unexpected error:", e)
    return None


def b64decoder(s):
    s = str(s).strip()
    import base64
    try:
        output = base64.b64decode(s)
        if PY3:
            output = output.decode('utf-8')
        return output

    except Exception:
        padding = len(s) % 4
        if padding == 1:
            print('Invalid base64 string: {}'.format(s))
            return ""
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        else:
            return ""

        output = base64.b64decode(s)
        if PY3:
            output = output.decode('utf-8')
        return output


def menustart():
    try:
        if CheckConn():
            # xml = xmlurl
            # data = checkGZIP(xml)
            # _session.open(LinuxsatPanel, data)
            _session.open(startLP)
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
        menustart()
    except:
        import traceback
        traceback.print_exc()
        pass


def menu(menuid, **kwargs):
    return [(_('Linuxsat Panel'), main, descplug, 44)] if menuid == "mainmenu" else []


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
