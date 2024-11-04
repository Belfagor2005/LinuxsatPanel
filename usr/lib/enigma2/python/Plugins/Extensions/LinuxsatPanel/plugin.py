#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import (
    _,
    AgentRequest,
    CheckConn,
    # abouturl,
    add_skin_font,
    b64decoder,
    checkGZIP,
    descplug,
    developer_url,
    fetch_url,
    freespace,
    infourl,
    installer_url,
    isWQHD,
    isFHD,
    isHD,
    RequestUrl,
    make_request,
    # lngx,
    refreshPlugins,
    xmlurl,
    HALIGN,
)
from .lsConsole import lsConsole
from .LCNScanner.plugin import LCNScanner
from .LCNScanner.Lcn import (
    # LCN,
    # LCNBuildHelper,
    ReloadBouquets,
    copy_files_to_enigma2,
    keepiptv,
    terrestrial,
)

from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (MultiContentEntryText, MultiContentEntryPixmapAlphaTest)
from Components.Pixmap import (Pixmap, MovingPixmap)
from Components.PluginComponent import plugins
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import (SCOPE_PLUGINS, resolveFilename, fileExists)
from datetime import datetime
import codecs
import json
import os
import re
import ssl
import sys
import shutil
import six
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    RT_HALIGN_RIGHT,
    eListboxPythonMultiContent,
    ePicLoad,
    eTimer,
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
global HALIGN
global setx
global skin_path
global has_dpkg

currversion = '2.5.5'

plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('LinuxsatPanel'))

PY3 = sys.version_info.major >= 3

skin_path = ''

_session = None

has_dpkg = False

setx = 0


if os.path.exists("/usr/bin/apt-get"):
    has_dpkg = True


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


if sys.version_info[0] >= 3:
    import html

    def decode_html(text):
        return html.unescape(text)
else:
    from HTMLParser import HTMLParser
    html_parser = HTMLParser()

    def decode_html(text):
        return html_parser.unescape(text)


def create_ssl_context():
    try:
        return ssl.create_default_context()
    except Exception:
        return None


def ssl_urlopen(url):
    sslContext = create_ssl_context()

    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except ImportError:
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


# init path
if isWQHD() or isFHD():
    skin_path = plugin_path + '/skins/fhd'
    picfold = plugin_path + "/LSicons2/"
    pngx = plugin_path + "/icons2/link.png"
    blpic = picfold + "Blank.png"
else:
    skin_path = plugin_path + '/skins/hd'
    picfold = plugin_path + "/LSicons/"
    pngx = plugin_path + "/icons/link.png"
    blpic = picfold + "Blank.png"


# menulist
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
    res = [(name, item)]
    if fileExists(pngx):
        if isFHD():
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 5), size=(40, 40), png=loadPNG(pngx)))
            res.append(MultiContentEntryText(pos=(55, 0), size=(920, 50), font=0, text=name, flags=HALIGN | RT_VALIGN_CENTER))
        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 7), size=(30, 30), png=loadPNG(pngx)))
            res.append(MultiContentEntryText(pos=(45, 0), size=(615, 35), font=0, text=name, flags=HALIGN | RT_VALIGN_CENTER))
    return res


def LPshowlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(LPListEntry(name, icount))
        icount += 1
        list.setList(plist)


# sortlist
class ListSortUtility:
    @staticmethod
    def list_sort(names, titles, pics, urls):
        combined_data = zip(names, titles, pics, urls)
        sorted_data = sorted(combined_data, key=lambda x: x[0])
        sorted_list, sorted_titles, sorted_pics, sorted_urls = zip(*sorted_data)
        return sorted_list, sorted_titles, sorted_pics, sorted_urls


# pixmaplist
def get_positions(resolution):
    positions = []
    if resolution == "FHD":
        positions = [
            [100, 210], [310, 210], [525, 210], [735, 210], [940, 210],
            [100, 420], [310, 420], [525, 420], [735, 420], [940, 420],
            [100, 635], [310, 635], [525, 635], [735, 635], [940, 635],
            [100, 835], [310, 835], [525, 835], [735, 835], [940, 835]
        ]
    elif resolution == "HD":
        positions = [
            [65, 135], [200, 135], [345, 135], [485, 135], [620, 135],
            [65, 270], [200, 270], [345, 270], [485, 270], [620, 270],
            [65, 405], [200, 405], [345, 405], [485, 405], [620, 405],
            [65, 540], [200, 540], [345, 540], [485, 540], [620, 540]
        ]
    return positions


# def add_menu_item(menu_list, titles, pics, name, pic):
    # menu_list.append((name, titles, pic, ""))

def add_menu_item(menu_list, titles, pics, urls, title, pic_name):
    menu_list.append(title)
    titles.append(title.strip())
    pics.append(picfold + pic_name)
    urls.append("")  # Aggiungi una stringa vuota per l'URL


# def add_menu_item(menu_list, titles, pics, title, pic_name):
    # menu_list.append(title)
    # titles.append(title.strip())
    # pics.append(picfold + pic_name)


def add_menu_item_with_url(menu_list, titles, pics, urls, title, pic_name, url):
    menu_list.append(title)
    titles.append(title.strip())
    pics.append(picfold + pic_name)
    urls.append(url)


