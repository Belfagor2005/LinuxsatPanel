#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#  Linuxsat Panel v2.8.5 - Professional Addons Manager    #
#  Created by: masterG, oktus, pcd                        #
#  Rewritten by: Lululla (2024-07-20)                     #
###########################################################

MAIN FEATURES:
• Comprehensive plugin/skin/script installer for Enigma2
• Support for both OE2.0 (ipkg) and OE2.2/2.5/2.6 (dpkg) systems
• Multi-resolution support (HD, FHD, WQHD)
• Interactive grid-based navigation with visual feedback
• Integrated console output viewer for installation logs
• Free server line integration (CCcam/Oscam)
• LCN Scanner for channel ordering
• Skin component checker
• Direct script execution from GitHub repositories

NEW IN v2.8.4:
UNIVERSAL ICON NAVIGATION - 20-icon grid with wrap-around navigation
INTELLIGENT CATEGORY SORTING - A-Z sorting with preservation of original order
REAL-TIME SPACE MONITORING - Free space display during installation
AUTO-UPDATE CHECKER - Background version checking with notification
MULTI-SOURCE SUPPORT - XML-based plugin database + direct GitHub scripts
ADVANCED ERROR HANDLING - Comprehensive error reporting and recovery

KEY CONTROLS - MAIN GRID:
OK     - Open selected category/execute action
EXIT   - Open About/Exit panel
RED    - Exit to About screen
0      - Toggle A-Z/Default sorting
LEFT   - Move left in grid (wrap-around)
RIGHT  - Move right in grid (wrap-around)
UP     - Move up 5 positions (wrap-around)
DOWN   - Move down 5 positions (wrap-around)
INFO   - Show system information
MENU   - Open About/Exit panel

UNIVERSAL NAVIGATION CONTROLS (ALL SCREENS):
• 20-item grid with visual frame indicator
• Multi-page support for large categories
• Page indicators and position tracking
• Quick jump to first/last item
• Position-based highlighting

INSTALLATION SYSTEM:
• Support for .ipk (OE2.0), .deb (OE2.2+), .zip, .tar, .gz, .bz2
• Automatic dependency handling
• Installation status checking (already installed detection)
• Safe removal with dependency checking
• Console output capture and display

SPECIAL FEATURES:
• Ciefp Installer - Direct installation of all Ciefp plugins
• Channel Lists - Multiple provider support (CIEFP, CYRUS, MANUTEK, etc.)
• Script Installer - One-click installation of 40+ community scripts
• Free Line Integration - Automatic C-line retrieval and configuration
• LCN Scanner - Automatic channel numbering for terrestrial
• Skin Checker - Verify skin component availability
• File Commander - Integrated file browser for logs

CATEGORY STRUCTURE:
1.  Backup Tools (OE2.0 only)
2.  Bouquets Tools (OE2.0 only)
3.  Channel List (multi-provider)
4.  Ciefp (specialized installer)
5.  DvbUsb Tuners Drivers (OE2.0 only)
6.  Epg Tools (OE2.0 only)
7.  Feeds Image (OE2.0 / OE2.2+)
8.  Games Tools (OE2.0 only)
9.  Iptv Tools (OE2.0 only)
10. KiddaC (OE2.0 / OE2.2+)
11. Lululla Zone (OE2.0 / OE2.2+)
12. Mediaplayer-Youtube (OE2.0 only)
13. MultiBoot Tools (OE2.0 only)
14. Multimedia Tools (OE2.0 only)
15. Panels Addons (OE2.0 only)
16. Picons Tools (OE2.0 only)
17. Python Library (OE2.0 only)
18. Radio Tools (OE2.0 only)
19. Script Installer (universal)
20. Skins (TEAM / FHD-HD)
21. Keys Tools (OE2.0 / OE2.2+)
22. Softcams (OE2.0 / OE2.2+)
23. Sport Tools (OE2.0 only)
24. Streamlink Tools (OE2.0 only)
25. Utility Tools (OE2.0 only)
26. Vpn Tools (OE2.0 only)
27. WeatherTools (OE2.0 only)
28. WeatherForecast (OE2.0 only)
29. Webcam Tools (OE2.0 only)
30. Adult (parental control protected)
31. Other (miscellaneous)
32. Information (system info)
33. About (credits & license)

SCRIPT INSTALLER HIGHLIGHTS:
• Add Libssl Libcrypto - Compatibility libraries
• Ajpanel - Alternative panel interface
• Arabic Savior - Arabic language support
• Biss Feed Autokey - Automatic BISS key updates
• Chocholousek Picons - Popular picon sets
• DNS Services - Cloudflare, Google, Quad9
• E2iPlayer variants - Multiple repository options
• EPGImport sources - EPG data importers
• History Zap Selector - Channel history navigation
• IPaudio Pro - Audio streaming enhancements
• Key management - Adders and updaters
• MultiStalker Pro - IPTV streaming
• Oscam generators - Multiple source configurations
• QuickSignal - Signal monitoring
• WireGuard VPN - Secure connections
• XC Forever - IPTV client
• Xstreamity - Streaming client
• Xtraevent - Event system enhancements

TECHNICAL ARCHITECTURE:
• Multi-threaded XML parsing with GZIP support
• SSL/TLS certificate handling for secure connections
• Dynamic skin loading based on resolution
• Font embedding for consistent typography
• Plugin refresh system for Enigma2 integration
• Configurable alignment (left/right) for RTL languages
• Screen inheritance for consistent UI behavior
• Timer-based background operations

DATABASE & SOURCES:
• Primary: XML from linuxsat-support.com (gzip compressed)
• Secondary: Direct GitHub raw URLs
• Tertiary: Provider-specific XML feeds
• Local: Cached configurations and scripts

CONFIGURATION:
• Automatic detection of OE version (ipkg/dpkg)
• Resolution detection (HD/FHD/WQHD)
• Parental control integration
• Network connectivity checking
• Update notification preferences

ERROR HANDLING:
• Network timeout management
• File system permission handling
• Package manager compatibility checks
• Skin component validation
• Memory and disk space monitoring

PERFORMANCE OPTIMIZATIONS:
• Lazy loading of icons and graphics
• Cached XML data parsing
• Background version checking
• Efficient grid rendering
• Minimal memory footprint

SECURITY FEATURES:
• SSL certificate verification (optional)
• Parental control for adult content
• Safe script execution with user confirmation
• File permission management
• Input validation for URLs and commands

VERSION HISTORY:
v1.0 - Basic plugin installer
v2.0 - Grid interface implementation
v2.5 - Multi-version support (OE2.0/OE2.2+)
v2.6 - Script installer integration
v2.7 - Ciefp specialized installer
v2.8 - Universal navigation system
v2.8.4 - Current stable version
v2.8.5 - Current stable version

