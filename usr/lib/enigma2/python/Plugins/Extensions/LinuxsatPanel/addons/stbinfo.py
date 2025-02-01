# -*- coding: utf-8 -*-

from os import system, popen, statvfs as statvfsx
from os.path import exists
import platform
import requests
import socket
import uuid


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


class StbInfo:
	def __init__(self):
		try:
			from Plugins.Extensions.OpenWebif.controllers.models.info import getInfo
			self.boxinfo = getInfo()
		except:
			self.boxinfo = {}
			pass

		self.hw_vendor = self.get_info_value('brand')
		self.hw_model = self.get_info_value('model')
		self.hw_chipset = self.get_info_value('chipset')
		self.hw_arch = self._get_arch()

		self.sw_distro_ver = self.get_info_value('imagever')
		self.sw_distro = self.get_info_value('friendlyimagedistro')
		self.sw_enigma_ver = self.get_info_value('enigmaver')
		self.sw_oe_ver = self.get_info_value('oever')

		self.node = self._get_node()
		self.installation_id = self._get_installation_id()
		self.python_version = self._get_python_version()
		self.python_version_touple = self._get_python_version_touple()

		self.is_vti_image = self._is_vti_image()
		self.is_dmm_image = self._is_dmm_image()

		self.internetline = self.get_internet_status()
		self.mountid = self.get_mount_info()
		self.storhdd = self.get_storage_info()
		self.memin = self.get_memory_info()
		self.ipub = self.get_ip()
		self.current_format = self.getResolution()
		self.pip = self.get_public_ip()

	def to_string(self):
		lines = []
		lines.append('Data source: %s' % 'OpenWebif' if self.boxinfo else 'proc')
		lines.append('\n')
		lines.append('HW Info:')
		lines.append('Vendor: %s' % self.hw_vendor)
		lines.append('Model: %s' % self.hw_model)
		lines.append('Chipset: %s' % self.hw_chipset)
		lines.append('Architecture: %s' % self.hw_arch)
		lines.append('Local Ip: %s' % self.ipub)
		lines.append('%s' % self.pip)
		lines.append('%s' % self.internetline)
		lines.append('\n')
		lines.append('SW Info:')
		lines.append('Installation ID: %s' % self.installation_id)
		lines.append('Python version: %s' % self.python_version)
		lines.append('Distro: %s' % self.sw_distro)
		lines.append('Distro version: %s' % self.sw_distro_ver)
		lines.append('Enigma version: %s' % self.sw_enigma_ver)
		lines.append('OE version: %s' % self.sw_oe_ver)
		lines.append('\n')
		lines.append('Video Format: %s' % self.current_format)
		lines.append('%s' % self.mountid)
		lines.append('%s' % self.storhdd)
		lines.append('%s' % self.memin)
		lines.append('Is VTi image: %s' % self.is_vti_image)
		lines.append('Is DMM image: %s' % self.is_dmm_image)

		return '\n'.join(lines)

	def getResolution(self):

		def getDesktopSize():
			from enigma import getDesktop
			s = getDesktop(0).size()
			return (s.width(), s.height())

		desktopSize = getDesktopSize()
		width = desktopSize[0]

		if width >= 3840:
			return "UHD/4K (3840x2160)"
		elif width >= 2560:
			return "WQHD (2560x1440)"
		elif width >= 1920:
			return "Full HD (1920x1080)"
		elif width >= 1280:
			return "HD (1280x720)"
		else:
			return "SD (720x576)"

	def get_internet_status(self):
		return "Internet: Connected" if system("ping -c 1 8.8.8.8 > /dev/null 2>&1") == 0 else "Internet: No Connection"

	def get_storage_info(self):
		try:
			statvfs = statvfsx("/")
			total_storage = (statvfs.f_blocks * statvfs.f_frsize) // (1024 * 1024)
			free_storage = (statvfs.f_bfree * statvfs.f_frsize) // (1024 * 1024)
			return "HDD: %d MB, Free: %d MB" % (total_storage, free_storage)
		except:
			return "Storage Info: Unknown"

	def get_info_value(self, entry):
		value = self.boxinfo.get(entry)

		if value:
			return value
		try:
			with open('/proc/stb/info/' + entry, 'r') as f:
				value = f.read().strip()
		except:
			value = 'unknown'

		return value

	def _get_node(self):
		ifaces = sorted(self.boxinfo.get('ifaces', []), key=lambda x: x['name'])
		if len(ifaces) > 0:
			mac_str = ifaces[0].get('mac')
			if mac_str:
				return mac_str.upper().replace(':', '')

		for method in ("_ip_getnode", "_ifconfig_getnode"):
			if hasattr(uuid, method):
				node = getattr(uuid, method)()
				if node:
					mac_str = ''.join(("%012X" % node)[i:i + 2] for i in range(0, 12, 2))
					break
		else:
			mac_str = ''

		return mac_str

	def get_memory_info(self):
		try:
			with open("/proc/meminfo") as f:
				mem_total = mem_free = 0
				for line in f:
					if "MemTotal" in line:
						mem_total = int(line.split()[1]) // 1024
					elif "MemFree" in line:
						mem_free = int(line.split()[1]) // 1024
				return "Ram: %d MB, Free: %d MB" % (mem_total, mem_free)
		except:
			return "Memory Info: Unknown"

	def _get_installation_id(self):
		from hashlib import md5
		return md5(str(self._get_node()).encode('utf-8')).hexdigest()

	@staticmethod
	def _get_arch():
		return platform.machine()

	@staticmethod
	def _get_python_version():
		return platform.python_version()

	@staticmethod
	def _get_python_version_touple():
		ver_major, ver_minor, patchlevel = platform.python_version_tuple()
		return (int(ver_major), int(ver_minor), int(patchlevel))

	@staticmethod
	def get_ip():
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 53))
			ip = s.getsockname()[0]
			s.close()
		except:
			ip = '127.0.0.1'
		return ip

	@staticmethod
	def _is_dmm_image():
		try:
			from enigma import eTimer
			eTimer().timeout.connect
		except Exception as e:
			print(e)
			return False
		return True

	@staticmethod
	def _is_vti_image():
		# this returns True also for some DMM images based on OE < 2.0
		try:
			import inspect
			from skin import parseSize as __parseSize

			try:
				argspec = inspect.getargspec(__parseSize)
			except:
				argspec = inspect.getfullargspec(__parseSize)
			return len(argspec.args) == 2
		except:
			return False

	def get_mount_info(self):
		try:
			mount_point = "/media/hdd"
			if exists(mount_point):
				return "Mount: ", mount_point
			else:
				return "Mount: Not Found"
		except:
			return "Mount: Unknown"

	def get_public_ip(self):
		services = [
			'https://api.ipify.org',
			'https://ident.me',
			'https://ifconfig.me/ip',
			'https://ipinfo.io/ip'
		]

		for service in services:
			try:
				response = requests.get(service, timeout=5)
				if response.status_code == 200:
					return "Public IP: {}".format(response.text.strip())
			except Exception as e:
				print("Error contacting {}: {}".format(service, str(e)))

		# Fallback to wget method
		try:
			result = popen('wget -qO - ifconfig.me 2>/dev/null').read().strip()
			if result:
				return "Public IP: %s" % result
		except Exception as e:
			print("Fallback method failed: %s" % str(e))

		return "Public IP: Unknown"


stbinfo = StbInfo()
