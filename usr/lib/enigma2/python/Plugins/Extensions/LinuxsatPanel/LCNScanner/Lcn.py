#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from .. import _

from enigma import (eServiceReference, eServiceCenter)
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Tools.Directories import (resolveFilename, SCOPE_PLUGINS)
from Components.config import (
    getConfigListEntry,
    config,
    ConfigSubsection,
    ConfigYesNo,
    ConfigSelection,
    configfile,
)

import os
import sys
import re
import glob
import shutil


try:
    from xml.etree.cElementTree import parse
except ImportError:
    from xml.etree.ElementTree import parse


# plugin_path = os.path.dirname(sys.modules[__name__].__file__)
plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('LinuxsatPanel'))
rules = os.path.join(plugin_path, 'LCNScanner/rules.xml')
ServiceListNewLamedb = plugin_path + '/temp/ServiceListNewLamedb'
TrasponderListNewLamedb = plugin_path + '/temp/TrasponderListNewLamedb'
ServOldLamedb = plugin_path + '/temp/ServiceListOldLamedb'
TransOldLamedb = plugin_path + '/temp/TrasponderListOldLamedb'
TerChArch = plugin_path + '/temp/TerrestrialChannelListArchive'
IptvChArch = plugin_path + '/temp'
e2etc = '/etc/enigma2'
ee2ldb = '/etc/enigma2/lamedb'
dbfile = '/var/etc/enigma2/lcndb'


def ReloadBouquets(x):
    print('\n----Reloading bouquets----\n')
    try:
        from enigma import eDVBDB
    except ImportError:
        eDVBDB = None
    print("\n----Reloading bouquets----")

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
    return


def Bouquet():
    for file in os.listdir("/etc/enigma2/"):
        if re.search('^userbouquet.*.tv', file):
            f = open("/etc/enigma2/" + file, "r")
            x = f.read()
            if re.search("#NAME Digitale Terrestre", x, flags=re.IGNORECASE):
                return "/etc/enigma2/" + file
            elif re.search("#NAME Terrestrial TV LCN", x, flags=re.IGNORECASE):
                return "/etc/enigma2/" + file
    return