Last Updated: 2024-12-31
Status: Production Stable
Credits: masterG, oktus, pcd (original), Lululla (rewrite)
Homepage: www.linuxsat-support.com
Support: Forum @ linuxsat-support.com
Donations: PayPal to project maintainers
License: GPL v2
###########################################################
"""

import codecs
import io
from datetime import datetime as dt
from json import loads
from re import compile, search, DOTALL
from shutil import copy2
from sys import version_info

from os import R_OK, access, chmod, makedirs, system, walk
from os.path import exists, join

import six
import requests
from six.moves.urllib.error import URLError
from six.moves.urllib.request import Request, urlopen

from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest, MultiContentEntryText
from Components.Pixmap import MovingPixmap, Pixmap
from Components.PluginComponent import plugins
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import SCOPE_PLUGINS, fileExists, resolveFilename
from enigma import (
	RT_HALIGN_RIGHT,
	RT_VALIGN_CENTER,
	eListboxPythonMultiContent,
	ePicLoad,
	eTimer,
	gFont,
	loadPNG,
)

from . import (
	_,
	AgentRequest,
	CheckConn,
	add_skin_fonts,
	b64decoder,
	checkGZIP,
	check_version,
	developer_url,
	freespace,
	installer_url,
	isWQHD,
	isFHD,
	isHD,
	PY3,
	RequestUrl,
	make_request,
	refreshPlugins,
	xmlurl,
	HALIGN,
	__version__,
	descplug,
	# __author__
)
from .addons.NewOeSk import ctrlSkin
from .lsConsole import lsConsole
from .LCNScanner.plugin import LCNScanner
from .LCNScanner.Lcn import (
	ReloadBouquets,
	copy_files_to_enigma2,
	keepiptv,
	terrestrial,
)


global HALIGN
global setx
global skin_path
global has_dpkg


# constants
_session = None
has_dpkg = False
setx = 0
skin_path = ""
if exists("/usr/bin/apt-get"):
	has_dpkg = True
plugin_path = resolveFilename(
	SCOPE_PLUGINS,
	"Extensions/{}".format("LinuxsatPanel")
)


if PY3:
	import html

	def decode_html(text):
		return html.unescape(text)
else:
	from HTMLParser import HTMLParser
	html_parser = HTMLParser()

	def decode_html(text):
		return html_parser.unescape(text)


if version_info >= (2, 7, 9):
	try:
		import ssl
		sslContext = ssl._create_unverified_context()
	except:
		sslContext = None


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


if isWQHD() or isFHD():
	skin_path = plugin_path + "/skins/fhd"
	picfold = plugin_path + "/LSicons2/"
	pngx = plugin_path + "/icons2/link.png"
	nss_pic = picfold + "LSS.png"
else:
	skin_path = plugin_path + "/skins/hd"
	picfold = plugin_path + "/LSicons/"
	pngx = plugin_path + "/icons/link.png"
	nss_pic = picfold + "LSS.png"


# menulist
class LPSlist(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, True, eListboxPythonMultiContent)
		if isWQHD() or isFHD():
			self.l.setItemHeight(50)
			textfont = int(34)
			self.l.setFont(0, gFont("lsat", textfont))
		if isHD():
			self.l.setItemHeight(35)
			textfont = int(22)
			self.l.setFont(0, gFont("lsat", textfont))


def LPListEntry(name, item):
	res = [(name, item)]

	if not fileExists(pngx):
		return res

	png = loadPNG(pngx)

	if isWQHD() or isFHD():
		icon_size = (40, 40)
		text_size = (930, 50)
		icon_x_right = 940
		icon_x_left = 5
		text_x_left = 55
	else:
		icon_size = (30, 30)
		text_size = (590, 35)
		icon_x_right = 640
		icon_x_left = 5
		text_x_left = 45

	if HALIGN == RT_HALIGN_RIGHT:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(icon_x_right, 5), size=icon_size, png=png))
		res.append(MultiContentEntryText(pos=(5, 0), size=text_size, font=0, text=name, flags=HALIGN | RT_VALIGN_CENTER))
	else:
		res.append(MultiContentEntryPixmapAlphaTest(pos=(icon_x_left, 5), size=icon_size, png=png))
		res.append(MultiContentEntryText(pos=(text_x_left, 0), size=text_size, font=0, text=name, flags=HALIGN | RT_VALIGN_CENTER))

	return res


def LPshowlist(data, list):
	plist = [LPListEntry(name, index) for index, name in enumerate(data)]
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


def add_menu_item(menu_list, titles, pics, urls, title, pic_name, url=""):
	menu_list.append(title)
	titles.append(title.strip())
	pics.append(picfold + pic_name)
	urls.append(url)  # add missing string for URL


class LinuxsatPanel(Screen):

	def __init__(self, session):

		Screen.__init__(self, session)
		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LinuxsatPanel.xml")
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
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Backup Tools ", "Backup.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Bouquets Tools ", "Bouquets.png")

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Channel List ", "Channel-list.png")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Ciefp ", "ciefp.png")
		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "DvbUsb Tuners Drivers", "usb-tuner-drivers.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Epg Tools ", "plugin-epg.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Feeds Image OE2.0 ", "Feeds2.0.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Feeds Image OE2.2/2.5/2.6 ", "Feeds2.2.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Games Tools ", "Game.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Iptv Tools ", "iptv-streaming.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "KiddaC OE2.0 ", "KiddaC1.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "KiddaC OE2.2/2.5/2.6 ", "KiddaC2.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Lululla Zone OE2.0 ", "oe2.0.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Lululla Zone OE2.2/2.5/2.6 ", "oe2.5-2.6.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Plugins OE2.2/2.5/2.6 ", "OE2.2-Plugins.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Mediaplayer-Youtube ", "mediayou.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "MultiBoot Tools ", "multiboot.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Multimedia Tools ", "Multimedia.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Panels Addons ", "Panels.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Picons Tools ", "picons.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Python Library ", "Library.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Radio Tools", "Radio.png")

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Script Installer ", "script.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins | TEAM ", "skinsteam.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Skins Fhd-Hd OE2.2/2.5/2.6 ", "OE2.2-Skins.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Tools OE2.0 ", "key-updater.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Tools OE2.2/2.5/2.6 ", "key-updater1.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Softcams OE2.0 ", "SOE20.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Softcams OE2.2/2.5/2.6 ", "SOE22.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Sport Tools ", "sport.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Streamlink Tools ", "streamlink.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Utility Tools ", "utility.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Vpn Tools ", "vpn.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "WeatherTools ", "weather.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "WeatherForecast ", "weather-forecast.png")
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Webcam Tools ", "webcam.png")

		if not config.ParentalControl.configured.value:
			if not has_dpkg:
				add_menu_item(menu_list, self.titles, self.pics, self.urls, "Adult OE2.0 ", "18+deb.png")
			else:
				add_menu_item(menu_list, self.titles, self.pics, self.urls, "Adult OE2.2/2.5/2.6 ", "18+.png")

		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Other OE2.0 ", "Other.png")
		else:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "Other OE2.2/2.5/2.6 ", "Other1.png")

		add_menu_item(menu_list, self.titles, self.pics, self.urls, " Information ", "Information.png")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, " About ", "about.png")

		self.names = menu_list
		self.sorted = False
		# self.combined_data = list(zip(self.names, self.titles, self.pics, self.urls))
		self["frame"] = MovingPixmap()
		self["info"] = Label()
		self["info"].setText(_("Please Wait..."))
		self["sort"] = Label(_("Sort A-Z"))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"MenuActions",
				"DirectionActions",
				"NumberActions",
				"ColorActions",
				"EPGSelectActions",
				"InfoActions"
			],
			{
				"ok": self.okbuttonClick,
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
				"menu": self.closeRecursive
			},
			-1
		)

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
		# self.onLayoutFinish.append(self.start_check_version)

	def start_check_version(self):
		self.Update = False
		self.new_version, self.new_changelog, update_available = check_version(
			__version__, installer_url, AgentRequest
		)
		if update_available:
			self.Update = True
			print("A new version is available:", self.new_version)

			# Check if current screen is modal before opening the MessageBox
			if self.session.current_dialog and getattr(self.session.current_dialog, "isModal", lambda: False)():
				msg = _("New version available\n\nChangelog:\n\nPress the green button to start the update.")
				msg = msg.replace("available", "available %s" % self.new_version)
				msg = msg.replace("Changelog:", "Changelog: %s" % self.new_changelog)
				self.session.open(
					MessageBox,
					msg,
					MessageBox.TYPE_INFO,
					timeout=5
				)
			else:
				msg = _("New version available\n\nChangelog:\n\nBut not downloadable!!!")
				msg = msg.replace("available", "available %s" % self.new_version)
				msg = msg.replace("Changelog:", "Changelog: %s" % self.new_changelog)
				self.session.open(
					MessageBox,
					msg,
					MessageBox.TYPE_INFO,
					timeout=5
				)
		else:
			print("No new version available.")

	def paintFrame(self):
		try:
			# If the index exceeds the maximum number of items, it returns to the first item
			if self.index > self.maxentry:
				self.index = self.minentry
			self.idx = self.index
			name = self.names[self.idx]
			self["info"].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print("Error in paintFrame: ", e)

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
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(nss_pic)
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
			if not exists(self.pics[idx]):
				pic = nss_pic
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
		if self.index == 0 and self.ipage == 1:
			self.ipage = self.npage
			self.index = self.minentry
			self.openTest()

		elif self.index >= 5 and not self.ipage == self.npage and self.index == self.minentry:
			self.index -= 5
		else:
			if self.ipage == self.npage and self.index == self.minentry:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage == self.npage:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage += 1
				self.index = self.minentry
				self.openTest()

		self.paintFrame()

	def keyNumberGlobal(self, number):
		number -= 1
		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def list_sort(self):
		if not hasattr(self, "original_data"):
			self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
			self.sorted = False

		if self.sorted:
			self.names, self.titles, self.pics, self.urls = self.original_data
			self.sorted = False
			self["sort"].setText(_("Sort A-Z"))
		else:
			self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
			self.sorted = True
			self["sort"].setText(_("Sort Default"))

		self.openTest()

	def refreshPlugins(self):
		plugins.clearPluginList()
		plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))

	def closeRecursive(self):
		if not has_dpkg:
			self.refreshPlugins()
		self.session.openWithCallback(self.close, AboutLSS)

	def closeNonRecursive(self):
		self.session.openWithCallback(self.close, AboutLSS)

	def createSummary(self):
		return

	def key_info(self):
		self.session.open(LSinfo, " Information ")

	def okbuttonClick(self):
		self.idx = self.index
		if self.idx is None:
			return
		name = self.names[self.idx]
		if "adult" in name.lower():
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("These Panel may contain Adult content\n\nare you sure you want to continue?"))
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

		elif name == "Ciefp ":
			self.session.open(CiefpInstaller, name)

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
				self.session.open(
					MessageBox, _("Error: No Data Find."),
					MessageBox.TYPE_ERROR
				)


class LSskin(Screen):

	def __init__(self, session, name):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LinuxsatPanel.xml")
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
		self["info"] = Label()
		self["info"].setText(_("Please Wait..."))
		self["sort"] = Label(_("Sort A-Z"))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"MenuActions",
				"DirectionActions",
				"NumberActions",
				"ColorActions",
				"EPGSelectActions",
				"InfoActions"
			],
			{
				"ok": self.okbuttonClick,
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
				"menu": self.closeRecursive
			},
			-1
		)

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
			self["info"].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print("Error in paintFrame: ", e)

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
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(nss_pic)
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
			if not exists(self.pics[idx]):
				pic = nss_pic
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
		if self.index == 0 and self.ipage == 1:
			self.ipage = self.npage
			self.index = self.minentry
			self.openTest()

		elif self.index >= 5 and not self.ipage == self.npage and self.index == self.minentry:
			self.index -= 5
		else:
			if self.ipage == self.npage and self.index == self.minentry:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage == self.npage:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage += 1
				self.index = self.minentry
				self.openTest()

		self.paintFrame()

	def keyNumberGlobal(self, number):
		number -= 1
		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def list_sort(self):
		if not hasattr(self, "original_data"):
			self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
			self.sorted = False

		if self.sorted:
			self.names, self.titles, self.pics, self.urls = self.original_data
			self.sorted = False
			self["sort"].setText(_("Sort A-Z"))
		else:
			self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
			self.sorted = True
			self["sort"].setText(_("Sort Default"))

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
			self.session.open(
				MessageBox, _("Error: No Data Find."),
				MessageBox.TYPE_ERROR
			)


class LSChannel(Screen):

	def __init__(self, session, name):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LinuxsatPanel.xml")
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
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CIEFP ", "ciefp.png", "https://github.com/ciefp/ciefpsettings-enigma2-zipped")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CYRUS ", "cyrus.png", "http://www.cyrussettings.com/Set_29_11_2011/Dreambox-IpBox/Config.xml")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "MANUTEK ", "manutek.png", "http://www.manutek.it/isetting/index.php")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "MORPHEUS ", "morpheus883.png", "http://github.com/morpheus883/enigma2-zipped")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "VHANNIBAL NET ", "vhannibal1.png", "http://www.vhannibal.net/asd.php")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "VHANNIBAL TEK ", "vhannibal2.png", "http://sat.alfa-tech.net/upload/settings/vhannibal/")

		self.names = menu_list
		# self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
		self["frame"] = MovingPixmap()
		self["info"] = Label()
		self["info"].setText(_("Please Wait..."))
		self["sort"] = Label(_("Sort A-Z"))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"MenuActions",
				"DirectionActions",
				"NumberActions",
				"ColorActions",
				"EPGSelectActions",
				"InfoActions"
			],
			{
				"ok": self.okbuttonClick,
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
				"menu": self.closeRecursive
			},
			-1
		)

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
			self["info"].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print("Error in paintFrame: ", e)

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
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(nss_pic)
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
			if not exists(self.pics[idx]):
				pic = nss_pic
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
		if self.index == 0 and self.ipage == 1:
			self.ipage = self.npage
			self.index = self.minentry
			self.openTest()

		elif self.index >= 5 and not self.ipage == self.npage and self.index == self.minentry:
			self.index -= 5
		else:
			if self.ipage == self.npage and self.index == self.minentry:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage == self.npage:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage += 1
				self.index = self.minentry
				self.openTest()

		self.paintFrame()

	def keyNumberGlobal(self, number):
		number -= 1
		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def list_sort(self):
		if not hasattr(self, "original_data"):
			self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
			self.sorted = False

		if self.sorted:
			self.names, self.titles, self.pics, self.urls = self.original_data
			self.sorted = False
			self["sort"].setText(_("Sort A-Z"))
		else:
			self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
			self.sorted = True
			self["sort"].setText(_("Sort Default"))

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
		self.session.open(addInstall, url, name, "")


class CiefpInstaller(Screen):

	def __init__(self, session, name):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LinuxsatPanel.xml")
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

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpBouquetUpdater",          "ciefp_bu.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpBouquetUpdater/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpChannelManager",          "ciefp_cman.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpChannelManager/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpE2Converter",             "ciefp_ec.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpE2Converter/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpIptvBouquets",            "ciefp_ib.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpIPTVBouquets/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpMojTvEPG",                "ciefp_mojtvepg.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpMojTvEPG/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpOpenDirectory",           "ciefp_opdir.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpOpenDirectories/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpOscamEditor",             "ciefp_oe.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpOscamEditor/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSatelliteAnalizer",       "ciefp_satan.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSatelliteAnalyzer/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSatelliteXmlEditor",      "ciefp_xed.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSatelliteXmlEditor/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSelectSatellite",         "ciefp_ss.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSelectSatellite/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSettingsDownloader",      "ciefp_sd.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsDownloader/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSettingsStreamrelay PY2", "ciefp_sr2.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelayPY2/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSettingsStreamrelay PY3", "ciefp_sr3.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelay/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSettingsT2miAbertis PLi", "ciefp_t2mpli.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertisOpenPLi/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpSettingsT2miAbertis",     "ciefp_t2m.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpTMDBSearch",              "ciefp_tmdb.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpTMDBSearch/main/installer.sh  -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpVibes",                   "ciefp_vibes.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpVibes/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpWhitelistStreamrelay",    "ciefp_wls.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpWhitelistStreamrelay/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpsettingsMotor",           "ciefp_sm.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsMotor/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "CiefpsettingsPanel",           "ciefp_sp.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh")
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "WebCamE2PrenjSF",              "ciefp_webcam.png", "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/WebCamE2PrenjSF/main/installer.sh -O - | /bin/sh")

		self.names = menu_list
		self.sorted = False
		# self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
		self["frame"] = MovingPixmap()
		self["info"] = Label()
		self["info"].setText(_("Please Wait..."))
		self["sort"] = Label(_("Sort A-Z"))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"MenuActions",
				"DirectionActions",
				"NumberActions",
				"ColorActions",
				"EPGSelectActions",
				"InfoActions"
			],
			{
				"ok": self.okbuttonClick,
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
				"menu": self.closeRecursive
			},
			-1
		)

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

	def openVi(self, callback=""):
		from .addons.File_Commander import File_Commander
		user_log = "/tmp/my_debug.log"
		if fileExists(user_log):
			self.session.open(File_Commander, user_log)

	def paintFrame(self):
		try:
			# If the index exceeds the maximum number of items, it returns to the first item
			if self.index > self.maxentry:
				self.index = self.minentry
			self.idx = self.index
			name = self.names[self.idx]
			self["info"].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print("Error in paintFrame: ", e)

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
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(nss_pic)
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
			if not exists(self.pics[idx]):
				pic = nss_pic
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
		if self.index == 0 and self.ipage == 1:
			self.ipage = self.npage
			self.index = self.minentry
			self.openTest()

		elif self.index >= 5 and not self.ipage == self.npage and self.index == self.minentry:
			self.index -= 5
		else:
			if self.ipage == self.npage and self.index == self.minentry:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage == self.npage:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage += 1
				self.index = self.minentry
				self.openTest()

		self.paintFrame()

	def keyNumberGlobal(self, number):
		number -= 1
		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def list_sort(self):
		if not hasattr(self, "original_data"):
			self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
			self.sorted = False

		if self.sorted:
			self.names, self.titles, self.pics, self.urls = self.original_data
			self.sorted = False
			self["sort"].setText(_("Sort A-Z"))
		else:
			self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
			self.sorted = True
			self["sort"].setText(_("Sort Default"))

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
		print("[okbuttonClick] idx", idx)
		if idx is None:
			return
		self.namev = self.names[idx]
		self.url = self.urls[idx]
		print("[okbuttonClick] self.namev", self.namev)
		print("[okbuttonClick] self.url", self.url)

		self.session.openWithCallback(self.okClicked, MessageBox, _("I am NOT responsible for any issues you may\nencounter once you install the plugins and skins.\n \
										However, if required, you can get help to resolve the issue.\n\n\nDo you want to execute %s?") % self.namev, MessageBox.TYPE_YESNO, default=True)

	def okClicked(self, answer=False):
		if answer:
			title = (_("Executing %s\nPlease Wait...") % self.namev)
			keywords = ["google", "cloudfaire", "quad9", "emm", "keys", "source"]
			lower_namev = self.namev.lower()
			keyword_found = any(keyword in lower_namev for keyword in keywords)
			if keyword_found:
				cmd = str(self.url) + " > /tmp/my_debug.log 2>&1"
				self.session.open(lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=False)
			else:
				cmd = str(self.url) + " > /tmp/my_debug.log 2>&1"
				self.session.openWithCallback(self.openVi, lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=True)
		else:
			return


class ScriptInstaller(Screen):

	def __init__(self, session, name):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LinuxsatPanel.xml")
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

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Add Libssl Libcrypto", "AddLibssl.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Add_Libssl1_Libcrypto1.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Add Symlink Libssl", "AddSymlink.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Symlink_Creator.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Ajpanel AMAJamry", "Ajpanel.png", 'wget --no-check-certificate "https://raw.githubusercontent.com/biko-73/AjPanel/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Arabic Savior", "arabicsav.png", 'wget --no-check-certificate "https://raw.githubusercontent.com/fairbird/ArabicSavior/main/installer.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Biss Feed Autokey", "BissFeedAutokey.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Bissfeedautokey.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Chocholousek Picons", "ChocholousekPicons.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Chocholousek_picons.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Dns Cloudfaire", "DnsCloudfaire.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsCloudflare.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Dns Google", "DnsGoogle.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsGoogle.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Dns Quad9", "DnsQuad9.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/DnsQuad9.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "E2player E2-MIRROR", "E2iPlayer.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/oe-mirrors/e2iplayer/refs/heads/python3/e2iplayer_install.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "E2player BYKO-73", "E2playerBiko-73.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/biko-73/E2IPlayer/main/installer-tar.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "E2player MAXBAMBY", "E2playerMAXBAMBY.png", 'wget -q --no-check-certificate "https://gitlab.com/maxbambi/e2iplayer/-/raw/master/install-e2iplayer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "E2player ZADMARIO", "E2playerZADMARIO.png", 'wget -q --no-check-certificate "https://gitlab.com/zadmario/e2iplayer/-/raw/master/install-e2iplayer.sh?inline=false" -O - | /bin/sh')
		# add_menu_item(menu_list, self.titles, self.pics, self.urls, "E2player XXX", "E2playerXXX.png", 'wget -q --no-check-certificate "https://gitlab.com/iptv-host-xxx/iptv-host-xxx/-/raw/master/IPTVPlayer/iptvupdate/custom/xxx.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "EPGImport - source", "epgsource.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/EPGImport-99/main/installer_source.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "History Zap Selector", "HistoryZapSelector.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Historyzapselector_dorik.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Ipaudio Pro", "ipaudio.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Ipaudiopro_1.4.sh?inline=false" -O - | /bin/sh')
		# add_menu_item(menu_list, self.titles, self.pics, self.urls, "Ipaudio Pro", "ipaudio.png", 'wget https://raw.githubusercontent.com/biko-73/ipaudio/main/ipaudiopro.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Adder", "keysadd.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/fairbird/KeyAdder/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Keys Update", "keys.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Keys_Updater.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Levi45 Manager", "Levi45Manager.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/levi-45/Manager/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Mountpoints", "Mountpoints.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Mountpoints.sh?inline=false" -O - | /bin/sh')
		# add_menu_item(menu_list, self.titles, self.pics, self.urls, "Multistalker Pro Ziko Biko", "Multistalker.png", 'wget -q --no-check-certificate  "https://raw.githubusercontent.com/biko-73/Multi-Stalker/main/pro/installer.sh -O - | /bin/sh?inline=false" -O - | /bin/sh; wget -q --no-check-certificate "https://gitlab.com/hmeng80/extensions/-/raw/main/multistalker/portal/Portal_multistalker.sh?inline=false" -O - | /bin/sh')
		# add_menu_item(menu_list, self.titles, self.pics, self.urls, "Multistalker Pro Ziko", "MultistalkerPro.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/refs/heads/main/installer.sh?inline=false" -O - | /bin/sh; wget -q --no-check-certificate "https://gitlab.com/hmeng80/extensions/-/raw/main/multistalker/portal/Portal_multistalker.sh?inline=false" | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Multistalker Pro Ziko", "MultistalkerPro.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/refs/heads/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/multisalker_pro12_eliesat.sh?inline=false" -O - | /bin/sh;wget -q --no-check-certificate "https://gitlab.com/hmeng80/extensions/-/raw/main/multistalker/portal/Portal_multistalker.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "New VirtualKeyboard", "NewVirtualKeyboard.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Oscam Generator LINGSAT", "lingsat.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Oscam_srvid_generator_lyngsat.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Oscam Generator KINGOFSAT", "kingofsat.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Oscam_srvid_generator_kingofsat.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Oscam Generator SATELINATV", "satelinatv.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Oscam_srvid_generator_satelitnatv.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Oscam Generator TWOJEIP", "twojeip.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Oscam_srvid_generator_twojeip.sh?inline=false" -O - | /bin/sh')

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Quicksignal Raed", "Quicksignal.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/fairbird/RaedQuickSignal/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "WireGuard Vpn", "WireGuard.png", 'wget -q --no-check-certificate "wget -qO /tmp/WireGuard.sh "https://raw.githubusercontent.com/m4dhouse/Wireguard-Vpn/python-3.12/WireGuard.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "XC Forever", "xc.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/xc_plugin_forever/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Xstreamity", "xstreamity.png", 'wget -q --no-check-certificate https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Xtraevent", "xtraevent.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Xtraevent.sh?inline=false" -O - | /bin/sh')

		# add_menu_item(menu_list, self.titles, self.pics, self.urls, "X-Klass", "xklass.png", 'wget -qO- --no-check-certificate "https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/XKlass/online-setup" | -O - | /bin/sh')

		# Adding more options without URLs
		if not has_dpkg:
			menu_list.append("Lcn Scanner")
			self.titles.append("Search Scanner Lcn channels ")
			self.pics.append(picfold + "LcnSearch.png")
			self.urls.append("")

		menu_list.append("Check Skin Conponent")
		self.titles.append("Search Skin Conponent Image Necessary ")
		self.pics.append(picfold + "CheckSkin.png")
		self.urls.append("")

		menu_list.append("Send Cline -> CCcam.cfg")
		self.titles.append("Send CCcline CCcam ")
		self.pics.append(picfold + "cccamfreee.png")
		self.urls.append("")

		menu_list.append("Send Cline -> oscam.server")
		self.titles.append("Send CCcline Oscam ")
		self.pics.append(picfold + "oscamfree.png")
		self.urls.append("")

		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Send Emm", "SendEmm.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Emm_Sender.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Subsupport addon", "SubSupportAddon.png", 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Subsupport_addon.sh?inline=false" -O - | /bin/sh')
		add_menu_item(menu_list, self.titles, self.pics, self.urls, "Transmission addon", "transmission.png", 'wget -q --no-check-certificate "http://dreambox4u.com/dreamarabia/Transmission_e2/Transmission_e2.sh?inline=false" -O - | /bin/sh')
		if not has_dpkg:
			add_menu_item(menu_list, self.titles, self.pics, self.urls, "ServiceApp Exteplayer", "serviceapp.png", 'opkg update && opkg --force-reinstall --force-overwrite install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp')

		self.names = menu_list
		self.sorted = False
		# self.combined_data = zip(self.names, self.titles, self.pics, self.urls)
		self["frame"] = MovingPixmap()
		self["info"] = Label()
		self["info"].setText(_("Please Wait..."))
		self["sort"] = Label(_("Sort A-Z"))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"MenuActions",
				"DirectionActions",
				"NumberActions",
				"ColorActions",
				"EPGSelectActions",
				"InfoActions"
			],
			{
				"ok": self.okbuttonClick,
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
				"menu": self.closeRecursive
			},
			-1
		)

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
			self.session.openWithCallback(self.Lcn, MessageBox, _("Do you want to Order LCN Bouquet?"), MessageBox.TYPE_YESNO)
		else:
			print("Starting LCN scan...")
			try:
				from .LCNScanner.Terrestrial import PluginSetup
				self.session.open(PluginSetup)
			except Exception as e:
				print("Exception during LCN scan:", e)

	def LcnXX(self, answer=None):
		if answer is None:
			self.session.openWithCallback(self.Lcn, MessageBox, _("Do you want to Order LCN Bouquet?"), MessageBox.TYPE_YESNO)
		else:
			print("Starting LCN scan...")
			try:
				lcn_scanner_instance = LCNScanner()
				LCN = lcn_scanner_instance.lcnScan()
				print("LCN Scanner returned:", LCN)

				if LCN:
					self.session.open(LCN)
				else:
					print("Error: LCN scan did not return a valid screen.")
			except Exception as e:
				print("Exception during LCN scan:", e)

			try:
				self.session.openWithCallback(self._onLCNScanFinished, MessageBox, _("[LCNScanner] LCN scan finished\nChannels Ordered!"), MessageBox.TYPE_INFO, timeout=5)
			except RuntimeError as re:
				print("RuntimeError during MessageBox display:", re)

	def _onLCNScanFinished(self, result=None):
		pass

	def Checkskin(self, answer=None):
		if answer is None:
			self.session.openWithCallback(
				self.Checkskin,
				MessageBox,
				_("[Checkskin] This operation checks if the skin has its components (is not sure)..\nDo you really want to continue?"),
				MessageBox.TYPE_YESNO
			)

		else:
			from .addons import checkskin
			check = checkskin.check_module_skin()
			self.timer = eTimer()
			try:
				self.timer_conn = self.timer.timeout.connect(check)
			except:
				self.timer.callback.append(check)
			self.timer.start(100, True)
			self.openVi()

	def openVi(self, callback=""):
		from .addons.File_Commander import File_Commander
		user_log = "/tmp/my_debug.log"
		if fileExists(user_log):
			self.session.open(File_Commander, user_log)

	def paintFrame(self):
		try:
			# If the index exceeds the maximum number of items, it returns to the first item
			if self.index > self.maxentry:
				self.index = self.minentry
			self.idx = self.index
			name = self.names[self.idx]
			self["info"].setText(str(name))
			ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
			ipos = self.pos[ifr]
			self["frame"].moveTo(ipos[0], ipos[1], 1)
			self["frame"].startMoving()
		except Exception as e:
			print("Error in paintFrame: ", e)

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
				self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(nss_pic)
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
			if not exists(self.pics[idx]):
				pic = nss_pic
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
		if self.index == 0 and self.ipage == 1:
			self.ipage = self.npage
			self.index = self.minentry
			self.openTest()

		elif self.index >= 5 and not self.ipage == self.npage and self.index == self.minentry:
			self.index -= 5
		else:
			if self.ipage == self.npage and self.index == self.minentry:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage = self.npage
				self.index = self.npics - 1
				self.openTest()
		self.paintFrame()

	def key_down(self):
		if self.index <= self.maxentry - 5:
			self.index += 5
		else:
			if self.ipage == self.npage:
				self.ipage = 1
				self.index = 0
				self.openTest()
			else:
				self.ipage += 1
				self.index = self.minentry
				self.openTest()

		self.paintFrame()

	def keyNumberGlobal(self, number):
		number -= 1
		if len(self["menu"].list) > number:
			self["menu"].setIndex(number)
			self.okbuttonClick()

	def list_sort(self):
		if not hasattr(self, "original_data"):
			self.original_data = (self.names[:], self.titles[:], self.pics[:], self.urls[:])
			self.sorted = False

		if self.sorted:
			self.names, self.titles, self.pics, self.urls = self.original_data
			self.sorted = False
			self["sort"].setText(_("Sort A-Z"))
		else:
			self.names, self.titles, self.pics, self.urls = ListSortUtility.list_sort(self.names, self.titles, self.pics, self.urls)
			self.sorted = True
			self["sort"].setText(_("Sort Default"))

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
		print("[okbuttonClick] idx", idx)
		if idx is None:
			return
		self.namev = self.names[idx]
		self.url = self.urls[idx]
		print("[okbuttonClick] self.namev", self.namev)
		print("[okbuttonClick] self.url", self.url)

		if "cccam.cfg" in self.namev.lower():
			self.askForFcl()
			return

		if "oscam.serv" in self.namev.lower():
			self.getcl("Oscam")
			return

		if "lcn scanner" in self.namev.lower():
			self.Lcn()
			return

		if "check skin conponent" in self.namev.lower():
			self.Checkskin()
			return

		self.session.openWithCallback(self.okClicked, MessageBox, _("I am NOT responsible for any issues you may\nencounter once you install the plugins and skins.\n \
										However, if required, you can get help to resolve the issue.\n\n\nDo you want to execute %s?") % self.namev, MessageBox.TYPE_YESNO, default=True)

	def okClicked(self, answer=False):
		if answer:
			title = (_("Executing %s\nPlease Wait...") % self.namev)
			keywords = ["google", "cloudfaire", "quad9", "emm", "keys", "source"]
			lower_namev = self.namev.lower()
			keyword_found = any(keyword in lower_namev for keyword in keywords)
			if keyword_found:
				cmd = str(self.url) + " > /tmp/my_debug.log 2>&1"
				self.session.open(lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=False)
			else:
				cmd = str(self.url) + " > /tmp/my_debug.log 2>&1"
				self.session.openWithCallback(self.openVi, lsConsole, _(title), cmdlist=[cmd], closeOnSuccess=True)
		else:
			return

	def askForFcl(self):
		self.session.openWithCallback(self.runScriptWithConsole, MessageBox, _("Do you want add Cline?"), MessageBox.TYPE_YESNO)

	def runScriptWithConsole(self, confirmed):
		if confirmed:
			script_path = "/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
			url = "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/refs/heads/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
			try:
				response = requests.get(url)
				response.raise_for_status()
				with io.open(script_path, "w", encoding="utf-8") as file:
					file.write(response.text)
				chmod(script_path, 0o777)
				print("Script updated successfully: {}".format(script_path))
			except requests.exceptions.HTTPError as e:
				print("HTTP error while downloading the script: {}".format(e))
			except requests.exceptions.RequestException as e:
				print("Error while downloading the script: {}".format(e))
			except IOError as e:
				print("Error while saving the script: {}".format(e))
			except Exception as e:
				print("Unexpected error while updating the script: {}".format(e))

			try:
				self.session.open(lsConsole, title="Executing Free Cline Access Script", cmdlist=[script_path])
			except Exception as e:
				print("Error while executing the script: {}".format(e))

	"""
	# def runScriptWithConsole(self, confirmed):
		# if confirmed:
			# script_path = "/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
			# url = "https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/refs/heads/main/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel/sh/Fcl.sh"
			# try:
				# import requests, io
				# response = requests.get(url)
				# response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx and 5xx)
				# with io.open(script_path, "w") as file:
					# file.write(response.text)
				# chmod(script_path, 0o777)
			# except Exception as e:
				# print("Failed to update script: {e}. Using existing script.", e)

			# self.session.open(lsConsole, title="Executing Free Cline Access Script", cmdlist=[script_path])
	"""

	def getcl(self, config_type):
		if config_type == "CCcam":
			dest = "/etc/CCcam.cfg"
			src = plugin_path + "/sh/CCcam.cfg"
			not_found_msg = _("File not found /etc/CCcam.cfg!\nRestart please...")
			write_format = "\nC: {} {} {} {}\n"

		elif config_type == "Oscam":
			dest_dir = "/etc/tuxbox/config"
			if not exists(dest_dir):
				makedirs(dest_dir)
			dest = join(dest_dir, "oscam.server")
			src = plugin_path + "/sh/oscam.server"
			not_found_msg = _("File not found /etc/tuxbox/config/oscam.server!\nRestart please...")
			write_format = (
				"\n[reader]\n"
				"label = Server_{}\n"  # host
				"enable= 1\n"
				"protocol = cccam\n"
				"device = {}, {}\n"  # host, port
				"user = {}\n"  # user
				"password = {}\n"  # password
				"inactivitytimeout = 30\n"
				"group = 1\n"
				"cccversion = 2.1.2\n"
				"cccmaxhops = 1\n"
				"ccckeepalive = 1\n"
				"audisabled = 1\n\n"
			)
		else:
			print("unknow actions")
			return

		if not exists(dest):
			copy2(src, dest)
			self.session.open(MessageBox, not_found_msg, type=MessageBox.TYPE_INFO, timeout=8)
			return

		try:
			dat = RequestUrl()
			print("Request Server url is:", dat)
			data = make_request(dat)

			if PY3:
				data = six.ensure_str(data)

			if "bosscccam" in data:  # ok
				print("bosscccam pattern")
				regex_patterns = [
					r"<strong>c:\s*([\w.-]+)\s+(\d+)\s+([\w\d]+)\s+([\w.-]+)</strong>",
				]
			elif "cccambird" in data:  # ok
				print("cccambird pattern")
				regex_patterns = [
					r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</th></tr>',
				]
			elif "cccamia" in data:  # ok
				print("cccamia pattern")
				regex_patterns = [
					r'>?C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*',
				]
			elif "cccam.net" in data:  # ok
				print("cccam.net pattern")
				regex_patterns = [
					r'b>C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)',
				]
			elif "iptv-15days" in data:  # ok cccamia
				print("15days pattern")
				regex_patterns = [
					r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</th></tr>',
				]
			else:
				print("generic pattern")
				regex_patterns = [
					r'">C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</h3>',
					r'<strong>c:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*</strong',
					r'cline">\s*C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*'
					r'<h1>C:\s+([\w.-]+)\s+(\d+)\s+(\w+)\s+([\w.-]+)\s*',
					r'"C: (.*?) (.*?) (.*?) (.*?)"',
					r'"c: (.*?) (.*?) (.*?) (.*?)"',
				]

			host = None
			port = None
			user = None
			pas = None

			for pattern in regex_patterns:
				url1 = search(pattern, data)
				if url1:
					host = url1.group(1)
					port = url1.group(2)
					user = url1.group(3)
					pas = url1.group(4)

					pas = pas.replace("</h1>", "").replace("</b>", "")
					pasw = pas.replace("</div>", "").replace("</span>", "")

					host = str(host) if host is not None else ""
					port = str(port) if port is not None else ""
					user = str(user) if user is not None else ""
					pasw = str(pasw) if pasw is not None else ""

					if config_type == "CCcam":
						print("Writing CCcam file")
						with open(dest, "a") as cfgdok:
							cfgdok.write(write_format.format(host, port, user, pasw))

					elif config_type == "Oscam":
						print("Writing Oscam file")
						with open(dest, "a") as cfgdok:
							cfgdok.write(write_format.format(host, host, port, user, pasw))

						msg = _("Server added\n\nServer:\nPort:\nUser:\nPassword:\n")

						text = msg
						text = text.replace("Server added", "Server %s added to %s" % (host, dest))
						text = text.replace("Server:", "Server: %s" % host)
						text = text.replace("Port:", "Port: %s" % port)
						text = text.replace("User:", "User: %s" % user)
						text = text.replace("Password:", "Password: %s" % pasw)

						if not PY3:
							text = text.encode("utf-8")

						self.session.open(
							MessageBox,
							text,
							MessageBox.TYPE_INFO,
							timeout=6
						)

		except Exception as e:
			# Error handling
			self.session.open(
				MessageBox,
				_("Server error.\n\nTry again, you might get lucky!\n%s") % str(e),
				type=MessageBox.TYPE_INFO,
				timeout=8
			)


class addInstall(Screen):

	def __init__(self, session, data, name, dest):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "addInstall.xml")
		'''
		if has_dpkg:
			skin = join(skin_path, 'addInstall-os.xml')  # now i have ctrlSkin for check
		'''
		with codecs.open(skin, "r", encoding="utf-8") as f:
			skin = f.read()

		self.skin = ctrlSkin("addInstall", skin)

		self.fxml = str(data)
		self.name = name
		self.dest = dest
		self["key_red"] = Label(_("Exit"))
		self["key_green"] = Label(_("Install"))
		self["key_yellow"] = Label(_("Remove"))
		self["key_blue"] = Label(_("Restart enigma"))
		self["sort"] = Label(_("Reload"))
		"""
		if HALIGN == RT_HALIGN_RIGHT:
			self["sort"].setText(_("Halign Left"))
		else:
			self["sort"].setText(_("Halign Right"))
		"""
		'''
		self.LcnOn = False
		if exists('/etc/enigma2/lcndb') and lngx == 'it':
			self['key_yellow'].setText('Lcn')
			self.LcnOn = True
			print('LcnOn = True')
		'''

		self.list = []
		self["list"] = LPSlist([])
		self["fspace"] = Label()
		self["fspace"].setText(_("Please Wait..."))
		self["info"] = Label()
		self["info"].setText(_("Load Category..."))
		self.downloading = False
		self["actions"] = ActionMap(
			[
				"SetupActions",
				"ColorActions",
				"NumberActions"
			],
			{
				"ok": self.message,
				"0": self.arabicx,
				"5": self.Lcn,
				"6": self.LcnXX,
				"green": self.message,
				"cancel": self.exitnow,
				"red": self.exitnow,
				"blue": self.restart,
				"yellow": self.remove
			},
			-2
		)
		self.timer = eTimer()
		try:
			self.timer_conn = self.timer.timeout.connect(self.getfreespace)
		except:
			self.timer.callback.append(self.getfreespace)
		self.timer.start(1000, 1)
		if self.dest is not None:
			self.onLayoutFinish.append(self.downxmlpage)
		else:
			self.onLayoutFinish.append(self.openTest)

	def arabicx(self):
		"""
		global HALIGN
		if HALIGN == RT_HALIGN_LEFT:
			HALIGN = RT_HALIGN_RIGHT
			self["sort"].setText(_("Halign Left"))
		elif HALIGN == RT_HALIGN_RIGHT:
			HALIGN = RT_HALIGN_LEFT
			self["sort"].setText(_("Halign Right"))
		"""
		if self.dest is not None:
			self.downxmlpage()
		else:
			self.openTest()

	def getfreespace(self):
		try:
			self["info"].setText(_("Category: ") + self.name)
			fspace = freespace()
			self["fspace"].setText(str(fspace))
		except Exception as e:
			print(e)

	def openTest(self):
		regex = '<plugin name="(.*?)".*?url>"(.*?)"</url'
		match = compile(regex, DOTALL).findall(self.fxml)
		self.names = []
		self.urls = []
		items = []
		for name, url in match:
			item = name + "###" + url
			items.append(item)
		items.sort()
		for item in items:
			name = item.split("###")[0]
			url = item.split("###")[1]

			self.names.append(name)
			self.urls.append(url)
		LPshowlist(self.names, self["list"])
		# self.buttons()

	def buttons(self):
		"""
		if HALIGN == RT_HALIGN_RIGHT:
			self["sort"].setText(_("Halign Left"))
		else:
			self["sort"].setText(_("Halign Right"))

		# if self.LcnOn is True:
		# # self.LcnOn = False
		# # if exists("/etc/enigma2/lcndb") and lngx == "it":
			# self["key_yellow"].setText("Lcn")
			# # self.LcnOn = True
			# print("LcnOn 2 = True")
		# else:
			# self["key_yellow"].setText(_("Remove"))
		"""
		return

	def message(self):
		if self.dest is not None:
			print("go okRun")
			self.okRun()
			return

		idx = self["list"].getSelectionIndex()
		self.url = self.urls[idx]
		n1 = self.url.rfind("/")
		self.plug = self.url[(n1 + 1):]
		self.iname = ""

		if ".deb" in self.plug:
			if not has_dpkg:
				self.session.open(MessageBox, _("Unknown Image!"), MessageBox.TYPE_INFO, timeout=5)
				return
			self.iname = self.plug.split("_")[0]

		elif ".ipk" in self.plug:
			if has_dpkg:
				self.session.open(MessageBox, _("Unknown Image!"), MessageBox.TYPE_INFO, timeout=5)
				return
			self.iname = self.plug.split("_")[0] if "_" in self.plug else self.plug

		elif ".zip" in self.plug or ".tar" in self.plug or ".gz" in self.plug or ".bz2" in self.plug:
			self.iname = self.plug

		path = "/var/lib/dpkg/info" if exists("/var/lib/dpkg/info") else "/var/lib/opkg/info"
		resp = "Is NOT installed.\n"
		self.plug_name = self.plug.split("_")[0].lower()

		for root, dirs, files in walk(path):
			if files is not None:
				for name in files:
					name = name.lower()
					if name.endswith((".postinst", ".preinst", ".prerm", ".postrm", ".md5sums", ".conffiles", "~")):
						continue
					if exists("/var/lib/dpkg/info"):
						if name.endswith(".list"):
							name = name.replace(".list", "")
					else:
						if name.endswith(".control"):
							name = name.replace(".control", "")
						if name.endswith(".list"):
							continue

					if name.startswith(self.plug_name):
						resp = "Is ALREADY installed.\n"
						break

		choices = [
			("Install", "install"),
			("Remove", "uninstall"),
			("Cancel", "cancel")
		]
		from Screens.ChoiceBox import ChoiceBox
		self.session.openWithCallback(
			self.choiceCallback,
			ChoiceBox,
			title=self.plug_name + "\n\n" + resp + "\nDo you want to Install, Remove, or Cancel?",
			list=choices
		)

	def choiceCallback(self, result):
		if result is not None:
			choice, action = result
			self.okClicked(action, self.plug_name, self.url)
		else:
			print("User canceled the operation")

	def okClicked(self, choice, name, url):
		n2 = self.plug.find("_")
		iname = self.plug[:n2] if n2 != -1 else self.plug

		if choice == "install":
			folddest = "/tmp/" + self.plug
			if self.retfile(folddest):
				command = ""
				if ".deb" in self.plug:
					command = "dpkg -i '/tmp/" + self.plug + "'"
				elif ".ipk" in self.plug:
					command = "opkg install --force-reinstall --force-overwrite '/tmp/" + self.plug + "'"
				elif ".zip" in self.plug:
					command = "unzip -o -q '/tmp/" + self.plug + "' -d /"
				elif ".tar" in self.plug:
					command = "tar -xvf '/tmp/" + self.plug + "' -C /"
				elif ".gz" in self.plug:
					command = "tar -xzvf '/tmp/" + self.plug + "' -C /"
				elif ".bz2" in self.plug:
					command = "tar -xjvf '/tmp/" + self.plug + "' -C /"
				else:
					return

				self.session.open(lsConsole, "Installing Extension", [command], closeOnSuccess=False)

		elif choice == "uninstall":
			if ".deb" in self.plug:
				if not has_dpkg:
					self.session.open(MessageBox, _("Unknown Image!"), MessageBox.TYPE_INFO, timeout=5)
					return
				command = "dpkg -r " + iname.lower()

			elif ".ipk" in self.plug:
				if has_dpkg:
					self.session.open(MessageBox, _("Unknown Image!"), MessageBox.TYPE_INFO, timeout=5)
					return
				command = "opkg remove --force-depends " + iname.lower()

			else:
				return

			self.session.open(lsConsole, "Execution Command", [command], closeOnSuccess=False)

		else:
			self.session.open(MessageBox, "Action Aborted.", MessageBox.TYPE_INFO, timeout=4)

	def retfile(self, dest):
		import requests
		response = requests.get(self.url)
		if response.status_code == 200:
			with open(dest, "wb") as f:
				f.write(response.content)
			print("File downloaded successfully.")
			return True
		else:
			print("Error downloading the file.")
		return False

	def downxmlpage(self):
		self.downloading = False
		r = make_request(self.fxml)
		if r is None:
			print("Error: No data received from make_request")
			return
		self.names = []
		self.urls = []
		items = []
		name = url = date = ""
		try:
			if "ciefp" in self.name.lower():
				n1 = r.find('title="README.txt', 0)
				n2 = r.find('href="#readme">', n1)
				r = r[n1:n2]
				regex = r'title="ciefp-E2-(.*?).zip".*?href="(.*?)"'
				match = compile(regex).findall(r)
				for name, url in match:
					if url.find(".zip") != -1:
						url = url.replace("blob", "raw")
						url = "https://github.com" + url
						name = decode_html(name)
						self.downloading = True
					item = name + "###" + str(url)
					items.append(item)

			if "cyrus" in self.name.lower():
				n1 = r.find('name="Sat">', 0)
				n2 = r.find("/ruleset>", n1)
				r = r[n1:n2]
				regex = r'Name="(.*?)".*?Link="(.*?)".*?Date="(.*?)"><'
				match = compile(regex).findall(r)
				for name, url, date in match:
					if url.find(".zip") != -1:
						if "ddt" in name.lower():
							continue
						if "Sat" in name.lower():
							continue
						name = decode_html(name) + " " + date
						self.downloading = True
					item = name + "###" + str(url)
					items.append(item)

			if "manutek" in self.name.lower():
				regex = r'href="/isetting/.*?file=(.+?).zip">'
				match = compile(regex).findall(r)
				for url in match:
					name = url
					name = name.replace("NemoxyzRLS_Manutek_", "").replace("_", " ").replace("%20", " ")
					url = "http://www.manutek.it/isetting/enigma2/" + url + ".zip"
					self.downloading = True
					item = decode_html(name) + "###" + str(url)
					items.append(item)

			if "morpheus" in self.name.lower():
				regex = r'title="E2_Morph883_(.*?).zip".*?href="(.*?)"'
				match = compile(regex).findall(r)
				for name, url in match:
					if url.find(".zip") != -1:
						name = "Morph883 " + decode_html(name)
						url = url.replace("blob", "raw")
						url = "https://github.com" + url
						self.downloading = True
					item = name + "###" + str(url)
					items.append(item)

			if "vhannibal net" in self.name.lower():
				pattern = compile(r'<td><a href="(.+?)".*?>(.+?)</a>.*?<td>(.+?)</td>.*?</tr>', DOTALL)
				matches = pattern.findall(r)
				for match in matches:
					url = match[0]
					name = match[1]
					if isinstance(name, bytes):
						name = name.decode("utf-8", errors="replace")
					name = decode_html(match[1])
					date = match[2]
					name = str(name).replace("&#127381;", "").replace("%20", " ").replace("..", "").strip() + " " + date
					url = "https://www.vhannibal.net/" + url
					self.downloading = True
					item = name + "###" + str(url)
					items.append(item)

			if "vhannibal tek" in self.name.lower():
				regex = r'<a href="Vhannibal(.*?).zip".*?right">(.*?) </td'
				match = compile(regex).findall(r)
				for url, date in match:
					if ".php" in url.lower():
						continue
					name = decode_html(url).replace("&#127381;", "").replace("%20", " ") + " " + date
					url = "http://sat.alfa-tech.net/upload/settings/vhannibal/Vhannibal" + url + ".zip"
					self.downloading = True
					item = name + "###" + str(url)
					items.append(item)

			items.sort()
			for item in items:
				name = item.split("###")[0]
				url = item.split("###")[1]
				if name in self.names:
					continue
				name = str(decode_html(name))
				url = str(url)
				self.names.append(name.strip())
				self.urls.append(url.strip())

			LPshowlist(self.names, self["list"])

		except Exception as e:
			print("downxmlpage get failed: ", str(e))
			self["info"].setText(_("Download page get failed ..."))

	def Lcn(self, answer=None):
		if answer is None:
			self.session.openWithCallback(
				self.Lcn,
				MessageBox,
				_("Do you want to Order LCN Bouquet?"),
				MessageBox.TYPE_YESNO
			)
		else:
			print("Starting LCN scan...")
			try:
				from .LCNScanner.Terrestrial import PluginSetup
				self.session.open(PluginSetup)
			except Exception as e:
				print("Exception during LCN scan:", e)

	def LcnXX(self, answer=None):
		if answer is None:
			self.session.openWithCallback(self.Lcn, MessageBox, _("Do you want to Order LCN Bouquet?"), MessageBox.TYPE_YESNO)
		else:
			print("Starting LCN scan...")
			try:
				lcn_scanner_instance = LCNScanner()
				LCN = lcn_scanner_instance.lcnScan()
				print("LCN Scanner returned:", LCN)

				if LCN:
					self.session.open(LCN)
				else:
					print("Error: LCN scan did not return a valid screen.")
			except Exception as e:
				print("Exception during LCN scan:", e)

			try:
				self.session.openWithCallback(self._onLCNScanFinished, MessageBox, _("[LCNScanner] LCN scan finished\nChannels Ordered!"), MessageBox.TYPE_INFO, timeout=5)
			except RuntimeError as re:
				print("RuntimeError during MessageBox display:", re)

	def _onLCNScanFinished(self, result=None):
		pass

	def okRun(self):
		self.session.openWithCallback(self.okRun1, MessageBox, _("I am NOT responsible for any issues you may\nencounter once you install the plugins and skins.\nHowever, if required, you can get help to resolve the issue.\n\n\nDo you want to install?"), MessageBox.TYPE_YESNO)

	def okRun1(self, answer=False):
		dest = "/tmp/settings.zip"
		if answer:
			global setx
			if self.downloading is True:
				idx = self["list"].getSelectionIndex()
				url = self.urls[idx]
				self.namel = ""
				if "dtt" not in url.lower():
					setx = 1
					terrestrial()
				if keepiptv():
					print("-----save iptv channels-----")

				from six.moves.urllib.request import urlretrieve
				urlretrieve(url, dest)
				if exists(dest) and ".zip" in dest:
					fdest1 = "/tmp/unzipped"
					fdest2 = "/etc/enigma2"
					if exists("/tmp/unzipped"):
						system("rm -rf /tmp/unzipped")
					makedirs("/tmp/unzipped")
					cmd2 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
					system(cmd2)
					for root, dirs, files in walk(fdest1):
						for name in dirs:
							self.namel = name
					system("rm -rf /etc/enigma2/lamedb")
					system("rm -rf /etc/enigma2/*.radio")
					system("rm -rf /etc/enigma2/*.tv")
					system("rm -rf /etc/enigma2/*.del")
					system("cp -rf  '/tmp/unzipped/" + str(self.namel) + "/'* " + fdest2)
					system("rm -rf /tmp/unzipped")
					system("rm -rf /tmp/settings.zip")
					title = (_("Installing %s\nPlease Wait...") % self.name)
					self.session.openWithCallback(self.yes, lsConsole, title=_(title), cmdlist=["wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"], closeOnSuccess=False)
			else:
				self["info"].setText(_("Settings Not Installed ..."))

	def pas(self, call=None):
		pass

	def yes(self, call=None):
		print("^^^^^^^^^^^^^^ add file to bouquet ^^^^^^^^^^^^^^")
		copy_files_to_enigma2()
		print("^^^^^^^^^^^^^^^ reloads bouquets ^^^^^^^^^^^^^^^")
		ReloadBouquets(setx)

	def remove(self):
		self.session.openWithCallback(self.removenow, MessageBox, _("Do you want to remove?"), MessageBox.TYPE_YESNO)

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
		self.session.openWithCallback(self.restartnow, MessageBox, _("Do you want to restart Gui Interface?"), MessageBox.TYPE_YESNO)

	def restartnow(self, answer=False):
		if answer:
			self.session.open(TryQuitMainloop, 3)

	def exitnow(self):

		try:
			if not has_dpkg:
				refreshPlugins()
		except Exception as e:
			print("error on exit!", e)

		self.close()


class LSinfo(Screen):

	def __init__(self, session, name):
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "LSinfo.xml")

		'''
		if has_dpkg:
			skin = join(skin_path, 'LSinfo-os.xml')  # now i have ctrlSkin for check
		'''

		with codecs.open(skin, "r", encoding="utf-8") as f:
			skin = f.read()

		self.skin = ctrlSkin("LSinfo", skin)

		self.name = name
		info = _("Please Wait...")
		self["list"] = ScrollLabel(info)
		self["key_green"] = Label()
		self["pixmap"] = Pixmap()
		self["pixmap"].hide()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"DirectionActions",
				"HotkeyActions",
				"InfobarEPGActions",
				"ColorActions",
				"ChannelSelectBaseActions"
			],
			{
				"ok": self.close,
				"back": self.close,
				"cancel": self.close,
				"up": self.Up,
				"down": self.Down,
				"left": self.Up,
				"right": self.Down,
				# "yellow": self.update_me,
				"green": self.update_me,
				"yellow_long": self.update_dev,
				"info_long": self.update_dev,
				"infolong": self.update_dev,
				"showEventInfoPlugin": self.update_dev,
				"red": self.close
			},
			-1
		)

		self.Update = False
		self.timer = eTimer()
		try:
			self.timer_conn = self.timer.timeout.connect(self.startRun)
		except:
			self.timer.callback.append(self.startRun)
		self.timer.start(100, 1)

		self.timerz = eTimer()
		try:
			self.timerz_conn = self.timerz.timeout.connect(self.check_vers)
		except:
			self.timerz.callback.append(self.check_vers)
		self.timerz.start(2000, 1)

		self.onLayoutFinish.append(self.pas)

	def pas(self):
		pass

	def check_vers(self):
		remote_version = '0.0'
		remote_changelog = ''
		page = ''

		try:
			req = Request(b64decoder(installer_url), headers={'User-Agent': 'Mozilla/5.0'})
			page = urlopen(req).read().decode("utf-8")  # Decodifica diretta
		except Exception as e:
			print("[ERROR] Unable to fetch version info:", str(e))
			return

		if page:
			for line in page.split("\n"):
				line = line.strip()
				if line.startswith("version"):
					remote_version = line.split("=")[-1].strip().strip("'").strip('"')
				elif line.startswith("changelog"):
					remote_changelog = line.split("=")[-1].strip().strip("'").strip('"')
					break

		self.new_version = remote_version
		self.new_changelog = remote_changelog
		if not isinstance(self.new_changelog, str):
			self.new_changelog = str(self.new_changelog)
		if not isinstance(self.new_version, str):
			self.new_version = str(self.new_version)
		# if float(__version__) < float(remote_version):
		if __version__ < remote_version:
			self.Update = True
			self.show_update_message()

	def show_update_message(self):
		"""Mostra un MessageBox con le informazioni sull'aggiornamento"""
		if self.Update:
			msg = _("New version available\n\nChangelog:\n\nPress the green button to start the update.")

			text = msg
			text = text.replace("New version available", "New version %s available" % self.new_version)
			text = text.replace("Changelog:", "Changelog: %s" % self.new_changelog)

			self.session.open(
				MessageBox,
				text,
				MessageBox.TYPE_INFO,
				timeout=10
			)
		else:
			msg = _("New version available\n\nChangelog:")

			text = "%s %s\n\n%s" % (
				msg,
				self.new_version,
				self.new_changelog
			)

			self.session.open(
				MessageBox,
				text,
				MessageBox.TYPE_INFO,
				timeout=10
			)
			print("Cannot open modal MessageBox. The current screen is not modal.")

			self["key_green"].setText(_("Update"))
			self["pixmap"].show()

	def update_me(self):
		if self.Update:
			msg = _("New version is available.\n\nChangelog:\n\nDo you want to install it now?")

			message = "%s %s\n\n%s" % (
				msg,
				self.new_version,
				self.new_changelog
			)

			self.session.openWithCallback(
				self.install_update,
				MessageBox,
				message,
				MessageBox.TYPE_YESNO
			)
		else:
			self.session.open(
				MessageBox,
				_("Congrats! You already have the latest version..."),
				MessageBox.TYPE_INFO,
				timeout=10
			)

	def update_dev(self):
		try:
			url = b64decoder(developer_url)
			req = Request(url, headers={"User-Agent": AgentRequest})
			try:
				response = urlopen(req)
				page = response.read()
			except URLError as e:
				print("Error fetching data from GitHub:", e)
				self.session.open(MessageBox, _("Failed to fetch update information. Please check your internet connection."), MessageBox.TYPE_ERROR)
				return

			try:
				data = loads(page)
			except ValueError as e:
				print("Error parsing JSON data:", e)
				self.session.open(MessageBox, _("Failed to parse update information. Please try again later."), MessageBox.TYPE_ERROR)
				return

			remote_date = data.get("pushed_at")
			if not remote_date:
				print("No 'pushed_at' field found in the response.")
				self.session.open(MessageBox, _("No update information available."), MessageBox.TYPE_INFO)
				return

			try:
				strp_remote_date = dt.strptime(remote_date, "%Y-%m-%dT%H:%M:%SZ")
				formatted_date = strp_remote_date.strftime("%Y-%m-%d")
			except ValueError as e:
				print("Error parsing date:", e)
				self.session.open(MessageBox, _("Invalid date format in update information."), MessageBox.TYPE_ERROR)
				return

			self.session.openWithCallback(
				self.install_update,
				MessageBox,
				_("Do you want to install update (%s) now?") % formatted_date,
				MessageBox.TYPE_YESNO
			)

		except Exception as e:
			print("Unexpected error in update_dev:", e)
			self.session.open(MessageBox, _("An unexpected error occurred. Please try again later."), MessageBox.TYPE_ERROR)

	def install_update(self, answer=False):
		if answer:
			self.session.open(lsConsole, "Upgrading...", cmdlist=["wget -q --no-check-certificate " + b64decoder(installer_url) + " -O - | /bin/sh"], finishedCallback=self.myCallback, closeOnSuccess=False)
		else:
			self.session.open(MessageBox, _("Update Aborted!"), MessageBox.TYPE_INFO, timeout=3)

	def myCallback(self, result=None):
		print("result:", result)
		return

	def startRun(self):
		try:
			if self.name == " Information ":
				print("Running openinfo method...")
				self.openinfo()

			elif self.name == " About ":
				print("Opening LICENSE file...")
				license_path = join(plugin_path, "LICENSE")
				try:

					if not exists(license_path):
						print("License file does not exist: {}".format(license_path))
						self["list"].setText("Error: LICENSE file not found.")
						return

					if not access(license_path, R_OK):
						print("License file is not readable: {}".format(license_path))
						self["list"].setText("Error: LICENSE file is not readable.")
						return

					with io.open(license_path, "r", encoding="utf-8") as filer:
						info = filer.read()
						info = info.replace("\r", "")
						info = str(info).strip()
						self["list"].setText(info)

				except IOError as e:
					print("Error reading LICENSE file: {}".format(e))
					self["list"].setText("Error: Could not read LICENSE file.")
				except Exception as e:
					print("Unexpected error: {}".format(e))
					self["list"].setText("Error: An unexpected error occurred.")
			else:
				print("Unknown name value:", self.name)
				return
		except Exception as e:
			print("Error in startRun: ", e)
			self["list"].setText(_("Unable to download updates!"))

	def openinfo(self):
		from .addons.stbinfo import stbinfo
		try:
			header = "Suggested by: @masterG - @oktus - @pcd\n"
			header += "All code was rewritten by @Lululla - 2024.07.20\n"
			header += "Designs and Graphics by @oktus\n"
			header += "Support on: Linuxsat-support.com\n\n"
			print("stbinfo initialized:", stbinfo)
			stbinfo_str = str(stbinfo.to_string()) if stbinfo else "No info available"
			base_content = "{0} V.{1}\n{2}STB info:\n{3}\n".format(
				descplug,
				__version__,
				header,
				stbinfo_str
			)

			try:
				# Python 3
				with open("/tmp/output.txt", "w", encoding="utf-8") as file:
					file.write(base_content)
			except TypeError:
				# Python 2
				with open("/tmp/output.txt", "w") as file:
					file.write(base_content.encode("utf-8"))

			info_path = join(plugin_path, "info.txt")
			if fileExists(info_path):
				try:
					try:
						# Python 3
						with open(info_path, "r", encoding="utf-8") as info_file:
							additional_info = info_file.read()
					except TypeError:
						# Python 2
						with open(info_path, "r") as info_file:
							additional_info = info_file.read().decode("utf-8")

					try:
						# Python 3
						with open("/tmp/output.txt", "a", encoding="utf-8") as output_file:
							output_file.write("\nAdditional Info:\n{0}".format(additional_info))
					except TypeError:
						# Python 2
						with open("/tmp/output.txt", "a") as output_file:
							output_file.write("\nAdditional Info:\n{0}".format(additional_info.encode("utf-8")))
				except Exception as e:
					print("Error appending info.txt: {0}".format(str(e)))
			else:
				print("Info file not found: {0}".format(info_path))

			try:
				try:
					# Python 3
					with open("/tmp/output.txt", "r", encoding="utf-8") as filer:
						content = filer.read()
				except TypeError:
					# Python 2
					with open("/tmp/output.txt", "r") as filer:
						content = filer.read().decode("utf-8")

				self["list"].setText(str(content))
			except Exception as e:
				print("Final read/display error: {0}".format(str(e)))
				self["list"].setText("Error loading system information")

		except Exception as e:
			print("Error in openinfo:", e)
			self["list"].setText("Error loading information")

	def cancel(self):
		self.close()

	def ok(self):
		self.close()

	def Down(self):
		self["list"].pageDown()

	def Up(self):
		self["list"].pageUp()


