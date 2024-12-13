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
from __future__ import print_function
from os.path import isfile

__author__ = "Lululla"
__email__ = "ekekaz@gmail.com"
__copyright__ = 'Copyright (c) 2024 Lululla'
__license__ = "GPL-v2"
__version__ = "1.0.0"


def newOE():
    '''
    coded by s3n0
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


def ctrlSkin(pank, skin):
    # coded by @Lululla 20240720
    from re import sub
    print('ctrlSkin panel=%s' % pank)
    # Keywords to identify when to remove "font" and "scrollbarWidth"
    scrollbar_keywords = ['list', 'menu', 'config']
    # 'tasklist', 'menulist', 'menu_list', 'filelist', 'file_list', 'entries', 'Listbox', 'list_left', 'list_right', 'streamlist', 'tablist', 'HelpScrollLabel']
    if newOE() or isfile('/etc/opkg/nn2-feed.conf'):  # Condition for Enigma2 version
        if 'scrollbarWidth' in skin:
            skin = sub(r'scrollbarWidth="[^"]*"', '', skin)
        for keyword in scrollbar_keywords:
            # Search for "scrollbarMode" with one of the associated values ​​(list, menu, config)
            if 'scrollbarMode="%s"' % keyword in skin:
                # print('Found keyword scrollbarMode:', keyword)
                # Remove "font=" from the line
                skin = sub(r'font="[^"]*"', '', skin)
        # print('Skin modded:', skin)
    else:
        # No changes to the content of `skin`
        skin = skin
    return skin
