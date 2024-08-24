#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from enigma import eServiceReference, eServiceCenter
import os
import sys
import re
import glob
import shutil
# ===============================================================================
#
# mod. by Lululla at 20240720
#
# ATTENTION PLEASE...
# This is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2, or (at your option) any later
# version.
# You must not remove the credits at
# all and you must make the modified
# code open to everyone. by Lululla
# ===============================================================================


try:
    from xml.etree.cElementTree import parse
except ImportError:
    from xml.etree.ElementTree import parse

# NAME Digitale Terrestre
plugin_path = os.path.dirname(sys.modules[__name__].__file__)
rules = os.path.join(plugin_path, 'rules.xml')
ServiceListNewLamedb = plugin_path + '/temp/ServiceListNewLamedb'
TrasponderListNewLamedb = plugin_path + '/temp/TrasponderListNewLamedb'
ServOldLamedb = plugin_path + '/temp/ServiceListOldLamedb'
TransOldLamedb = plugin_path + '/temp/TrasponderListOldLamedb'
TerChArch = plugin_path + '/temp/TerrestrialChannelListArchive'
IptvChArch = plugin_path + '/temp'
e2etc = '/etc/enigma2'
ee2ldb = '/etc/enigma2/lamedb'


def ReloadBouquets(x):
    print('\n----Reloading bouquets----\n')
    try:
        from enigma import eDVBDB
    except ImportError:
        eDVBDB = None
    print("\n----Reloading bouquets----")

    # print("\n----Reloading Iptv----")
    # copy_files_to_enigma2

    global setx
    if x == 1:
        setx = 0
        print("\n----Reloading Terrestrial----")
        terrestrial_rest()

    if eDVBDB:
        db = eDVBDB.getInstance()
        if db:
            db.reloadServicelist()
            db.reloadBouquets()
            print("eDVBDB: bouquets reloaded...")
    else:
        os.system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &")
        os.system("wget -qO - http://127.0.0.1/web/servicelistreload?mode=4 > /dev/null 2>&1 &")
        print("wGET: bouquets reloaded...")
    return  # x


def Bouquet():
    for file in os.listdir("/etc/enigma2/"):
        if re.search('^userbouquet.*.tv', file):
            f = open("/etc/enigma2/" + file, "r")
            x = f.read()
            if re.search("#NAME Digitale Terrestre", x, flags=re.IGNORECASE):
                return "/etc/enigma2/" + file
    return


