#!/usr/bin/python
# -*- coding: utf-8 -*-

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

from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from enigma import getDesktop
import gettext
import os

descplug = "Linuxsat-Support.com (Addons Panel)"
PluginLanguageDomain = 'LinuxsatPanel'
PluginLanguagePath = 'Extensions/LinuxsatPanel/locale'

infourl = 'https://patbuweb.com/xml/info.txt'
abouturl = 'https://patbuweb.com/xml/about.txt'
xmlurl = 'http://patbuweb.com/xml/addons_2024.xml'

isDreamOS = False
if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


def wgetsts():
    wgetsts = False
    cmd22 = 'find /usr/bin -name "wget"'
    res = os.popen(cmd22).read()
    if 'wget' not in res.lower():
        if os.path.exists("/var/lib/dpkg/status"):
            cmd23 = 'apt-get update && apt-get install wget'
            os.popen(cmd23)
            wgetsts = True
        else:
            cmd23 = 'opkg update && opkg install wget'
            os.popen(cmd23)
            wgetsts = True
        return wgetsts


def localeInit():
    if isDreamOS:  # check if opendreambox image
        lang = language.getLanguage()[:2]  # getLanguage returns e.g. "fi_FI" for "language_country"
        os.environ["LANGUAGE"] = lang  # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreamOS:  # check if DreamOS image
    _ = lambda txt: gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
else:
    def _(txt):
        if gettext.dgettext(PluginLanguageDomain, txt):
            return gettext.dgettext(PluginLanguageDomain, txt)
        else:
            print(("[%s] fallback to default translation for %s" % (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)
localeInit()
language.addCallback(localeInit)


def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())


def isFHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] >= 1920


def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280

AgentRequest = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'


# self.token = "ZUp6enk4cko4ZzBKTlBMTFNxN3djd25MOHEzeU5Zak1Bdkd6S3lPTmdqSjhxeUxMSTBNOFRhUGNBMjBCVmxBTzlBPT0K"
# def check(self, token):
    # result = base64.b64decode(token)
    # result = zlib.decompress(base64.b64decode(result))
    # result = base64.b64decode(result).decode()
    # return result