class LCN():
    service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'
    service_types_radio = '1:7:2:0:0:0:0:0:0:0:(type == 2)'

    def __init__(self):
        self.bouquetfile = Bouquet()
        self.lcnlist = []
        self.markers = []
        self.e2services = []
        mdom = parse(rules)
        self.root = None
        for x in mdom.getroot():
            if x.tag == "rules" and x.get("name") == 'Default':
                self.root = x
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
            elif self.lcnlist[i][0] > lcn:
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

    def read(self, serviceType):
        self.readE2Services(serviceType)
        try:
            with open(dbfile) as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    line = line.strip()
                    if len(line) != 38:
                        continue
                    tmp = line.split(":")
                    if len(tmp) != 6:
                        continue
                    self.addLcnToList(int(tmp[0], 16), int(tmp[1], 16), int(tmp[2], 16), int(tmp[3], 16), int(tmp[4]), int(tmp[5]))

        except Exception as e:
            print("Errore durante la lettura del file:", e)
            return

        if self.root is not None:
            for x in self.root:
                if x.tag == "rule":
                    if x.get("type") == "renumber":
                        self.renumberLcn(x.get("range"), x.text)
                        self.lcnlist.sort(key=lambda z: int(z[0]))
                    elif x.get("type") == "marker":
                        self.addMarker(int(x.get("position")), x.text)
        self.markers.sort(key=lambda z: int(z[0]))

    def readE2Services(self, serviceType):
        self.e2services = []
        if serviceType == "TV":
            refstr = '%s ORDER BY name' % (self.service_types_tv)
        elif serviceType == "RADIO":
            refstr = '%s ORDER BY name' % (self.service_types_radio)
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

    def ClearDoubleMarker(self, UserBouquet):
        if not os.path.exists(UserBouquet):
            print("File UserBouquet non trovato.", UserBouquet)
            return

        try:
            with open(UserBouquet, "r") as read_file:
                uBQ = read_file.readlines()

            LineMaker = []
            PosDelMaker = []
            x = 1
            for line in uBQ:
                if "#SERVICE 1:64:" in line:
                    x += 1
                    continue
                elif "#DESCRIPTION" in line:
                    LineMaker.append(x)
                x += 1

            for i in range(len(LineMaker) - 1):
                START = LineMaker[i]
                STOP = LineMaker[i + 1]
                if STOP - START < 3:
                    PosDelMaker.extend([START, START + 1])
                if uBQ[START] == uBQ[STOP]:
                    PosDelMaker.extend([STOP, STOP + 1])
            PosDelMaker = sorted(set(PosDelMaker), reverse=True)
            for delmark in PosDelMaker:
                del uBQ[delmark - 1]
            with open(UserBouquet, "w") as write_file:
                write_file.writelines(uBQ)

        except Exception as e:
            print("Errore durante la gestione del file UserBouquet:", e)

    def writeBouquet(self):
        dttbouquet = Bouquet()
        try:
            with open(dttbouquet, "w") as f:
                self.newlist = []
                count = 0
                for x in self.lcnlist:
                    count += 1
                    while x[0] != count:
                        self.newlist.append([count, 11111111, 11111, 111, 111, 111111])
                        count += 1
                    if x[0] == count:
                        self.newlist.append(x)

                f.write("#NAME Terrestrial TV LCN\n")
                f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0::Terrestrial TV LCN\n")
                f.write("##DESCRIPTION Terrestrial TV LCN\n")

                for x in self.newlist:
                    if int(x[1]) == 11111111:
                        f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
                        continue
                    if len(self.markers) > 0 and x[0] > self.markers[0][0]:
                        f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0:\n")
                        f.write("#DESCRIPTION ------- " + self.markers[0][1] + " -------\n")
                        self.markers.pop(0)  # Rimuove il primo marker

                    refstr = "1:0:1:%x:%x:%x:%x:0:0:0:" % (x[4], x[3], x[2], x[1])
                    refsplit = eServiceReference(refstr).toString().split(":")
                    added = False
                    for tref in self.e2services:
                        tmp = tref.split(":")
                        if (tmp[3] == refsplit[3] and tmp[4] == refsplit[4] and
                                tmp[5] == refsplit[5] and tmp[6] == refsplit[6]):
                            f.write("#SERVICE " + tref + "\n")
                            added = True
                            break
                    if not added:
                        f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
            self.addInTVBouquets()
        except Exception as e:
            print("Errore nella scrittura del bouquet: ", str(e))

    def addInTVBouquets(self):
        try:
            with open('/etc/enigma2/bouquets.tv', 'r') as f:
                ret = f.read().splitlines()
            dttbouquet_str = Bouquet()  # "FROM BOUQUET \"userbouquet.terrestrial_lcn.tv\""
            for line in ret:
                if dttbouquet_str in line:
                    return
            with open('/etc/enigma2/bouquets.tv', 'w') as f:
                f.write(ret[0] + "\n")
                f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial_lcn.tv" ORDER BY bouquet\n')
                for line in ret[1:]:
                    f.write(line + "\n")
        except Exception as e:
            print("Errore nell'aggiunta del bouquet TV: ", str(e))

    def writeRadioBouquet(self):
        try:
            with open('/etc/enigma2/userbouquet.terrestrial_lcn.radio', "w") as f:
                self.newlist = []
                count = 0
                for x in self.lcnlist:
                    count += 1
                    while x[0] != count:
                        self.newlist.append([count, 11111111, 11111, 111, 111, 111111])
                        count += 1
                    if x[0] == count:
                        self.newlist.append(x)

                f.write("#NAME Terrestrial Radio LCN\n")
                f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0::Terrestrial RADIO LCN\n")
                f.write("##DESCRIPTION Terrestrial RADIO LCN\n")

                for x in self.newlist:
                    if int(x[1]) == 11111111:
                        f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
                        continue

                    if len(self.markers) > 0 and x[0] > self.markers[0][0]:
                        f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0:\n")
                        f.write("#DESCRIPTION ------- " + self.markers[0][1] + " -------\n")
                        self.markers.pop(0)

                    refstr = "1:0:2:%x:%x:%x:%x:0:0:0:" % (x[4], x[3], x[2], x[1])
                    refsplit = eServiceReference(refstr).toString().split(":")
                    added = False

                    for tref in self.e2services:
                        tmp = tref.split(":")
                        if tmp[3] == refsplit[3] and tmp[4] == refsplit[4] and tmp[5] == refsplit[5] and tmp[6] == refsplit[6]:
                            f.write("#SERVICE " + tref + "\n")
                            added = True
                            break

                    if not added:
                        f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
                        print("Servizio non trovato per riferimento: ", refsplit)

            self.addInRadioBouquets()

        except Exception as e:
            print("Errore nella scrittura del bouquet radio: ", str(e))

    def addInRadioBouquets(self):
        radio_file = '/etc/enigma2/bouquets.radio'
        with open(radio_file, 'r') as f:
            ret = f.readlines()
        if any("userbouquet.terrestrial_lcn.radio" in line for line in ret):
            return
        with open(radio_file, 'w') as f:
            f.write(ret[0].strip() + "\n")
            f.write('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial_lcn.radio" ORDER BY bouquet\n')
            f.writelines(ret[1:])

    def reloadBouquets(self):
        ReloadBouquets(0)