class LCN:
    service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'

    def __init__(self):
        self.dbfile = '/var/etc/enigma2/lcndb'
        self.bouquetfile = Bouquet()
        self.lcnlist = []
        self.markers = []
        self.e2services = []
        mdom = parse(rules)
        '''
        # with open(rules, 'rt') as f:
            # mdom = ET()
            # mdom.parse(f)
        '''
        self.root = None
        for x in mdom.getroot():
            if x.tag == "ruleset" and x.get("name") == 'Italy':
                self.root = x
                return
        return

    def addLcnToList(self, namespace, nid, tsid, sid, lcn, signal):
        for x in self.lcnlist:
            if x[0] == lcn and x[1] == namespace and x[2] == nid and x[3] == tsid and x[4] == sid:
                return
        if lcn == 0:
            return
        for i in range(0, len(self.lcnlist)):
            if self.lcnlist[i][0] == lcn:
                if self.lcnlist[i][5] > signal:
                    self.addLcnToList(namespace, nid, tsid, sid, lcn + 16536, signal)
                else:
                    znamespace = self.lcnlist[i][1]
                    znid = self.lcnlist[i][2]
                    ztsid = self.lcnlist[i][3]
                    zsid = self.lcnlist[i][4]
                    zsignal = self.lcnlist[i][5]
                    self.lcnlist[i][1] = namespace
                    self.lcnlist[i][2] = nid
                    self.lcnlist[i][3] = tsid
                    self.lcnlist[i][4] = sid
                    self.lcnlist[i][5] = signal
                    self.addLcnToList(znamespace, znid, ztsid, zsid, lcn + 16536, zsignal)
                return
            if self.lcnlist[i][0] > lcn:
                self.lcnlist.insert(i, [lcn, namespace, nid, tsid, sid, signal])
                return
        self.lcnlist.append([lcn, namespace, nid, tsid, sid, signal])

    def renumberLcn(self, range, rule):
        tmp = range.split("-")
        if len(tmp) != 2:
            return
        min = int(tmp[0])
        max = int(tmp[1])
        for x in self.lcnlist:
            if x[0] >= min and x[0] <= max:
                value = x[0]
                cmd = "x[0] = " + rule
                try:
                    print('value:', value)
                    exec(cmd)
                except Exception as e:
                    print(e)

    def addMarker(self, position, text):
        self.markers.append([position, text])

    def read(self):
        self.readE2Services()
        try:
            f = open(self.dbfile)
        except Exception as e:
            print(e)
            return
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.strip()
            if len(line) != 38:
                continue
            tmp = line.split(":")
            if len(tmp) != 6:
                continue
            self.addLcnToList(int(tmp[0], 16), int(tmp[1], 16), int(tmp[2], 16), int(tmp[3], 16), int(tmp[4]), int(tmp[5]))
        if self.root is not None:
            for x in self.root:
                if x.tag == "rule":
                    if x.get("type") == "marker":
                        self.addMarker(int(x.get("position")), x.text)
        self.markers.sort(key=lambda z: int(z[0]))

    def readE2Services(self):
        self.e2services = []
        refstr = '%s ORDER BY name' % (self.service_types_tv)
        ref = eServiceReference(refstr)
        serviceHandler = eServiceCenter.getInstance()
        servicelist = serviceHandler.list(ref)
        if servicelist is not None:
            while True:
                service = servicelist.getNext()
                if not service.valid():
                    break
                unsigned_orbpos = service.getUnsignedData(4) >> 16
                if unsigned_orbpos == 0xEEEE or unsigned_orbpos == 61166:  # Terrestrial
                    self.e2services.append(service.toString())
        return

    def ClearDoubleMarker(self, UserBouquet):
        if os.path.exists(UserBouquet):
            ReadFile = open(UserBouquet, "r")
            uBQ = ReadFile.readlines()
            ReadFile.close()
            WriteFile = open(UserBouquet, "w")
            LineMaker = []
            PosDelMaker = []
            x = 1
            for line in uBQ:
                if line.find("#SERVICE 1:64:"):
                    x += 1
                    continue
                elif line.find("#DESCRIPTION"):
                    LineMaker.append(x)
                x += 1
            START = 0
            STOP = 0
            i = 0
            for xx in LineMaker:
                if i + 1 < len(LineMaker):
                    START = LineMaker[i]
                    STOP = LineMaker[i + 1]
                    if STOP - START < 3:
                        PosDelMaker.append(START)
                        PosDelMaker.append(START + 1)
                    if uBQ[START] == uBQ[STOP]:
                        PosDelMaker.append(STOP)
                        PosDelMaker.append(STOP + 1)
                i += 1
            PosDelMaker.reverse()
            for delmark in PosDelMaker:
                del uBQ[delmark - 1]
            for x in uBQ:
                WriteFile.write(x)
            WriteFile.close()

    def writeBouquet(self):
        try:
            f = open(self.bouquetfile, "w")
        except Exception as e:
            print(e)
            return
        f.write("#NAME Digitale Terrestre\n")
        for x in self.lcnlist:
            if len(self.markers) > 0:
                if x[0] > self.markers[0][0]:
                    f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0:\n")
                    f.write("#DESCRIPTION ------- " + self.markers[0][1] + " -------\n")
                    self.markers.remove(self.markers[0])
            refstr = "1:0:1:%x:%x:%x:%x:0:0:0:" % (x[4], x[3], x[2], x[1])  # temporary ref
            refsplit = eServiceReference(refstr).toString().split(":")
            for tref in self.e2services:
                tmp = tref.split(":")
                if tmp[3] == refsplit[3] and tmp[4] == refsplit[4] and tmp[5] == refsplit[5] and tmp[6] == refsplit[6]:
                    f.write("#SERVICE " + tref + "\n")
                    break
        f.close()
        self.ClearDoubleMarker(self.bouquetfile)

    def reloadBouquets(self):
        ReloadBouquets(0)


def terrestrial():
    SavingProcessTerrestrialChannels = StartSavingTerrestrialChannels()
    import time
    now = time.time()
    ttime = time.localtime(now)
    tt = str('{0:02d}'.format(ttime[2])) + str('{0:02d}'.format(ttime[1])) + str(ttime[0])[2:] + '_' + str('{0:02d}'.format(ttime[3])) + str('{0:02d}'.format(ttime[4])) + str('{0:02d}'.format(ttime[5]))
    os.system('tar -czvf /tmp/' + tt + '_enigma2settingsbackup.tar.gz' + ' -C / /etc/enigma2/*.tv /etc/enigma2/*.radio /etc/enigma2/lamedb')
    if SavingProcessTerrestrialChannels:
        print('SavingProcessTerrestrialChannels')
    return