class startLP(Screen):
	def __init__(self, session):
		self.session = session
		global _session

		_session = session
		Screen.__init__(self, session)

		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass

		skin = join(skin_path, "startLP.xml")
		with codecs.open(skin, "r", encoding="utf-8") as f:
			self.skin = f.read()
		# self.skin = ctrlSkin("startLP", skin)
		self["poster"] = Pixmap()
		self["version"] = Label("Wait Please... Linuxsat Panel V." + __version__)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.clsgo, "cancel": self.clsgo}, -1)
		self.onLayoutFinish.append(self.loadDefaultImage)

	def clsgo(self, *args):
		print("[startLP] Opening LinuxsatPanel...")
		self["actions"].setEnabled(False)
		self.session.open(LinuxsatPanel)
		self.close()

	def loadDefaultImage(self):
		self.fldpng = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/icons/pageLogo.png".format("LinuxsatPanel"))

		self.timer = eTimer()
		try:
			self.timer_conn = self.timer.timeout.connect(self.decodeImage)
		except:
			self.timer.callback.append(self.decodeImage)  # Py2 (OpenPLi)
		self.timer.start(100, True)

		self.delayedTimer = eTimer()
		try:
			self.delayedTimer_conn = self.delayedTimer.timeout.connect(self.clsgo)
		except:
			self.delayedTimer.callback.append(self.clsgo)
		self.delayedTimer.start(1000, True)

	def decodeImage(self, *args):
		pixmapx = self.fldpng
		if fileExists(pixmapx):
			size = self["poster"].instance.size()
			if not hasattr(self, "picload") or not self.picload:
				self.picload = ePicLoad()
			self.scale = AVSwitch().getFramebufferScale()
			self.picload.setPara([size.width(), size.height(), self.scale[0], self.scale[1], 0, 1, "#00000000"])
			# _l = self.picload.PictureData.get()
			# del self.picload
			if has_dpkg:
				self.picload.startDecode(pixmapx, False)
			else:
				self.picload.startDecode(pixmapx, 0, 0, False)
			ptr = self.picload.getData()
			if ptr is not None:
				self["poster"].instance.setPixmap(ptr)
				self["poster"].show()
		return


