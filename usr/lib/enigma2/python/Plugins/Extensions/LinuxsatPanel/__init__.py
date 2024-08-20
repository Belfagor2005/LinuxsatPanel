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
from Tools.Directories import (resolveFilename, SCOPE_PLUGINS)
from enigma import (
    RT_HALIGN_RIGHT,
    RT_HALIGN_LEFT,
    getDesktop,
)
from os import path as os_path
import gettext
import os
import sys

descplug = "Linuxsat-Support.com (Addons Panel)"
PluginLanguageDomain = 'LinuxsatPanel'
PluginLanguagePath = 'Extensions/LinuxsatPanel/locale'
plugin_path = os.path.dirname(sys.modules[__name__].__file__)

infourl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/info.txt'
abouturl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/about.txt'
# xmlurl = 'https://github.com/Belfagor2005/upload/raw/main/fill/addons_2024.xml'
xmlurl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/addons_2024.xml'
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9MaW51eHNhdFBhbmVsL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvTGludXhzYXRQYW5lbA=='

isDreamOS = False
if os.path.exists("/var/lib/dpkg/status"):
    isDreamOS = True


def CheckConn(host='www.google.com', port=80, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print('error: ', e)
        return False


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


def isWQHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] >= 2560


def isFHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] >= 1920


def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] <= 1280


AgentRequest = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'


def refreshPlugins():
    from Components.PluginComponent import plugins
    from Tools.Directories import SCOPE_PLUGINS, resolveFilename
    plugins.clearPluginList()
    plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))


# language
locl = "ar", "ae", "bh", "dz", "eg", "in", "iq", "jo", "kw", "lb", "ly", "ma", "om", "qa", "sa", "sd", "ss", "sy", "tn", "ye"
global lngx
lngx = 'en'
try:
    from Components.config import config
    lngx = config.osd.language.value
    lngx = lngx[:-3]
except:
    lngx = 'en'
    pass

global HALIGN

HALIGN = RT_HALIGN_LEFT


def add_skin_font():
    global HALIGN
    from enigma import addFont
    FNTPath = os_path.join(plugin_path + "/fonts")
    # addFont(filename, name, scale, isReplacement, render)
    if any(s in lngx for s in locl):
        HALIGN = RT_HALIGN_RIGHT
        addFont((FNTPath + '/DejaVuSans.ttf'), 'lsat', 100, 1)
        addFont((FNTPath + '/DejaVuSans.ttf'), 'lmsat', 100, 1)
        addFont((FNTPath + '/DejaVuSans.ttf'), 'lbsat', 100, 1)
    else:
        addFont((FNTPath + '/ls-regular.ttf'), 'lsat', 100, 1)
        addFont((FNTPath + '/ls-medium.ttf'), 'lmsat', 100, 1)
        addFont((FNTPath + '/ls-medium.ttf'), 'lbsat', 100, 1)


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
    import sys
    try:

        output = base64.b64decode(s)
        if sys.version_info[0] == 3:
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
        if sys.version_info[0] == 3:
            output = output.decode('utf-8')
        return output


# self.token = "ZUp6enk4cko4ZzBKTlBMTFNxN3djd25MOHEzeU5Zak1Bdkd6S3lPTmdqSjhxeUxMSTBNOFRhUGNBMjBCVmxBTzlBPT0K"
# def check(self, token):
    # result = base64.b64decode(token)
    # result = zlib.decompress(base64.b64decode(result))
    # result = base64.b64decode(result).decode()
    # return result
