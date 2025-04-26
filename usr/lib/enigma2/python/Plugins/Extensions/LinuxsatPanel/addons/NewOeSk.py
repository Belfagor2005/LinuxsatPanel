#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
# ═════════════════════════════════════════════════════════════════════
#
#  UTILITY SKIN
#  Version: 5.4
#  Created by Lululla (https://github.com/Belfagor2005)
#  License: CC BY-NC-SA 4.0
#  https://creativecommons.org/licenses/by-nc-sa/4.0
#
#  Last Modified: "15:14 - 20250423"
#
#  Credits:
#
# 👨‍💻 Original Developers: Lululla
# ✍️ (2024-07-20)
#
# ⚖️ License: GNU General Public License (v2 or later)
#    You must NOT remove credits and must share modified code.
# ═════════════════════════════════════════════════════════════════════
from re import search
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


patterns_to_remove = [
	r'scrollbarWidth="[^"]*"',
	r'scrollbarSliderBorderWidth="[^"]*"',
	r'textoffsets\s*="[^"]*"',
	r'secondfont\s*="[^"]*"',
	r'scrollbarBorderWidth="[^"]*"',
	r'scrollbarForegroundColor="[^"]*"',
	r'scrollbarBorderColor="[^"]*"'
]

# scrollbarMode="
patterns_to_remove = [
	r'scrollbarWidth="[^"]*"',
	r'scrollbarSliderBorderWidth="[^"]*"',
	r'textoffsets\s*="[^"]*"',
	r'secondfont\s*="[^"]*"',
	r'scrollbarBorderWidth="[^"]*"',
	r'scrollbarForegroundColor="[^"]*"',
	r'scrollbarBorderColor="[^"]*"'
]


scrollbar_keywords_patterns = [
	r'scrollbarMode="list"',
	r'scrollbarMode="text"',
	r'scrollbarMode="menu"',
	r'scrollbarMode="config"',
	r'scrollbarMode="tasklist"',
	r'scrollbarMode="menulist"',
	r'scrollbarMode="menu_list"',
	r'scrollbarMode="filelist"',
	r'scrollbarMode="file_list"',
	r'scrollbarMode="entries"',
	r'scrollbarMode="Listbox"',
	r'scrollbarMode="list_left"',
	r'scrollbarMode="list_right"',
	r'scrollbarMode="streamlist"',
	r'scrollbarMode="tablist"',
	r'scrollbarMode="HelpScrollLabel"',
]


# scrollbarMode="
def ctrlSkin(pank, skin):
	from re import sub
	print('ctrlSkin panel=%s' % pank)
	# Edit only if `newOE()` is True or `/etc/opkg/nn2-feed.conf` exists
	if newOE() or isfile('/etc/opkg/nn2-feed.conf') or isfile("/usr/bin/apt-get"):
		for pattern in patterns_to_remove:
			skin = sub(pattern, '', skin)
		# Remove "font" only if a scrollbarMode pattern is found
		for pattern in scrollbar_keywords_patterns:
			if search(pattern, skin):  # If any pattern in scrollbar_keywords is found
				skin = sub(r'font="[^"]*"', '', skin)  # Remove font
		# print('Skin modified:\n', skin)
	else:
		print('No Skin modifications applied.')
	return skin


"""
# def ctrlSkin(pank, skin):
	# from re import sub
	# print('ctrlSkin panel=%s' % pank)
	# scrollbar_keywords = ['list', 'text', 'menu', 'config', 'tasklist', 'menulist']  # , 'menu_list', 'filelist', 'file_list', 'entries', 'Listbox', 'list_left', 'list_right', 'streamlist', 'tablist', 'HelpScrollLabel']
	# # Edit only if `newOE()` is True or `/etc/opkg/nn2-feed.conf` exists
	# if newOE() or isfile('/etc/opkg/nn2-feed.conf') or isfile("/usr/bin/apt-get"):
		# for pattern in patterns_to_remove:
			# skin = sub(pattern, '', skin)
		# # Remove "font" only if a widget has `scrollbarMode` with one of the specific values
		# for keyword in scrollbar_keywords:
			# if 'scrollbarMode="' in skin:  # Cerca scrollbarMode nel widget
				# skin = sub(r'font="[^"]*"', '', skin)

		# # print('Skin modified:\n', skin)
	# else:
		# print('no Skin modifies a change to the contents of `skin.')
	# return skin
"""