class LCNBuildHelper():
    def __init__(self):
        self.bouquetlist = []
        for x in self.readBouquetsTvList("/etc/enigma2"):
            self.bouquetlist.append((x[0], x[1]))

        self.rulelist = []
        mdom = parse(os.path.dirname(sys.modules[__name__].__file__) + "/rules.xml")
        for x in mdom.getroot():
            if x.tag == "rules":
                self.rulelist.append((x.get("name"), x.get("name")))
        config.lcn = ConfigSubsection()
        config.lcn.enabled = ConfigYesNo(True)
        config.lcn.bouquet = ConfigSelection(default="userbouquet.LastScanned.tv", choices=self.bouquetlist)  # not used instead self.bouquetfile
        config.lcn.rules = ConfigSelection(self.rulelist)

    def readBouquetsTvList(self, pwd):
        return self.readBouquetsList(pwd, "bouquets.tv")

    def readBouquetsRadioList(self, pwd):
        return self.readBouquetsList(pwd, "bouquets.radio")

    def readBouquetsList(self, pwd, bouquetname):
        try:
            f = open(pwd + "/" + bouquetname)
        except Exception as e:
            print(e)
            return

        ret = []

        while True:
            line = f.readline()
            if line == "":
                break

            if line[:8] != "#SERVICE":
                continue

            tmp = line.strip().split(":")
            line = tmp[len(tmp) - 1]

            filename = None
            if line[:12] == "FROM BOUQUET":
                tmp = line[13:].split(" ")
                filename = tmp[0].strip("\"")
            else:
                filename = line

            if filename:
                try:
                    fb = open(pwd + "/" + filename)
                except Exception as e:
                    print(e)
                    continue

                tmp = fb.readline().strip()
                if tmp[:6] == "#NAME ":
                    ret.append([filename, tmp[6:]])
                else:
                    ret.append([filename, filename])
                fb.close()

        return ret

    def buildAfterScan(self):
        if config.lcn.enabled.value is True:
            self.buildlcn(True)

    def buildlcn(self, suppressmessages=False):
        rule = self.rulelist[0][0]
        for x in self.rulelist:
            if x[0] == config.lcn.rules.value:
                rule = x[0]
                print('rule:', rule)
                break

        bouquet = self.rulelist[0][0]
        self.bouquetfile = Bouquet()
        for x in self.bouquetlist:
            if x[0] == self.bouquetfile:
                bouquet = x[0]
                print('bouquet:', bouquet)
                break

        lcn = LCN()
        lcn.read("TV")
        if len(lcn.lcnlist) > 0:
            lcn.writeBouquet()
        else:
            if not suppressmessages:
                self.session.open(MessageBox, _("No entry in lcn db. Please do a service scan."), MessageBox.TYPE_INFO)

        lcn.read("RADIO")
        if len(lcn.lcnlist) > 0:
            lcn.writeRadioBouquet()
        else:
            if not suppressmessages:
                self.session.open(MessageBox, _("No entry in lcn db. Please do a service scan."), MessageBox.TYPE_INFO)
        print('reload blouquet=======')
        lcn.reloadBouquets()