class AboutLSS(Screen):
	def __init__(self, session):
		global _session, first

		_session = session
		first = False
		Screen.__init__(self, session)
		try:
			Screen.setTitle(self, _("%s") % descplug + " V." + __version__)
		except:
			try:
				self.setTitle(_("%s") % descplug + " V." + __version__)
			except:
				pass
		skin = join(skin_path, "AboutLSS.xml")
		with codecs.open(skin, "r", encoding="utf-8") as f:
			skin = f.read()
		self.skin = ctrlSkin("AboutLSS", skin)
		credit = _("Thank you for choosing plugin for management of your Enigma Box.\n\n")
		credit += _("Suggested by: @masterG - @oktus - @pcd\n")
		credit += _("Designs and Graphics by @oktus\n")
		credit += _("Support on: Linuxsat-support.com\n\n")
		credit += _("The Plugin lives thanks to the donations of each of you.\n")
		credit += _("A coffee costs nothing.\n\n")
		credit += _("If you think it is a useful tool for your box\n")
		credit += _("please make a donation:\n")
		credit += "http://paypal.com/paypalme/belfagor2005\n"
		credit += _("make donation on Linuxsat-support.com\n\n\n\n\n")
		credit += _("All code was rewritten by @Lululla - 2024.07.20\n")
		self["Info"] = Label(_(credit))
		self["key_red"] = Label(_("Exit"))
		self["pixmap"] = Pixmap()
		self["actions"] = ActionMap(
			[
				"OkCancelActions",
				"ColorActions"
			],
			{
				"ok": self.close,
				"cancel": self.close,
				"exit": self.close,
				"back": self.close,
				"red": self.close
			},
			-1
		)


def menustart():
	try:
		if CheckConn():
			_session.open(startLP)
		else:
			_session.open(
				MessageBox,
				_("Check Connection!"),
				MessageBox.TYPE_INFO,
				timeout=5
			)

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
	return [(_("Linuxsat Panel"), main, descplug, 44)] if menuid == "mainmenu" else []


def Plugins(**kwargs):
	# initialize_global_settings()  # Initialize the necessary fonts
	add_skin_fonts()
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