def SearchIPTV():
    iptv_list = []
    for iptv_file in sorted(glob.glob("/etc/enigma2/userbouquet.*.tv")):
        usbq = open(iptv_file, "r").read()
        usbq_lines = usbq.strip().lower()
        if "http" in usbq_lines:
            iptv_list.append(os.path.basename(iptv_file))

    if not iptv_list:
        return False
    else:
        return iptv_list


def keepiptv():
    iptv_to_save = SearchIPTV()
    print('iptv_to_save:', iptv_to_save)
    if iptv_to_save:
        for iptv in iptv_to_save:
            cmnd = "cp -rf /etc/enigma2/" + iptv + " " + IptvChArch + '/' + iptv
            print('cmnd:', cmnd)
            os.system(cmnd)
        return True
    return False


def terrestrial_rest():
    if LamedbRestore():
        TransferBouquetTerrestrialFinal()
        # terrr = os.path.join(plugin_path, 'temp/TerrestrialChannelListArchive')
        terrr = plugin_path + '/temp/TerrestrialChannelListArchive'
        if os.path.exists(terrr):
            os.system("cp -rf " + plugin_path + "/temp/TerrestrialChannelListArchive /etc/enigma2/userbouquet.terrestrial.tv")
        os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
        with open('/etc/enigma2/bouquets.tv', 'r+') as f:
            bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n'
            if bouquetTvString not in f:
                new_bouquet = open('/etc/enigma2/new_bouquets.tv', 'w')
                new_bouquet.write('#NAME User - bouquets (TV)\n')
                new_bouquet.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial.tv" ORDER BY bouquet\n')
                file_read = open('/etc/enigma2/bouquets.tv').readlines()
                for line in file_read:
                    if line.startswith("#NAME"):
                        continue
                    new_bouquet.write(line)
                new_bouquet.close()
                os.system('cp -rf /etc/enigma2/bouquets.tv /etc/enigma2/backup_bouquets.tv')
                os.system('mv -f /etc/enigma2/new_bouquets.tv /etc/enigma2/bouquets.tv')
        if os.path.exists('/etc/enigma2/lcndb'):
            lcnstart()


def copy_files_to_enigma2():
    IptvChArch = plugin_path + '/temp'
    enigma2_folder = "/etc/enigma2"
    bouquet_file = os.path.join(enigma2_folder, "bouquets.tv")

    # Copia i file dalla cartella temporanea a /etc/enigma2
    for filename in os.listdir(IptvChArch):
        if filename.endswith(".tv"):
            src_path = os.path.join(IptvChArch, filename)
            dst_path = os.path.join(enigma2_folder, filename)
            shutil.copy(src_path, dst_path)

            # Aggiungi il nome del file al file bouquet.tv
            with open(bouquet_file, "r+") as f:
                line = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "{}" ORDER BY bouquet\n'.format(filename)
                if line not in f:
                    f.write(line)
    print("Operazione completata!")


def lcnstart():
    print(' lcnstart ')
    if os.path.exists('/etc/enigma2/lcndb'):
        lcn = LCN()
        lcn.read()
        if len(lcn.lcnlist) >= 1:
            lcn.writeBouquet()
            ReloadBouquets(0)
    return