class LCNScannerPlugin(Screen, ConfigListScreen, LCNBuildHelper):
    skin = """
        <screen position="center,center" size="560,400" title="LCN Scanner">
            <widget name="config" position="5,5" size="550,350" scrollbarMode="showOnDemand" zPosition="1"/>
            <widget name="key_red" position="0,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
            <widget name="key_green" position="140,360" size="140,40" valign="center" halign="center" zPosition="5" transparent="1" foregroundColor="white" font="Regular;18"/>
            <ePixmap name="red" pixmap="skin_default/buttons/red.png" position="0,360" size="140,40" zPosition="4" transparent="1" alphatest="on"/>
            <ePixmap name="green" pixmap="skin_default/buttons/green.png" position="140,360" size="140,40" zPosition="4" transparent="1" alphatest="on"/>
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        LCNBuildHelper.__init__(self)

        self.list = [
            getConfigListEntry(_("Enable terrestrial LCN:"), config.lcn.enabled),
            getConfigListEntry(_("Terrestrial bouquet:"), config.lcn.bouquet),
            getConfigListEntry(_("LCN rules:"), config.lcn.rules),
        ]

        ConfigListScreen.__init__(self, self.list, session=session)
        self["key_red"] = Button(_("Rebuild"))
        self["key_green"] = Button(_("Exit"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                    {"red": self.ok,
                                     "green": self.keyCancel,
                                     "cancel": self.keyCancel}, -2)

    def confirm(self, confirmed):
        if confirmed:
            self.buildlcn()

        self.keySave()
        configfile.save()

    def ok(self):
        if config.lcn.enabled.value is True:
            self.session.openWithCallback(self.confirm, MessageBox, _("Rebuild LCN bouquet now?"), MessageBox.TYPE_YESNO, default=True)
        else:
            self.keySave()
            configfile.save()


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
        with open(iptv_file, "r") as file:
            usbq_lines = file.read().strip().lower()
            if "http" in usbq_lines:
                iptv_list.append(os.path.basename(iptv_file))
    return iptv_list if iptv_list else False


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
        if os.path.exists(dbfile):
            lcnstart()


def copy_files_to_enigma2():

    IptvChArch = plugin_path + '/temp'
    enigma2_folder = "/etc/enigma2"
    bouquet_file = os.path.join(enigma2_folder, "bouquets.tv")
    for filename in os.listdir(IptvChArch):
        if filename.endswith(".tv"):
            src_path = os.path.join(IptvChArch, filename)
            dst_path = os.path.join(enigma2_folder, filename)
            shutil.copy(src_path, dst_path)
            with open(bouquet_file, "r+") as f:
                line = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "{}" ORDER BY bouquet\n'.format(filename)
                if line not in f:
                    f.write(line)
    print("Operazione completata!")


def lcnstart():
    print(' lcnstart ')
    if os.path.exists(dbfile):
        '''
        # lcn = LCN()
        # lcn.read()
        # if len(lcn.lcnlist) >= 1:
            # lcn.writeBouquet()
            # ReloadBouquets(0)
        '''
        try:
            lcn = LCNBuildHelper()
            lcn.buildAfterScan()
        except Exception as e:
            print(e)
    return


def StartSavingTerrestrialChannels():

    def ForceSearchBouquetTerrestrial():
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            with open(file, "r") as f:
                content = f.read().strip().lower()
                if 'eeee' in content:
                    return file
        return

    def ResearchBouquetTerrestrial(search):
        search_lower = search.lower()
        for file in sorted(glob.glob("/etc/enigma2/*.tv")):
            with open(file, "r") as f:
                content = f.read().strip()
                content_lower = content.lower()
                if "#NAME" in content:
                    if search_lower in content_lower:
                        if 'eeee' in content_lower:
                            return file
        return

    def SaveTrasponderService():
        Trasponder = False
        inTransponder = False
        inService = False
        try:
            with open(TransOldLamedb, 'w') as TrasponderListOldLamedb, open(ServOldLamedb, 'w') as ServiceListOldLamedb:
                with open(ee2ldb, 'r') as LamedbFile:
                    for line in LamedbFile:
                        line = line.strip()

                        if not (inTransponder or inService):
                            if line.startswith('transponders'):
                                inTransponder = True
                            elif line.startswith('services'):
                                inService = True

                        if line.startswith('end'):
                            inTransponder = False
                            inService = False

                        line_lower = line.lower()
                        if 'eeee' in line_lower:
                            Trasponder = True
                            if inTransponder:
                                TrasponderListOldLamedb.write(line_lower + "\n")
                                for i in range(2):
                                    line = next(LamedbFile).strip()
                                    TrasponderListOldLamedb.write(line + "\n")
                            elif inService:
                                tmp = line.split(':')
                                ServiceListOldLamedb.write(':'.join(tmp[:5]) + ":0\n")
                                for i in range(2):
                                    line = next(LamedbFile).strip()
                                    ServiceListOldLamedb.write(line + "\n")

            if not Trasponder:
                os.remove(TransOldLamedb)
                os.remove(ServOldLamedb)

        except Exception as e:
            print("Errore durante il processo:", e)

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
        with open(plugin_path + '/temp/TrasponderListNewLamedb', 'w') as TransNew, \
             open(plugin_path + '/temp/ServiceListNewLamedb', 'w') as ServNew:
            inTransponder = False
            inService = False

            with open(ee2ldb, 'r') as infile:
                for line in infile:
                    line = line.strip()
                    if not (inTransponder or inService):
                        if line.startswith('transponders'):
                            inTransponder = True
                        elif line.startswith('services'):
                            inService = True
                    if line.startswith('end'):
                        inTransponder = False
                        inService = False
                    if inTransponder:
                        TransNew.write(line + "\n")
                    if inService:
                        ServNew.write(line + "\n")

        with open(ee2ldb, "w") as WritingLamedbFinal:
            WritingLamedbFinal.write("eDVB services /4/\n")

            with open(plugin_path + '/temp/TrasponderListNewLamedb', 'r') as TransNew:
                WritingLamedbFinal.writelines(TransNew)

            try:
                with open(TransOldLamedb, 'r') as TransOld:
                    WritingLamedbFinal.writelines(TransOld)
            except FileNotFoundError:
                pass

            WritingLamedbFinal.write("end\n")

            with open(plugin_path + '/temp/ServiceListNewLamedb', 'r') as ServNew:
                WritingLamedbFinal.writelines(ServNew)

            try:
                with open(ServOldLamedb, 'r') as ServOld:
                    WritingLamedbFinal.writelines(ServOld)
            except FileNotFoundError:
                pass

            WritingLamedbFinal.write("end\n")
        return True
    except Exception as e:
        print("Errore durante il ripristino del lamedb:", e)
        return False


def TransferBouquetTerrestrialFinal():

    def RestoreTerrestrial(TerChArch):
        def find_terrestrial_bouquet():
            for file in os.listdir("/etc/enigma2/"):
                if re.search(r'^userbouquet.*\.tv$', file):
                    with open("/etc/enigma2/" + file, "r") as f:
                        content = f.read()
                        if re.search(r'#NAME Digitale Terrestre', content, flags=re.IGNORECASE) or \
                           re.search(r'#NAME DTT', content, flags=re.IGNORECASE) or \
                           re.search(r'#NAME Terrestrial TV LCN', content, flags=re.IGNORECASE):
                            return "/etc/enigma2/" + file
            return None

        try:
            with open(TerChArch, 'r') as archive_file:
                terrestrial_channel_list = archive_file.readlines()

            terrestrial_bouquet_path = find_terrestrial_bouquet()
            if terrestrial_bouquet_path:
                with open(terrestrial_bouquet_path, 'w') as bouquet_file:
                    for line in terrestrial_channel_list:
                        if '#NAME' in line.lower():
                            bouquet_file.write('#NAME Digitale Terrestre\n')
                        else:
                            bouquet_file.write(line)
                return True
        except Exception as e:
            print("Errore durante il ripristino del bouquet:", e)
            return False


# ===== by lululla
