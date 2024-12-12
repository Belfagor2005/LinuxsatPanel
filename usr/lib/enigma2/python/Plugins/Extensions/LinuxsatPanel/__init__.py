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
from __future__ import absolute_import
__author__ = "Lululla"
__email__ = "ekekaz@gmail.com"
__copyright__ = 'Copyright (c) 2024 Lululla'
__license__ = "GPL-v2"
__version__ = "1.0.0"

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
AgentRequest = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'
infourl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/info.txt'
abouturl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/about.txt'
xmlurl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/addons_2024.xml'
# xmlurl = 'https://raw.githubusercontent.com/Belfagor2005/upload/main/fill/addons_20242.xml'
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9MaW51eHNhdFBhbmVsL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvTGludXhzYXRQYW5lbA=='

ListUrl = ['https://bosscccam.co/Test.php',
           'https://iptv-15days.blogspot.com',
           'https://cccamia.com/free-cccam',
           'https://cccam.net/freecccam']


isDreamOS = False
if os.path.exists("/usr/bin/apt-get"):
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
    if isDreamOS:
        lang = language.getLanguage()[:2]
        os.environ["LANGUAGE"] = lang
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreamOS:
    def _(txt):
        return gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
else:
    def _(txt):
        translated = gettext.dgettext(PluginLanguageDomain, txt)
        if translated:
            return translated
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


def RequestUrl():
    from random import choice
    RandomUrl = choice(ListUrl)
    return RandomUrl


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


try:
    wgetsts()
except:
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


# Use the feature to get the text and update the interface
def fetch_url(url, retries=3, initial_timeout=5):
    import sys
    import socket
    if sys.version_info[0] == 3:
        from urllib.request import (urlopen)
        from urllib.error import URLError
        # unicode = str
        PY3 = True
    else:
        from urllib2 import (urlopen)
        from urllib2 import URLError
    timeout = initial_timeout
    for i in range(retries):
        try:
            fp = urlopen(url, timeout=timeout)
            lines = fp.readlines()
            fp.close()
            labeltext = ""
            for line in lines:
                if PY3:
                    line = line.decode()  # Decode bytes to str in Python 3
                labeltext += str(line)
            return labeltext
        except socket.timeout:
            print("Attempt failed: The connection timed out after %s seconds." % timeout)
            timeout *= 2  # Double the timeout for the next attempt
        except URLError as e:
            print("URL Error:", e)
            break
        except Exception as e:
            print("Error:", e)
            break
    return None


def checkGZIP(url):
    url = url
    from io import StringIO
    import gzip
    import requests
    import sys
    if sys.version_info[0] == 3:
        from urllib.request import (urlopen, Request)
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


def make_request(url, max_retries=3, base_delay=1):
    import time
    import socket
    import sys
    # import six

    if sys.version_info[0] == 3:
        from urllib.request import (urlopen, Request)
        from urllib.error import URLError
    else:
        from urllib2 import (urlopen, Request)
        from urllib2 import URLError

    for attempt in range(max_retries):
        try:
            req = Request(url)
            req.add_header('User-Agent', AgentRequest)
            # start_time = time.time()
            response = urlopen(req, None, 30)
            # elapsed_time = time.time() - start_time
            # print('elapsed_time:', elapsed_time)
            if response.getcode() == 200:
                content = response.read()
                if not content:
                    return None
                try:
                    content = content.decode('utf-8')
                except UnicodeDecodeError:
                    print("Decoding error with 'utf-8', trying 'latin-1'...")
                    content = content.decode('latin-1', errors='replace')
                # try:
                    # content = six.ensure_str(content, errors='replace')
                # except UnicodeDecodeError:
                    # print("Decoding error with 'utf-8', trying 'latin-1'...")
                    # content = content.decode('latin-1', errors='replace')
                print("Contenuto decodificato con latin-1:\n", content)
                return content
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                delay = base_delay * (2 ** attempt)
                # print("Timeout occurred. Retrying in seconds...", str(delay))
                time.sleep(delay)
            else:
                print("URLError occurred:", str(e))
                return None
    print("Max retries reached.")
    return None


def newOE():
    # coded by s3n0
    '''
    return True ---- for commercial versions of Enigma2 core (OE 2.2+) - DreamElite, DreamOS, Merlin, ... etc.
    return False --- for open-source versions of Enigma2 core (OE 2.0 or OE-Alliance 4.x) - OpenATV, OpenPLi, VTi, ... etc.
    '''
    # return os.path.exists('/etc/dpkg')
    boo = False
    try:
        from enigma import PACKAGE_VERSION
        major, minor, patch = [int(n) for n in PACKAGE_VERSION.split('.')]
        if major > 4 or (major == 4 and minor >= 2):  # if major > 4 or major == 4 and minor >= 2:
            boo = True  # new enigma core (DreamElite, DreamOS, Merlin, ...) ===== e2 core: OE 2.2+ ====================== (c)Dreambox core
    except Exception:
        pass
    try:
        from Components.SystemInfo import SystemInfo
        if 'MachineBrand' in SystemInfo.keys and 'TeamBlue' in SystemInfo['MachineBrand']:
            boo = False
    except Exception:
        pass
    try:
        from boxbranding import getOEVersion
        if getOEVersion().find('OE-Alliance') >= 0:
            boo = False
    except Exception:
        pass
    return boo


# self.token = "ZUp6enk4cko4ZzBKTlBMTFNxN3djd25MOHEzeU5Zak1Bdkd6S3lPTmdqSjhxeUxMSTBNOFRhUGNBMjBCVmxBTzlBPT0K"
# def check(self, token):
    # result = base64.b64decode(token)
    # result = zlib.decompress(base64.b64decode(result))
    # result = base64.b64decode(result).decode()
    # return result