def StartSavingTerrestrialChannels():

    def ForceSearchBouquetTerrestrial():
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            f = open(file, "r").read()
            x = f.strip().lower()
            if x.find('eeee') != -1:
                return file
                break
        return

    def ResearchBouquetTerrestrial(search):
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            f = open(file, "r").read()
            x = f.strip().lower()
            x1 = f.strip()
            if x1.find("#NAME") != -1:
                if x.lower().find(search.lower()) != -1:
                    if x.find('eeee') != -1:
                        return file
                        break
        return

    def SaveTrasponderService():
        TrasponderListOldLamedb = open(TransOldLamedb, 'w')
        ServiceListOldLamedb = open(ServOldLamedb, 'w')
        Trasponder = False
        inTransponder = False
        inService = False
        try:
            LamedbFile = open(ee2ldb, 'r')
            while 1:
                line = LamedbFile.readline()
                if not line:
                    break
                if not (inTransponder or inService):
                    if line.find('transponders') == 0:
                        inTransponder = True
                    if line.find('services') == 0:
                        inService = True
                if line.find('end') == 0:
                    inTransponder = False
                    inService = False
                line = line.lower()
                if line.find('eeee') != -1:
                    Trasponder = True
                    if inTransponder:
                        TrasponderListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        TrasponderListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        TrasponderListOldLamedb.write(line)
                    if inService:
                        tmp = line.split(':')
                        ServiceListOldLamedb.write(tmp[0] + ":" + tmp[1] + ":" + tmp[2] + ":" + tmp[3] + ":" + tmp[4] + ":0\n")
                        line = LamedbFile.readline()
                        ServiceListOldLamedb.write(line)
                        line = LamedbFile.readline()
                        ServiceListOldLamedb.write(line)
            TrasponderListOldLamedb.close()
            ServiceListOldLamedb.close()
            if not Trasponder:
                os.system('rm -fr ' + TransOldLamedb)
                os.system('rm -fr ' + ServOldLamedb)
        except:
            pass
        return Trasponder

    def CreateBouquetForce():
        WritingBouquetTemporary = open(TerChArch, 'w')
        WritingBouquetTemporary.write('#NAME terrestre\n')
        ReadingTempServicelist = open(ServOldLamedb, 'r').readlines()
        for jx in ReadingTempServicelist:
            if jx.find('eeee') != -1:
                String = jx.split(':')
                WritingBouquetTemporary.write('#SERVICE 1:0:%s:%s:%s:%s:%s:0:0:0:\n' % (hex(int(String[4]))[2:], String[0], String[2], String[3], String[1]))
        WritingBouquetTemporary.close()

    def SaveBouquetTerrestrial():
        NameDirectory = ResearchBouquetTerrestrial('terr')
        if not NameDirectory:
            NameDirectory = ForceSearchBouquetTerrestrial()
        try:
            shutil.copyfile(NameDirectory, TerChArch)
            return True
        except:
            pass
        return
    Service = SaveTrasponderService()
    if Service:
        if not SaveBouquetTerrestrial():
            CreateBouquetForce()
        return True
    return


def LamedbRestore():
    try:
        TrasponderListNewLamedb = open(plugin_path + '/temp/TrasponderListNewLamedb', 'w')
        ServiceListNewLamedb = open(plugin_path + '/temp/ServiceListNewLamedb', 'w')
        inTransponder = False
        inService = False
        infile = open(ee2ldb, 'r')
        while 1:
            line = infile.readline()
            if not line:
                break
            if not (inTransponder or inService):
                if line.find('transponders') == 0:
                    inTransponder = True
                if line.find('services') == 0:
                    inService = True
            if line.find('end') == 0:
                inTransponder = False
                inService = False
            if inTransponder:
                TrasponderListNewLamedb.write(line)
            if inService:
                ServiceListNewLamedb.write(line)
        TrasponderListNewLamedb.close()
        ServiceListNewLamedb.close()
        WritingLamedbFinal = open(ee2ldb, "w")
        WritingLamedbFinal.write("eDVB services /4/\n")
        TrasponderListNewLamedb = open(plugin_path + '/temp/TrasponderListNewLamedb', 'r').readlines()
        for x in TrasponderListNewLamedb:
            WritingLamedbFinal.write(x)
        try:
            TrasponderListOldLamedb = open(TransOldLamedb, 'r').readlines()
            for x in TrasponderListOldLamedb:
                WritingLamedbFinal.write(x)
        except:
            pass
        WritingLamedbFinal.write("end\n")
        ServiceListNewLamedb = open(plugin_path + '/temp/ServiceListNewLamedb', 'r').readlines()
        for x in ServiceListNewLamedb:
            WritingLamedbFinal.write(x)
        try:
            ServiceListOldLamedb = open(ServOldLamedb, 'r').readlines()
            for x in ServiceListOldLamedb:
                WritingLamedbFinal.write(x)
        except:
            pass
        WritingLamedbFinal.write("end\n")
        WritingLamedbFinal.close()
        return True
    except:
        return False


def TransferBouquetTerrestrialFinal():

    def RestoreTerrestrial():
        for file in os.listdir("/etc/enigma2/"):
            if re.search('^userbouquet.*.tv', file):
                f = open("/etc/enigma2/" + file, "r")
                x = f.read()
                if re.search('#NAME Digitale Terrestre', x, flags=re.IGNORECASE) or re.search('#NAME DTT', x, flags=re.IGNORECASE):  # for disa51
                    return "/etc/enigma2/" + file
        return

    try:
        TerrestrialChannelListArchive = open(TerChArch, 'r').readlines()
        DirectoryUserBouquetTerrestrial = RestoreTerrestrial()
        if DirectoryUserBouquetTerrestrial:
            TrasfBouq = open(DirectoryUserBouquetTerrestrial, 'w')
            for Line in TerrestrialChannelListArchive:
                if Line.lower().find('#name') != -1:
                    TrasfBouq.write('#NAME Digitale Terrestre\n')
                else:
                    TrasfBouq.write(Line)
            TrasfBouq.close()
            return True
    except:
        return False
    return

# ===== by lululla