class LinuxsatPanel(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        if isWQHD() or isFHD():
            self.pos = get_positions("FHD")
        elif isHD():
            self.pos = get_positions("HD")

        self.data = checkGZIP(xmlurl)
        menu_list = []
        self.titles = []
        self.pics = []
        self.urls = []

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Backup ", "Backup.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Bouquets ", "Bouquets.png")

        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Channel List ", "Channel-list.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "DvbUsb Tuners Drivers", "usb-tuner-drivers.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Epg ", "plugin-epg.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Feeds Image Oe2.0 ", "Feeds2.0.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Feeds Image DreamOs ", "Feeds2.2.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Games ", "Game.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Iptv ", "iptv-streaming.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Kiddac Oe2.0 ", "KiddaC1.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Kiddac DreamOs ", "KiddaC2.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Lululla Zone Oe2.0 ", "oe2.0.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Lululla Zone DreamOs ", "oe2.5-2.6.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "DreamOs Plugins ", "OE2.2-Plugins.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Mediaplayer-Youtube ", "mediayou.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "MultiBoot ", "multiboot.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Multimedia ", "Multimedia.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Panels Addons ", "Panels.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Picons Tools ", "picons.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Python Library ", "Library.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Radio Tools", "Radio.png")

        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Script Installer ", "script.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins | TEAM ", "skinsteam.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins Fhd-Hd DreamOs ", "OE2.2-Skins.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Tools2.0 ", "key-updater.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Tools DreamOs ", "key-updater1.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "SoftcamsOE2.0 ", "SOE20.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Softcams DreamOs ", "SOE22.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Sport Tools ", "sport.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Streamlink Tools ", "streamlink.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Utility ", "utility.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Vpn Oe2.0 ", "vpn.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "WeatherTools ", "weather.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "WeatherForecast ", "weather-forecast.png")
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Webcam ", "webcam.png")

        if not config.ParentalControl.configured.value:
            if not has_dpkg:
                add_menu_item(menu_list, self.titles, self.pics, self.urls, "Adult Oe2.0 ", "18+deb.png")
            else:
                add_menu_item(menu_list, self.titles, self.pics, self.urls, "Adult DreamOs ", "18+.png")

        if not has_dpkg:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Other Oe2.0 ", "Other.png")
        else:
            add_menu_item(menu_list, self.titles, self.pics, self.urls, "Other DreamOs ", "Other1.png")

        add_menu_item(menu_list, self.titles, self.pics, self.urls, " Information ", "Information.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, " About ", "about.png")

        self.names = menu_list
        self.sorted = False
        # self.combined_data = list(zip(self.names, self.titles, self.pics, self.urls))
        self["frame"] = MovingPixmap()
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort A-Z'))
        self['key_red'] = Label(_('Exit'))
        self["pixmap"] = Pixmap()
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     'ColorActions',
                                     "EPGSelectActions",
                                     "InfoActions"],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "exit": self.closeRecursive,
                                     "back": self.closeNonRecursive,
                                     "red": self.closeNonRecursive,
                                     "0": self.list_sort,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        self.PIXMAPS_PER_PAGE = 20
        i = 0
        while i < self.PIXMAPS_PER_PAGE:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1

        self.npics = len(self.names)
        self.npage = int(round(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        # self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.index = 0
        self.maxentry = len(menu_list) - 1
        self.ipage = 1
        self.onLayoutFinish.append(self.openTest)

    def paintFrame(self):
        try:
            # If the index exceeds the maximum number of items, it returns to the first item
            if self.index > self.maxentry:
                self.index = self.minentry
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('Error in paintFrame: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
            i1 = 0
            while i1 < self.PIXMAPS_PER_PAGE:
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
            # self["label" + str(i + 1)].setText(self.names[idx])  # this show label to bottom of png pixmap
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        # Decrement the index only if we are not at the first pixmap
        if self.index >= 0:
            self.index -= 1
        else:
            # If we are at the first pixmap, go back to the last pixmap of the last page
            self.ipage = self.npage
            self.index = self.npics - 1
        # Check if we need to change pages
        if self.index < self.minentry:
            self.ipage -= 1
            if self.ipage < 1:  # If we go beyond the first page
                self.ipage = self.npage
                self.index = self.npics - 1  # Back to the last pixmap of the last page
            self.openTest()
        else:
            self.paintFrame()

    def key_right(self):
        # Increment the index only if we are not at the last pixmap
        if self.index < self.npics - 1:
            self.index += 1
        else:
            # If we are at the last pixmap, go back to the first pixmap of the first page
            self.index = 0
            self.ipage = 1
            self.openTest()
        # Check if we need to change pages
        if self.index > self.maxentry:
            self.ipage += 1
            if self.ipage > self.npage:  # If we exceed the number of pages
                self.index = 0
                self.ipage = 1  # Back to first page
            self.openTest()
        else:
            self.paintFrame()

    def key_up(self):
        if self.index >= 5:
            self.index -= 5
        else:
            if self.ipage > 1:
                self.ipage -= 1
                self.index = self.maxentry  # Back to the last line of the previous page
                self.openTest()
            else:
                # If we are on the first page, go back to the last pixmap of the last page
                self.ipage = self.npage
                self.index = self.npics - 1
                self.openTest()
        self.paintFrame()

    def key_down(self):
        if self.index <= self.maxentry - 5:
            self.index += 5
        else:
            if self.ipage < self.npage:
                self.ipage += 1
                self.index = self.minentry  # Back to the top of the next page
                self.openTest()
            else:
                # If we are on the last page, go back to the first pixmap of the first page
                self.index = 0
                self.ipage = 1
                self.openTest()

        self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    # def list_sort(self):
        # self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
        # self.openTest()

    def list_sort(self):
        # Salva le liste originali la prima volta che questa funzione viene chiamata
        if not hasattr(self, 'original_data'):
            self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
            self.sorted = False  # Flag per monitorare lo stato di ordinamento

        # Controlla se è ordinato
        if self.sorted:
            # Se è ordinato, ripristina l'ordine originale
            self.names, self.titles, self.pics, self.urls = self.original_data
            self.sorted = False
            self['sort'].setText(_('0 Sort A-Z'))
        else:
            # Se non è ordinato, applica l'ordinamento
            self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
            self.sorted = True
            self['sort'].setText(_('0 Sort Default'))

        self.openTest()

    def closeNonRecursive(self):
        self.close(False)

    def refreshPlugins(self):
        plugins.clearPluginList()
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))

    def closeRecursive(self):
        if not has_dpkg:
            self.refreshPlugins()
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
        if 'adult' in name.lower():
            self.session.openWithCallback(self.cancelConfirm,
                                          MessageBox,
                                          _('These Panel may contain Adult content\n\nare you sure you want to continue?'))
        else:
            self.okbuttonContinue(self.idx)

    def cancelConfirm(self, result):
        if not result:
            return
        else:
            self.okbuttonContinue(result)

    def okbuttonContinue(self, result):
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

        elif name == "Script Installer ":
            self.session.open(ScriptInstaller, name)

        elif name == "Skins | TEAM ":
            self.session.open(LSskin, name)

        else:
            title = self.titles[self.idx]
            self.data = checkGZIP(xmlurl)
            if self.data is not None:
                n1 = self.data.find(title, 0)
                n2 = self.data.find("</plugins>", n1)
                url = self.data[n1:n2]
                self.session.open(addInstall, url, name, None)
            else:
                self.session.open(MessageBox, _("Error: No Data Find."), MessageBox.TYPE_ERROR)


class LSskin(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.data = checkGZIP(xmlurl)
        # self.data = fetch_url(xmlurl)

        if isWQHD() or isFHD():
            self.pos = get_positions("FHD")
        elif isHD():
            self.pos = get_positions("HD")

        self.name = name
        menu_list = []
        self.titles = []
        self.pics = []
        self.urls = []

        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins All ", "otherskins.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins | HD ", "SkinHD.png")
        # add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins | FHD ", "SkinFHD.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins Egami ", "egami.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins HDF ", "hdf.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins OpenBh ", "openbh.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins OPEN ATV ", "openatv.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins OpenPLi ", "openpli.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins OpenSpa ", "openspa.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins VTi ", "vti.png")
        add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins Oe Based ", "oebased.png")

        self.names = menu_list
        self.sorted = False
        # self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
        self["frame"] = MovingPixmap()
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort A-Z'))
        self['key_red'] = Label(_('Exit'))
        self["pixmap"] = Pixmap()
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     'ColorActions',
                                     "EPGSelectActions",
                                     "InfoActions"],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "exit": self.closeRecursive,
                                     "back": self.closeNonRecursive,
                                     "red": self.closeNonRecursive,
                                     "0": self.list_sort,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        self.PIXMAPS_PER_PAGE = 20
        i = 0
        while i < self.PIXMAPS_PER_PAGE:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1

        self.npics = len(self.names)
        # self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.npage = int(round(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.index = 0
        self.maxentry = len(menu_list) - 1
        self.ipage = 1
        self.onLayoutFinish.append(self.openTest)

    def paintFrame(self):
        try:
            # If the index exceeds the maximum number of items, it returns to the first item
            if self.index > self.maxentry:
                self.index = self.minentry
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('Error in paintFrame: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
            i1 = 0
            while i1 < self.PIXMAPS_PER_PAGE:
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
            # self["label" + str(i + 1)].setText(self.names[idx])  # this show label to bottom of png pixmap
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        # Decrement the index only if we are not at the first pixmap
        if self.index >= 0:
            self.index -= 1
        else:
            # If we are at the first pixmap, go back to the last pixmap of the last page
            self.ipage = self.npage
            self.index = self.npics - 1
        # Check if we need to change pages
        if self.index < self.minentry:
            self.ipage -= 1
            if self.ipage < 1:  # If we go beyond the first page
                self.ipage = self.npage
                self.index = self.npics - 1  # Back to the last pixmap of the last page
            self.openTest()
        else:
            self.paintFrame()

    def key_right(self):
        # Increment the index only if we are not at the last pixmap
        if self.index < self.npics - 1:
            self.index += 1
        else:
            # If we are at the last pixmap, go back to the first pixmap of the first page
            self.index = 0
            self.ipage = 1
            self.openTest()
        # Check if we need to change pages
        if self.index > self.maxentry:
            self.ipage += 1
            if self.ipage > self.npage:  # If we exceed the number of pages
                self.index = 0
                self.ipage = 1  # Back to first page
            self.openTest()
        else:
            self.paintFrame()

    def key_up(self):
        if self.index >= 5:
            self.index -= 5
        else:
            if self.ipage > 1:
                self.ipage -= 1
                self.index = self.maxentry  # Back to the last line of the previous page
                self.openTest()
            else:
                # If we are on the first page, go back to the last pixmap of the last page
                self.ipage = self.npage
                self.index = self.npics - 1
                self.openTest()
        self.paintFrame()

    def key_down(self):
        if self.index <= self.maxentry - 5:
            self.index += 5
        else:
            if self.ipage < self.npage:
                self.ipage += 1
                self.index = self.minentry  # Back to the top of the next page
                self.openTest()
            else:
                # If we are on the last page, go back to the first pixmap of the first page
                self.index = 0
                self.ipage = 1
                self.openTest()

        self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    # def list_sort(self):
        # self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
        # self.openTest()

    def list_sort(self):
        # Salva le liste originali la prima volta che questa funzione viene chiamata
        if not hasattr(self, 'original_data'):
            self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
            self.sorted = False  # Flag per monitorare lo stato di ordinamento

        # Controlla se è ordinato
        if self.sorted:
            # Se è ordinato, ripristina l'ordine originale
            self.names, self.titles, self.pics, self.urls = self.original_data
            self.sorted = False
            self['sort'].setText(_('0 Sort A-Z'))
        else:
            # Se non è ordinato, applica l'ordinamento
            self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
            self.sorted = True
            self['sort'].setText(_('0 Sort Default'))

        self.openTest()

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
        title = self.titles[self.idx]
        self.data = checkGZIP(xmlurl)
        if self.data is not None:
            n1 = self.data.find(title, 0)
            n2 = self.data.find("</plugins>", n1)
            url = self.data[n1:n2]
            self.session.open(addInstall, url, name, None)
        else:
            self.session.open(MessageBox, _("Error: No Data Find."), MessageBox.TYPE_ERROR)


class LSChannel(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        if isWQHD() or isFHD():
            self.pos = get_positions("FHD")
        elif isHD():
            self.pos = get_positions("HD")

        self.name = name
        menu_list = []
        self.titles = []
        self.pics = []
        self.urls = []

        # menu_list, titles, pics, urls, title, pic_name, url
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "CIEFP ", "ciefp.png", 'https://github.com/ciefp/ciefpsettings-enigma2-zipped')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "CYRUS ", "cyrus.png", 'http://www.cyrussettings.com/Set_29_11_2011/Dreambox-IpBox/Config.xml')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "MANUTEK ", "manutek.png", 'http://www.manutek.it/isetting/index.php')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "MORPHEUS ", "morpheus883.png", 'http://github.com/morpheus883/enigma2-zipped')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "VHANNIBAL NET ", "vhannibal1.png", 'http://www.vhannibal.net/asd.php')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "VHANNIBAL TEK ", "vhannibal2.png", 'http://sat.alfa-tech.net/upload/settings/vhannibal/')

        self.names = menu_list
        # self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
        self["frame"] = MovingPixmap()
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort A-Z'))
        self['key_red'] = Label(_('Exit'))
        self["pixmap"] = Pixmap()
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     'ColorActions',
                                     "EPGSelectActions",
                                     "InfoActions"],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "exit": self.closeRecursive,
                                     "back": self.closeNonRecursive,
                                     "red": self.closeNonRecursive,
                                     "0": self.list_sort,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        self.PIXMAPS_PER_PAGE = 20
        i = 0
        while i < self.PIXMAPS_PER_PAGE:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1

        self.npics = len(self.names)
        # self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.npage = int(round(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.index = 0
        self.maxentry = len(menu_list) - 1
        self.ipage = 1
        self.onLayoutFinish.append(self.openTest)

    def paintFrame(self):
        try:
            # If the index exceeds the maximum number of items, it returns to the first item
            if self.index > self.maxentry:
                self.index = self.minentry
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('Error in paintFrame: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
            i1 = 0
            while i1 < self.PIXMAPS_PER_PAGE:
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
            # self["label" + str(i + 1)].setText(self.names[idx])  # this show label to bottom of png pixmap
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        # Decrement the index only if we are not at the first pixmap
        if self.index >= 0:
            self.index -= 1
        else:
            # If we are at the first pixmap, go back to the last pixmap of the last page
            self.ipage = self.npage
            self.index = self.npics - 1
        # Check if we need to change pages
        if self.index < self.minentry:
            self.ipage -= 1
            if self.ipage < 1:  # If we go beyond the first page
                self.ipage = self.npage
                self.index = self.npics - 1  # Back to the last pixmap of the last page
            self.openTest()
        else:
            self.paintFrame()

    def key_right(self):
        # Increment the index only if we are not at the last pixmap
        if self.index < self.npics - 1:
            self.index += 1
        else:
            # If we are at the last pixmap, go back to the first pixmap of the first page
            self.index = 0
            self.ipage = 1
            self.openTest()
        # Check if we need to change pages
        if self.index > self.maxentry:
            self.ipage += 1
            if self.ipage > self.npage:  # If we exceed the number of pages
                self.index = 0
                self.ipage = 1  # Back to first page
            self.openTest()
        else:
            self.paintFrame()

    def key_up(self):
        if self.index >= 5:
            self.index -= 5
        else:
            if self.ipage > 1:
                self.ipage -= 1
                self.index = self.maxentry  # Back to the last line of the previous page
                self.openTest()
            else:
                # If we are on the first page, go back to the last pixmap of the last page
                self.ipage = self.npage
                self.index = self.npics - 1
                self.openTest()
        self.paintFrame()

    def key_down(self):
        if self.index <= self.maxentry - 5:
            self.index += 5
        else:
            if self.ipage < self.npage:
                self.ipage += 1
                self.index = self.minentry  # Back to the top of the next page
                self.openTest()
            else:
                # If we are on the last page, go back to the first pixmap of the first page
                self.index = 0
                self.ipage = 1
                self.openTest()

        self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    # def list_sort(self):
        # self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
        # self.openTest()

    def list_sort(self):
        # Salva le liste originali la prima volta che questa funzione viene chiamata
        if not hasattr(self, 'original_data'):
            self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
            self.sorted = False  # Flag per monitorare lo stato di ordinamento

        # Controlla se è ordinato
        if self.sorted:
            # Se è ordinato, ripristina l'ordine originale
            self.names, self.titles, self.pics, self.urls = self.original_data
            self.sorted = False
            self['sort'].setText(_('0 Sort A-Z'))
        else:
            # Se non è ordinato, applica l'ordinamento
            self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
            self.sorted = True
            self['sort'].setText(_('0 Sort Default'))

        self.openTest()

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
        url = self.urls[self.idx]
        self.session.open(addInstall, url, name, '')


class ScriptInstaller(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LinuxsatPanel.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()

        if isWQHD() or isFHD():
            self.pos = get_positions("FHD")
        elif isHD():
            self.pos = get_positions("HD")

        self.name = name
        menu_list = []
        self.titles = []
        self.pics = []
        self.urls = []

        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Add Libssl Libcrypto", "AddLibssl.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Add_Libssl1_Libcrypto1.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Add Symlink Libssl", "AddSymlink.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Symlink_Creator.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Ajpanel AMAJamry", "Ajpanel.png", 'wget --no-check-certificate "https://raw.githubusercontent.com/biko-73/AjPanel/main/installer.sh?inline=false" -O - | /bin/sh')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Biss Feed Autokey", "BissFeedAutokey.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/bissfeedautokey.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Chocholousek Picons", "ChocholousekPicons.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/chocholousek-picons.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Dns Cloudfaire", "DnsCloudfaire.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsCloudflare.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Dns Google", "DnsGoogle.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsGoogle.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Dns Quad9", "DnsQuad9.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsQuad9.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "E2player MOHAMED", "E2playerMOHAMED.png", 'wget --no-check-certificate "https://gitlab.com/MOHAMED_OS/e2iplayer/-/raw/main/install-e2iplayer.sh?inline=false" -O - | /bin/sh')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "E2player MAXBAMBY", "E2playerMAXBAMBY.png", 'wget -qO- --no-check-certificate "https://gitlab.com/maxbambi/e2iplayer/-/raw/master/install-e2iplayer.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "E2player ZADMARIO", "E2playerZADMARIO.png", 'wget -q- --no-check-certificate "https://gitlab.com/zadmario/e2iplayer/-/raw/master/install-e2iplayer.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "E2player XXX", "E2playerXXX.png", 'wget -q- --no-check-certificate "https://gitlab.com/iptv-host-xxx/iptv-host-xxx/-/raw/master/IPTVPlayer/iptvupdate/custom/xxx.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "History Zap Selector", "HistoryZapSelector.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/historyzapselector-dorik.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "iSetting E2", "iSettingE2.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/isetting-e2.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Keys Update", "keys.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Keys_Updater.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Levi45 Manager", "Levi45Manager.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/levi-45/Manager/main/installer.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Mountpoints", "Mountpoints.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Mountpoints.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Multistalker Ziko", "Multistalker.png", 'wget -q install --force-depends "https://dreambox4u.com/emilnabil237/plugins/MultiStalkerPro/installer.sh?inline=false" -O - | /bin/sh ;wget -q --no-check-certificate "https://gitlab.com/hmeng80/extensions/-/raw/main/multistalker/portal/Portal_multistalker.sh?inline=false" -O - | /bin/sh')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "New VirtualKeyboard", "NewVirtualKeyboard.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Quicksignal Raed", "Quicksignal.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/fairbird/RaedQuickSignal/main/installer.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "XC Forever", "xc.png", 'wget -q "--no-check-certificate" https://raw.githubusercontent.com/Belfagor2005/xc_plugin_forever/main/installer.sh?inline=false -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Xstreamity", "xstreamity.png", 'wget -q "--no-check-certificate" wget https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh?inline=false -O - | bash')
        # add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "X-Klass", "xklass.png", 'wget -qO- --no-check-certificate "https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/XKlass/online-setup" | -O - | bash')

        # Adding more options without URLs
        if not has_dpkg:
            menu_list.append("Lcn Scanner")
            self.titles.append("Search Scanner Lcn channels ")
            self.pics.append(picfold + "LcnSearch.png")
            self.urls.append('')

        menu_list.append("Check Skin Conponent")
        self.titles.append("Search Skin Conponent Image Necessary ")
        self.pics.append(picfold + "CheckSkin.png")
        self.urls.append('')

        menu_list.append("Send Cline -> CCcam.cfg")
        self.titles.append("Send CCcline CCcam ")
        self.pics.append(picfold + "cccamfreee.png")
        self.urls.append('')

        menu_list.append("Send Cline -> oscam.server")
        self.titles.append("Send CCcline Oscam ")
        self.pics.append(picfold + "oscamfree.png")
        self.urls.append('')

        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Send Emm", "SendEmm.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Emm_Sender.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Subsupport addon", "SubSupportAddon.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/subsupport-addon.sh?inline=false" -O - | bash')
        add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "Transmission addon", "transmission.png", 'wget -q --no-check-certificate "http://dreambox4u.com/dreamarabia/Transmission_e2/Transmission_e2.sh?inline=false" -O - | bash')
        if not has_dpkg:
            add_menu_item_with_url(menu_list, self.titles, self.pics, self.urls, "ServiceApp Exteplayer", "serviceapp.png", 'opkg update && opkg --force-reinstall --force-overwrite install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp')

        self.names = menu_list
        self.sorted = False
        # self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
        self["frame"] = MovingPixmap()
        self['info'] = Label()
        self['info'].setText(_('Please Wait...'))
        self['sort'] = Label(_('0 Sort A-Z'))
        self['key_red'] = Label(_('Exit'))
        self["pixmap"] = Pixmap()
        self["actions"] = ActionMap(["OkCancelActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions",
                                     'ColorActions',
                                     "EPGSelectActions",
                                     "InfoActions"],
                                    {"ok": self.okbuttonClick,
                                     "cancel": self.closeNonRecursive,
                                     "exit": self.closeRecursive,
                                     "back": self.closeNonRecursive,
                                     "red": self.closeNonRecursive,
                                     "0": self.list_sort,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down,
                                     "info": self.key_info,
                                     "menu": self.closeRecursive})

        self.PIXMAPS_PER_PAGE = 20
        i = 0
        while i < self.PIXMAPS_PER_PAGE:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1

        self.npics = len(self.names)
        # self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.npage = int(round(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.index = 0
        self.maxentry = len(menu_list) - 1
        self.ipage = 1
        self.onLayoutFinish.append(self.openTest)

    def Lcn(self, answer=None):
        if answer is None:
            self.session.openWithCallback(self.Lcn,
                                          MessageBox, _("Do you want to Order LCN Bouquet"),
                                          MessageBox.TYPE_YESNO)
        else:
            print('scan init')
            lcn_scanner_instance = LCNScanner()
            LCN = lcn_scanner_instance.lcnScan()
            # print("LCNScannerSetup instance:", LCN)
            try:
                self.session.open(LCN)
            except Exception as e:
                print('except..:', e)
            self.session.open(MessageBox, _('[LCNScanner] LCN scan finished\nChannels Ordered!'),
                              MessageBox.TYPE_INFO,
                              timeout=5)

    def Checkskin(self, answer=None):
        if answer is None:
            self.session.openWithCallback(self.Checkskin,
                                          MessageBox, _("[Checkskin] This operation checks if the skin has its components (is not sure)..\nDo you really want to continue?"),
                                          MessageBox.TYPE_YESNO)
        else:
            from .addons import checkskin
            self.check_module = eTimer()
            check = checkskin.check_module_skin()
            try:
                self.check_module_conn = self.check_module.timeout.connect(check)
            except:
                self.check_module.callback.append(check)
            self.check_module.start(100, True)
            self.openVi()

    def openVi(self, callback=''):
        from .addons.File_Commander import File_Commander
        user_log = '/tmp/my_debug.log'
        if fileExists(user_log):
            self.session.open(File_Commander, user_log)

    def paintFrame(self):
        try:
            # If the index exceeds the maximum number of items, it returns to the first item
            if self.index > self.maxentry:
                self.index = self.minentry
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('Error in paintFrame: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
            i1 = 0
            while i1 < self.PIXMAPS_PER_PAGE:
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
            # self["label" + str(i + 1)].setText(self.names[idx])  # this show label to bottom of png pixmap
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = blpic
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        # Decrement the index only if we are not at the first pixmap
        if self.index >= 0:
            self.index -= 1
        else:
            # If we are at the first pixmap, go back to the last pixmap of the last page
            self.ipage = self.npage
            self.index = self.npics - 1
        # Check if we need to change pages
        if self.index < self.minentry:
            self.ipage -= 1
            if self.ipage < 1:  # If we go beyond the first page
                self.ipage = self.npage
                self.index = self.npics - 1  # Back to the last pixmap of the last page
            self.openTest()
        else:
            self.paintFrame()

    def key_right(self):
        # Increment the index only if we are not at the last pixmap
        if self.index < self.npics - 1:
            self.index += 1
        else:
            # If we are at the last pixmap, go back to the first pixmap of the first page
            self.index = 0
            self.ipage = 1
            self.openTest()
        # Check if we need to change pages
        if self.index > self.maxentry:
            self.ipage += 1
            if self.ipage > self.npage:  # If we exceed the number of pages
                self.index = 0
                self.ipage = 1  # Back to first page
            self.openTest()
        else:
            self.paintFrame()

    def key_up(self):
        if self.index >= 5:
            self.index -= 5
        else:
            if self.ipage > 1:
                self.ipage -= 1
                self.index = self.maxentry  # Back to the last line of the previous page
                self.openTest()
            else:
                # If we are on the first page, go back to the last pixmap of the last page
                self.ipage = self.npage
                self.index = self.npics - 1
                self.openTest()
        self.paintFrame()

    def key_down(self):
        if self.index <= self.maxentry - 5:
            self.index += 5
        else:
            if self.ipage < self.npage:
                self.ipage += 1
                self.index = self.minentry  # Back to the top of the next page
                self.openTest()
            else:
                # If we are on the last page, go back to the first pixmap of the first page
                self.index = 0
                self.ipage = 1
                self.openTest()

        self.paintFrame()

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    # def list_sort(self):
        # self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
        # self.openTest()

    def list_sort(self):
        # Salva le liste originali la prima volta che questa funzione viene chiamata
        if not hasattr(self, 'original_data'):
            self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
            self.sorted = False  # Flag per monitorare lo stato di ordinamento

        # Controlla se è ordinato
        if self.sorted:
            # Se è ordinato, ripristina l'ordine originale
            self.names, self.titles, self.pics, self.urls = self.original_data
            self.sorted = False
            self['sort'].setText(_('0 Sort A-Z'))
        else:
            # Se non è ordinato, applica l'ordinamento
            self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
            self.sorted = True
            self['sort'].setText(_('0 Sort Default'))

        self.openTest()

    def closeNonRecursive(self):
        self.close(False)

    def closeRecursive(self):
        self.close(True)

    def createSummary(self):
        return

    def key_info(self):
        self.session.open(LSinfo, " Information ")

    def okbuttonClick(self):
        idx = self.index
        print('[okbuttonClick] idx', idx)
        if idx is None:
            return
        self.namev = self.names[idx]
        self.url = self.urls[idx]
        print('[okbuttonClick] self.namev', self.namev)
        print('[okbuttonClick] self.url', self.url)

        if 'cccam.cfg' in self.namev.lower():
            # self.getcl('CCcam')
            self.askForFcl()
            return

        if 'oscam.serv' in self.namev.lower():
            self.getcl('Oscam')
            return

        if 'lcn scanner' in self.namev.lower():
            self.Lcn()
            return

        if 'check skin conponent' in self.namev.lower():
            self.Checkskin()
            return

        self.session.openWithCallback(self.okClicked,
                                      MessageBox, _("Do you want to execute %s?") % self.namev,
                                      MessageBox.TYPE_YESNO, default=True)

    def okClicked(self, answer=False):
        if answer:
            title = (_("Executing %s\nPlease Wait...") % self.namev)
            keywords = ['google', 'cloudfaire', 'quad9', 'emm', 'keys']
            lower_namev = self.namev.lower()
            keyword_found = any(keyword in lower_namev for keyword in keywords)
            if keyword_found:
                cmd = str(self.url) + ' > /tmp/my_debug.log'
                self.session.open(lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=False)
            else:
                cmd = str(self.url) + ' > /tmp/my_debug.log'
                self.session.openWithCallback(self.openVi, lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=True)
        else:
            return

    def askForFcl(self):
        self.session.openWithCallback(self.runScriptWithConsole,
                                      MessageBox, _("Do you want add Cline?"),
                                      MessageBox.TYPE_YESNO)

    def runScriptWithConsole(self, confirmed):
        if confirmed:
            script_path = "/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
            url = "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/refs/heads/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
            try:
                import requests
                from os import chmod
                response = requests.get(url)
                response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)
                with open(script_path, 'w') as file:
                    file.write(response.text)
                chmod(script_path, 0o777)
            except Exception as e:
                print("Failed to update script: {e}. Using existing script.", e)

            self.session.open(lsConsole, title="Executing Free Cline Access Script", cmdlist=[script_path])

    def getcl(self, config_type):
        if config_type == 'CCcam':
            dest = '/etc/CCcam.cfg'
            src = plugin_path + '/sh/CCcam.cfg'
            not_found_msg = _('File not found /etc/CCcam.cfg!\nRestart please...')
            write_format = '\nC: {} {} {} {}\n'

        elif config_type == 'Oscam':
            dest_dir = '/etc/tuxbox/config'
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            dest = os.path.join(dest_dir, 'oscam.server')
            src = plugin_path + '/sh/oscam.server'
            not_found_msg = _('File not found /etc/tuxbox/config/oscam.server!\nRestart please...')
            write_format = ('\n[reader]\n'
                            'label = Server_{}\n'  # host
                            'enable= 1\n'
                            'protocol = cccam\n'
                            'device = {}, {}\n'  # host, port,
                            'user = {}\n'  # user
                            'password = {}\n'  # pasw
                            'inactivitytimeout = 30\n'
                            'group = 1\n'
                            'cccversion = 2.1.2\n'
                            'cccmaxhops = 1\n'
                            'ccckeepalive = 1\n'
                            'audisabled = 1\n\n')
        else:
            print('unknow actions')
            return

        if not os.path.exists(dest):
            shutil.copy2(src, dest)
            self.session.open(MessageBox, not_found_msg,
                              type=MessageBox.TYPE_INFO,
                              timeout=8)
            return

        try:
            dat = RequestUrl()
            print('Request Server url is:', dat)
            # data = checkGZIP(dat)
            data = make_request(dat)
            # data = fetch_url(dat)

            if PY3:
                data = six.ensure_str(data)

            if 'bosscccam' in data:  # ok
                print('bosscccam pattern')
                regex_patterns = [
                    r"<strong>c:\s*([\w.-]+)\s+(\d+)\s+([\w\d]+)\s+([\w.-]+)</strong>",
                ]
            elif 'cccambird' in data:  # ok
                print('cccambird pattern')
                regex_patterns = [
                    r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</th></tr>',
                ]
            elif 'cccamia' in data:  # ok
                print('cccamia pattern')
                regex_patterns = [
                    r'>?C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*',
                ]
            elif 'cccam.net' in data:  # ok
                print('cccam.net pattern')
                regex_patterns = [
                    r'b>C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)',
                ]
            elif 'iptv-15days' in data:  # ok cccamia
                print('15days pattern')
                regex_patterns = [
                    r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</th></tr>',
                ]
            else:
                print('generic pattern')
                regex_patterns = [
                    r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</h3>',
                    r'<strong>c:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</strong',
                    r'cline">\s*C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*'
                    r'<h1>C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*',
                    r'"C: (.*?) (.*?) (.*?) (.*?)"',
                    r'"c: (.*?) (.*?) (.*?) (.*?)"',
                ]
            host = None
            pas = None
            for pattern in regex_patterns:
                url1 = re.search(pattern, data)
                if url1:
                    host = url1.group(1)
                    port = url1.group(2)
                    user = url1.group(3)
                    pas = url1.group(4)
                    '''
                    print("Server:", host)
                    print("Port:", port)
                    print("User:", user)
                    print("Password:", pas)
                    '''
            if host and host is not None:
                pas = pas.replace('</h1>', '').replace('</b>', '')
                pasw = pas.replace('</div>', '').replace('</span>', '')

                if config_type == 'CCcam':
                    print('write cccam file')
                    with open(dest, 'a') as cfgdok:
                        cfgdok.write(write_format.format(host, port, user, pasw))

                if config_type == 'Oscam':
                    print('write Oscam file')
                    with open(dest, 'a') as cfgdok:
                        cfgdok.write(write_format.format(host, host, port, user, pasw))

                self.session.open(MessageBox, _('Server %s added in %s\n\nServer:%s\nPort:%s\nUser:%s\nPassword:%s\n') % (host, dest, host, port, user, pasw),
                                  type=MessageBox.TYPE_INFO, timeout=6)
            else:
                self.session.open(MessageBox, _("Server Error.\n\nTry again, you'll be luckier!"),
                                  type=MessageBox.TYPE_INFO,
                                  timeout=8)

        except Exception as e:
            print('error on host', str(e))


class addInstall(Screen):

    def __init__(self, session, data, name, dest):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'addInstall.xml')
        if has_dpkg:
            skin = os.path.join(skin_path, 'addInstall-os.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.fxml = str(data)
        self.name = name
        self.dest = dest
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Install'))
        self['key_yellow'] = Label(_('Remove'))
        self['key_blue'] = Label(_('Restart enigma'))
        self['sort'] = Label()
        if HALIGN == RT_HALIGN_RIGHT:
            self['sort'].setText(_('0 Halign Left'))
        else:
            self['sort'].setText(_('0 Halign Right'))
        '''
        self.LcnOn = False
        if os.path.exists('/etc/enigma2/lcndb') and lngx == 'it':
            self['key_yellow'].setText('Lcn')
            self.LcnOn = True
            print('LcnOn = True')
        '''
        self.list = []
        self["list"] = LPSlist([])
        self['fspace'] = Label()
        self['fspace'].setText(_('Please Wait...'))
        self['info'] = Label()
        self['info'].setText(_('Load Category...'))
        self.downloading = False
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', 'NumberActions'],
                                    {'ok': self.message,
                                     '0': self.arabicx,
                                     '5': self.Lcn,
                                     'green': self.message,
                                     'cancel': self.exitnow,
                                     'red': self.exitnow,
                                     'blue': self.restart,
                                     'yellow': self.remove}, -2)
        self.timer = eTimer()
        if has_dpkg:
            self.timer_conn = self.timer.timeout.connect(self.getfreespace)
        else:
            self.timer.callback.append(self.getfreespace)
        self.timer.start(1000, 1)

        if self.dest is not None:
            self.onLayoutFinish.append(self.downxmlpage)
        else:
            self.onLayoutFinish.append(self.openTest)

    def arabicx(self):
        global HALIGN
        if HALIGN == RT_HALIGN_LEFT:
            HALIGN = RT_HALIGN_RIGHT
            self['sort'].setText(_('0 Halign Left'))
        elif HALIGN == RT_HALIGN_RIGHT:
            HALIGN = RT_HALIGN_LEFT
            self['sort'].setText(_('0 Halign Right'))

        if self.dest is not None:
            self.downxmlpage()
        else:
            self.openTest()

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
        self.buttons()

    def buttons(self):
        if HALIGN == RT_HALIGN_RIGHT:
            self['sort'].setText(_('0 Halign Left'))
        else:
            self['sort'].setText(_('0 Halign Right'))
        # if self.LcnOn is True:
        # # self.LcnOn = False
        # # if os.path.exists('/etc/enigma2/lcndb') and lngx == 'it':
            # self['key_yellow'].setText('Lcn')
            # # self.LcnOn = True
            # print('LcnOn 2 = True')
        # else:
            # self['key_yellow'].setText(_('Remove'))
        return

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
                if not has_dpkg:
                    self.session.open(MessageBox, _('Unknow Image!'),
                                      MessageBox.TYPE_INFO,
                                      timeout=5)
                    return
                n2 = self.plug.find("_", 0)
                self.iname = self.plug[:n2]

            if ".ipk" in self.plug:
                if has_dpkg:
                    self.session.open(MessageBox, _('Unknow Image!'),
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
            print("File downloaded successfully.")
            return True
        else:
            print("Error downloading the file.")
        return False

    def okClicked(self, answer=False):
        if answer:
            dest = "/tmp"
            if not os.path.exists(dest):
                os.system('ln -sf  /var/volatile/tmp /tmp')
            folddest = '/tmp/' + self.plug
            if self.retfile(folddest):
                cmd2 = ''
                if ".deb" in self.plug:
                    cmd2 = "dpkg -i /tmp/" + self.plug  # + "'"
                if ".ipk" in self.plug:
                    cmd2 = "opkg install --force-reinstall --force-overwrite '/tmp/" + self.plug + "'"
                elif ".zip" in self.plug:
                    cmd2 = "unzip -o -q '/tmp/" + self.plug + "' -d /"
                elif ".tar" in self.plug and "gz" in self.plug:
                    cmd2 = "tar -xvf '/tmp/" + self.plug + "' -C /"
                elif ".bz2" in self.plug and "gz" in self.plug:
                    cmd2 = "tar -xjvf '/tmp/" + self.plug + "' -C /"
                # print('cmd:', cmd)
                title = (_("Installing %s\nPlease Wait...") % self.iname)
                self.session.open(lsConsole, _(title), cmdlist=[cmd2], closeOnSuccess=False)

    def downxmlpage(self):
        self.downloading = False
        r = make_request(self.fxml)
        if r is None:
            print("Errore: Nessun dato ricevuto da make_request")
            return
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
                regex = r'title="ciefp-E2-(.*?).zip".*?href="(.*?)"'
                match = re.compile(regex).findall(r)
                # print('match:', match)
                for name, url in match:
                    if url.find('.zip') != -1:
                        url = url.replace('blob', 'raw')
                        url = 'https://github.com' + url
                        name = decode_html(name)
                        self.downloading = True
                    item = name + "###" + str(url)
                    items.append(item)
                    items.sort()

            if 'cyrus' in self.name.lower():
                n1 = r.find('name="Sat">', 0)
                n2 = r.find("/ruleset>", n1)
                r = r[n1:n2]
                regex = r'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
                match = re.compile(regex).findall(r)
                # print('match:', match)
                for name, url, date in match:
                    if url.find('.zip') != -1:
                        if 'ddt' in name.lower():
                            continue
                        if 'Sat' in name.lower():
                            continue
                        name = decode_html(name) + ' ' + date
                        self.downloading = True
                    item = name + "###" + str(url)
                    items.append(item)
                    items.sort()

            if 'manutek' in self.name.lower():
                regex = r'href="/isetting/.*?file=(.+?).zip">'
                match = re.compile(regex).findall(r)
                # print('match:', match)
                for url in match:
                    name = url
                    name = name.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")
                    url = 'http://www.manutek.it/isetting/enigma2/' + url + '.zip'
                    self.downloading = True
                    item = decode_html(name) + "###" + str(url)
                    items.append(item)
                    items.sort()

            if 'morpheus' in self.name.lower():
                regex = r'title="E2_Morph883_(.*?).zip".*?href="(.*?)"'
                # n1 = r.find('title="README.txt', 0)
                # n2 = r.find('href="#readme">', n1)
                # r = r[n1:n2]
                match = re.compile(regex).findall(r)
                # print('match:', match)
                for name, url in match:
                    if url.find('.zip') != -1:
                        name = 'Morph883 ' + decode_html(name)
                        url = url.replace('blob', 'raw')
                        url = 'https://github.com' + url
                        self.downloading = True
                    item = name + "###" + str(url)
                    items.append(item)
                    items.sort()

            if 'vhannibal net' in self.name.lower():
                '''
                <tr class="site_content_row">
                <td width="30"><img src="images/green_icon.png" alt="Aggiornato il 07/10/24 alle 10:24:57" width="30" height="30" title="Aggiornato il 07/10/24 alle 10:24:57"/></td>
                <td><a href="download_setting.php?id=1&action=download" target="_blank">Vhannibal Hot Bird 13°E</a></td>
                <td> 7 ott</td>
                <td>858435</td>
                <td width="30"><a href="download_setting.php?id=1&action=download" target="_blank"><img src="images/download_icon.png" width="30" height="30" alt="Scarica" /></a></td>
                </tr>
                '''

                # r = six.ensure_str(r, errors='replace')

                pattern = re.compile(r'<td><a href="(.+?)".*?>(.+?)</a>.*?<td>(.+?)</td>.*?</tr>', re.DOTALL)
                matches = pattern.findall(r)
                for match in matches:
                    url = match[0]
                    name = match[1]
                    if isinstance(name, bytes):
                        name = name.decode('utf-8', errors='replace')
                    name = decode_html(match[1])
                    date = match[2]
                    name = str(name).replace('&#127381;', '').replace("%20", " ").replace("..", "").strip() + ' ' + date
                    url = "https://www.vhannibal.net/" + url
                    self.downloading = True
                    item = name + "###" + str(url)
                    items.append(item)
                    items.sort()

            if 'vhannibal tek' in self.name.lower():
                regex = r'<a href="Vhannibal(.*?).zip".*?right">(.*?) </td'
                match = re.compile(regex).findall(r)
                for url, date in match:
                    if '.php' in url.lower():
                        continue
                    name = decode_html(url).replace('&#127381;', '').replace("%20", " ") + ' ' + date
                    url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + '.zip'
                    self.downloading = True
                    item = name + "###" + str(url)
                    items.append(item)
                    items.sort()

            for item in items:
                name = item.split('###')[0]
                url = item.split('###')[1]
                if name in self.names:
                    continue
                name = str(decode_html(name))
                url = str(url)
                self.names.append(name.strip())
                self.urls.append(url.strip())
            LPshowlist(self.names, self["list"])
        except Exception as e:
            print('downxmlpage get failed: ', str(e))
            self['info'].setText(_('Download page get failed ...'))

    def Lcn(self, answer=None):
        if answer is None:
            self.session.openWithCallback(self.Lcn,
                                          MessageBox, _("[LCNScanner] Do you want to Scan Order LCN Bouquet"),
                                          MessageBox.TYPE_YESNO)
        else:
            print('scan init')
            lcn_scanner_instance = LCNScanner()
            LCN = lcn_scanner_instance.lcnScan()
            # print("LCNScannerSetup instance:", LCN)
            try:
                self.session.open(LCN)
            except Exception as e:
                print('except..:', e)
            self.session.open(MessageBox, _('[LCNScanner] LCN scan finished\nChannels Ordered!'),
                              MessageBox.TYPE_INFO,
                              timeout=5)

    def okRun(self):
        self.session.openWithCallback(self.okRun1,
                                      MessageBox, _("Do you want to install?"),
                                      MessageBox.TYPE_YESNO)

    def okRun1(self, answer=False):
        dest = "/tmp/settings.zip"
        if answer:
            global setx
            if self.downloading is True:
                idx = self["list"].getSelectionIndex()
                url = self.urls[idx]
                self.namel = ''
                if 'dtt' not in url.lower():
                    setx = 1
                    terrestrial()
                if keepiptv():
                    print('-----save iptv channels-----')

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
                    self.session.openWithCallback(self.yes, lsConsole, title=_(title),
                                                  cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"],
                                                  closeOnSuccess=False)
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
        self.session.openWithCallback(self.removenow,
                                      MessageBox, _("Do you want to remove?"),
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
            self.session.open(lsConsole, _(title), cmdlist=[cmd])

    def restart(self):
        self.session.openWithCallback(self.restartnow,
                                      MessageBox, _("Do you want to restart Gui Interface?"),
                                      MessageBox.TYPE_YESNO)

    def restartnow(self, answer=False):
        if answer:
            self.session.open(TryQuitMainloop, 3)

    def exitnow(self):

        try:
            if not has_dpkg:
                refreshPlugins()
        except Exception as e:
            print('error on exit!', e)

        self.close()


class LSinfo(Screen):

    def __init__(self, session, name):
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'LSinfo.xml')
        if has_dpkg:
            skin = os.path.join(skin_path, 'LSinfo-os.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        titlex = descplug + ' V.' + currversion
        self.name = name
        info = _('Please Wait...')
        self.labeltext = ('')
        self['list'] = ScrollLabel(info)
        self['key_green'] = Label()
        self["pixmap"] = Pixmap()
        self["pixmap"].hide()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'DirectionActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'ColorActions',
                                     'ChannelSelectBaseActions'], {'ok': self.close,
                                                                   'back': self.close,
                                                                   'cancel': self.close,
                                                                   'up': self.Up,
                                                                   'down': self.Down,
                                                                   'left': self.Up,
                                                                   'right': self.Down,
                                                                   # 'yellow': self.update_me,
                                                                   'green': self.update_me,
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
        if has_dpkg:
            self.timer_conn = self.timer.timeout.connect(self.startRun)
        else:
            self.timer.callback.append(self.startRun)
        self.timer.start(1000, 1)
        self.onLayoutFinish.append(self.pas)

    def pas(self):
        pass

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
        # if float(currversion) < float(remote_version):
        if currversion < remote_version:
            self.Update = True
            print('new version online')
            self.mbox = self.session.open(MessageBox, _('New version %s is available\n\nChangelog: %s\n\nPress green button to start updating') % (self.new_version, self.new_changelog),
                                          MessageBox.TYPE_INFO, timeout=5)
            self['key_green'].setText(_('Update'))
            self["pixmap"].show()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(self.install_update,
                                          MessageBox, _("New version %s is available.\n\nChangelog: %s\n\nDo you want to install it now?") % (self.new_version, self.new_changelog),
                                          MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox,
                              _("Congrats! You already have the latest version..."),
                              MessageBox.TYPE_INFO, timeout=4)

    def update_dev(self):
        req = Request(b64decoder(developer_url), headers={'User-Agent': AgentRequest})
        page = urlopen(req).read()
        data = json.loads(page)
        remote_date = data['pushed_at']
        strp_remote_date = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
        remote_date = strp_remote_date.strftime('%Y-%m-%d')
        self.session.openWithCallback(self.install_update,
                                      MessageBox, _("Do you want to install update ( %s ) now?") % (remote_date),
                                      MessageBox.TYPE_YESNO)

    def install_update(self, answer=False):
        if answer:
            self.session.open(lsConsole, 'Upgrading...', cmdlist=['wget -q "--no-check-certificate" ' + b64decoder(installer_url) + ' -O - | /bin/sh'], finishedCallback=self.myCallback, closeOnSuccess=False)
        else:
            self.session.open(MessageBox, _("Update Aborted!"),
                              MessageBox.TYPE_INFO, timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def startRun(self):
        try:
            if self.name == " Information ":
                # self.infoBox()
                self.openinfo()

            elif self.name == " About ":
                # ab = fetch_url(abouturl)
                with open(os.path.join(plugin_path, 'LICENSE'), 'r') as filer:
                    info = filer.read()
                    self['list'].setText(info)
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
            if has_dpkg:
                zarcffll = os.popen('dpkg --print-architecture | grep -iE "arm|aarch64|mips|cortex|sh4|sh_4"').read().strip('\n\r')
            else:
                zarcffll = os.popen('opkg print-architecture | grep -iE "arm|aarch64|mips|cortex|h4|sh_4"').read().strip('\n\r')
        except Exception as e:
            print("Error ", e)
        return str(zarcffll)

    def openinfo(self, callback=''):
        from .stbinfo import stbinfo
        print('STB info:\n%s' % stbinfo.to_string())
        with open('/tmp/output.txt', 'w') as file:
            info = 'Suggested by: @masterG - @oktus - @pcd\nAll code was rewritten by @Lululla - 2024.07.20\n'
            info2 = 'Designs and Graphics by @oktus\nSupport on: Linuxsat-support.com\n\n'
            file.write('%s V.%s\n%s%s\nSTB info:\n%s' % (descplug, currversion, info, info2, stbinfo.to_string()))
        # user_log = '/tmp/output.txt'
        # if fileExists(user_log):
            # from .File_Commander import File_Commander
            # self.session.open(File_Commander, user_log)
        try:
            with open('/tmp/output.txt', 'r') as filer:
                info = filer.read()
                self['list'].setText(info)
        except Exception as e:
            print(e)

    def infoBox(self):
        info = '%s V.%s\n\n' % (descplug, currversion)
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
            info += 'Suggested by: @masterG - @oktus - @pcd\n'
            info += 'All code was rewritten by @Lululla - 2024.07.20\n'
            info += 'Designs and Graphics by @oktus\n'
            info += 'Support on: Linuxsat-support.com\n\n'
            info += 'Current IP Wan: %s\n' % ifg
            info += 'Image: %s' % img
            info += 'Cpu: %s\n' % arc
            info += 'Python Version: %s\n' % python
            info += 'Arch. Info: %s\n' % arkFull
            info += 'Libssl(oscam): %s\n' % libsssl
            info += fetch_url(infourl)
        except Exception as e:
            print("Error ", e)
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
        self["version"] = Label('Wait Please... Linuxsat Panel V.' + currversion)
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
        if os.path.exists("/usr/bin/apt-get"):
            self.timer_conn = self.timer.timeout.connect(self.decodeImage)
        else:
            self.timer.callback.append(self.decodeImage)
        self.timer.start(100, True)

        self.timerx = eTimer()
        if os.path.exists("/usr/bin/apt-get"):
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
            if os.path.exists("/usr/bin/apt-get"):
                self.picload.startDecode(pixmapx, False)
            else:
                self.picload.startDecode(pixmapx, 0, 0, False)
            ptr = self.picload.getData()
            if ptr is not None:
                self['poster'].instance.setPixmap(ptr)
                self['poster'].show()
        return


def menustart():
    try:
        if CheckConn():
            _session.open(startLP)
        else:
            _session.open(MessageBox, _('Check Connection!'),
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
    add_skin_font()  # Initialize the necessary fonts
    return [
        PluginDescriptor(
            name="Linuxsat Panel",
            description=descplug,
            icon="LinuxsatPanel.png",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
        ),
        PluginDescriptor(
            name="Linuxsat Panel",
            description=descplug,
            where=PluginDescriptor.WHERE_MENU,
            fnc=menu
        )
    ]
