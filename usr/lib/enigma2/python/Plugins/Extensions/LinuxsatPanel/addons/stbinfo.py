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

from os import system, popen, statvfs as statvfsx
from os.path import exists
import platform
import socket
import uuid
import sys
from .. import _

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


PY3 = sys.version_info[0] >= 3


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
        try:
            lines.append('Data source: %s' % ('OpenWebif' if self.boxinfo else 'proc'))
            lines.append('\n')
            lines.append('HW Info:')
            lines.append('Vendor: %s' % str(self.hw_vendor) if self.hw_vendor else 'Unknown')
            lines.append('Model: %s' % str(self.hw_model) if self.hw_model else 'Unknown')
            lines.append('Chipset: %s' % str(self.hw_chipset) if self.hw_chipset else 'Unknown')
            lines.append('Architecture: %s' % str(self.hw_arch) if self.hw_arch else 'Unknown')
            lines.append('Local Ip: %s' % str(self.ipub) if self.ipub else 'Unknown')
            lines.append('Public IP: %s' % str(self.pip) if self.pip else 'Unknown')
            lines.append('Internet: %s' % str(self.internetline) if self.internetline else 'Unknown')
            lines.append('\n')
            lines.append('SW Info:')
            lines.append('Installation ID: %s' % str(self.installation_id) if self.installation_id else 'Unknown')
            lines.append('Python version: %s' % str(self.python_version) if self.python_version else 'Unknown')
            lines.append('Distro: %s' % str(self.sw_distro) if self.sw_distro else 'Unknown')
            lines.append('Distro version: %s' % str(self.sw_distro_ver) if self.sw_distro_ver else 'Unknown')
            lines.append('Enigma version: %s' % str(self.sw_enigma_ver) if self.sw_enigma_ver else 'Unknown')
            lines.append('OE version: %s' % str(self.sw_oe_ver) if self.sw_oe_ver else 'Unknown')
            lines.append('\n')
            lines.append('Video Format: %s' % str(self.current_format) if self.current_format else 'Unknown')
            lines.append('Mount Info: %s' % str(self.mountid) if self.mountid else 'Unknown')
            lines.append('Storage Info: %s' % str(self.storhdd) if self.storhdd else 'Unknown')
            lines.append('Memory Info: %s' % str(self.memin) if self.memin else 'Unknown')
            lines.append('Is VTi image: %s' % str(self.is_vti_image) if self.is_vti_image else 'Unknown')
            lines.append('Is DMM image: %s' % str(self.is_dmm_image) if self.is_dmm_image else 'Unknown')
        except Exception as e:
            print("Error formatting info:", e)
        return '\n'.join(lines)

    def getResolution(self):
        def getDesktopSize():
            from enigma import getDesktop
            try:
                s = getDesktop(0).size()
                return (s.width(), s.height())
            except:
                return (1920, 1080)  # Valore predefinito

        try:
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
        except:
            return "Resolution: Unknown"

    def get_internet_status(self):
        """Check internet connection for Enigma2 - simple and safe"""
        try:
            import socket

            # Test 1: Ping Google DNS
            if system("ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1") == 0:
                return _("Internet: Connected")

            # Test 2: TCP connection to port 80 (HTTP) of a reliable server
            # Note: This is a pure TCP connection, HTTPS is not required
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect(("www.google.com", 80))
                sock.close()
                return _("Internet: Connected")
            except:
                pass

            return _("Internet: No Connection")

        except Exception as e:
            print("Internet check error:", str(e))
            return _("Internet: Unknown")

    def get_storage_info(self):
        try:
            statvfs = statvfsx("/")
            total_storage = (statvfs.f_blocks * statvfs.f_frsize) // (1024 * 1024)
            free_storage = (statvfs.f_bfree * statvfs.f_frsize) // (1024 * 1024)
            used_storage = total_storage - free_storage
            return "Storage: %d MB total, %d MB free, %d MB used" % (total_storage, free_storage, used_storage)
        except:
            return "Storage Info: Unknown"

    def get_info_value(self, entry):
        value = self.boxinfo.get(entry)
        if value:
            return value

        try:
            with open('/proc/stb/info/' + entry, 'r') as f:
                value = f.read().strip()
                return value if value else 'unknown'
        except IOError:
            return 'unknown'
        except:
            return 'unknown'

    def _get_node(self):
        ifaces = self.boxinfo.get('ifaces', [])
        if ifaces:
            ifaces_sorted = sorted(ifaces, key=lambda x: x.get('name', ''))
            for iface in ifaces_sorted:
                mac_str = iface.get('mac', '')
                if mac_str:
                    return mac_str.upper().replace(':', '')

        # Fallback: usa uuid (Python 2/3 compatibile)
        try:
            # Per Python 2
            if not PY3:
                node = uuid.getnode()
                if node != uuid.getnode():  # Se non è l'indirizzo fallback
                    mac_str = ''.join(("%012X" % node)[i:i + 2] for i in range(0, 12, 2))
                    return mac_str
        except:
            pass

        try:
            with open('/sys/class/net/eth0/address', 'r') as f:
                mac = f.read().strip().upper().replace(':', '')
                if mac and mac != '00:00:00:00:00:00':
                    return mac
        except:
            pass

        return '000000000000'

    def get_memory_info(self):
        try:
            with open("/proc/meminfo") as f:
                mem_total = mem_free = mem_available = 0
                for line in f:
                    if line.startswith("MemTotal:"):
                        mem_total = int(line.split()[1]) // 1024
                    elif line.startswith("MemFree:"):
                        mem_free = int(line.split()[1]) // 1024
                    elif line.startswith("MemAvailable:"):
                        mem_available = int(line.split()[1]) // 1024

                if mem_available > 0:
                    return "RAM: %d MB total, %d MB available" % (mem_total, mem_available)
                else:
                    return "RAM: %d MB total, %d MB free" % (mem_total, mem_free)
        except:
            return "Memory Info: Unknown"

    def _get_installation_id(self):
        try:
            from hashlib import md5
            node = self._get_node()
            # Python 2/3 compatibile
            if PY3:
                return md5(node.encode('utf-8')).hexdigest()
            else:
                return md5(node).hexdigest()
        except:
            return 'unknown'

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
            s.settimeout(2)
            s.connect(("8.8.8.8", 53))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            try:
                import netifaces
                for iface in netifaces.interfaces():
                    if iface.startswith('eth') or iface.startswith('wlan'):
                        addrs = netifaces.ifaddresses(iface)
                        if netifaces.AF_INET in addrs:
                            return addrs[netifaces.AF_INET][0]['addr']
            except:
                pass
            return '127.0.0.1'

    @staticmethod
    def _is_dmm_image():
        try:
            from enigma import eTimer
            timer = eTimer()
            # In DMM images, eTimer ha timeout.connect
            return hasattr(timer, 'timeout')
        except:
            return False

    @staticmethod
    def _is_vti_image():
        try:
            try:
                from inspect import getfullargspec
            except ImportError:
                # Python 2
                from inspect import getargspec as getfullargspec

            from skin import parseSize
            argspec = getfullargspec(parseSize)
            return len(argspec.args) == 2
        except:
            return False

    def get_mount_info(self):
        mount_points = ["/media/hdd", "/media/usb", "/media/sda1", "/media/mmc"]
        for mount_point in mount_points:
            if exists(mount_point):
                try:
                    from os.path import ismount
                    if ismount(mount_point):
                        return "Mount: %s (mounted)" % mount_point
                    else:
                        return "Mount: %s (exists)" % mount_point
                except:
                    return "Mount: %s" % mount_point

        return "Mount: Not Found"

    def get_public_ip(self):
        if not HAS_REQUESTS:
            return self._get_public_ip_fallback()

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
                    ip = response.text.strip()
                    if ip and '.' in ip:  # Validazione base IP
                        return "Public IP: %s" % ip
            except Exception as e:
                print("Error contacting %s: %s" % (service, str(e)))
                continue

        return self._get_public_ip_fallback()

    def _get_public_ip_fallback(self):
        methods = [
            ('curl -s ifconfig.me', 'curl'),
            ('wget -qO - ifconfig.me 2>/dev/null', 'wget'),
            ('dig +short myip.opendns.com @resolver1.opendns.com', 'dig'),
            ('nslookup myip.opendns.com resolver1.opendns.com | grep Address | tail -1 | cut -d" " -f2', 'nslookup')
        ]

        for command, tool in methods:
            try:
                result = popen(command).read().strip()
                if result and '.' in result:  # Validazione base IP
                    return "Public IP: %s (via %s)" % (result, tool)
            except:
                continue

        return "Public IP: Unknown"


stbinfo = StbInfo()


if __name__ == "__main__":
    print("=== STB Info ===")
    print(stbinfo.to_string())
