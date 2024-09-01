#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from enigma import (eServiceReference, eServiceCenter)
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
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


class LCN():
    service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'
    service_types_radio = '1:7:2:0:0:0:0:0:0:0:(type == 2)'

    def __init__(self):
        # def __init__(self, dbfile, rulefile, rulename, bouquetfile):
        # self.dbfile = dbfile
        # self.bouquetfile = bouquetfile
        self.dbfile = '/var/etc/enigma2/lcndb'
        self.bouquetfile = Bouquet()
        self.lcnlist = []
        self.markers = []
        self.e2services = []
        mdom = parse(rules)
        # mdom = xml.etree.cElementTree.parse(rulefile)
        self.root = None
        for x in mdom.getroot():
            # if x.tag == "ruleset" and x.get("name") == rulename:
            if x.tag == "ruleset" and x.get("name") == 'Italy':
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
        # def read(self):
        # self.readE2Services()
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
            f = open('/etc/enigma2/userbouquet.terrestrial_lcn.tv', "w")
            # f = open(self.bouquetfile, "w")
        except Exception as e:
            print(e)
            return

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
                # print x[0], " Detected 111111111111 service"
                f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
                continue

            if len(self.markers) > 0:
                if x[0] > self.markers[0][0]:
                    f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0:\n")
                    f.write("#DESCRIPTION ------- " + self.markers[0][1] + " -------\n")
                    self.markers.remove(self.markers[0])
            refstr = "1:0:1:%x:%x:%x:%x:0:0:0:" % (x[4], x[3], x[2], x[1])  # temporary ref
            refsplit = eServiceReference(refstr).toString().split(":")
            added = False
            for tref in self.e2services:
                tmp = tref.split(":")
                if tmp[3] == refsplit[3] and tmp[4] == refsplit[4] and tmp[5] == refsplit[5] and tmp[6] == refsplit[6]:
                    f.write("#SERVICE " + tref + "\n")
                    added = True
                    break

            if not added:  # no service found? something wrong? a log should be a good idea. Anyway we add an empty line so we keep the numeration
                f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")

        f.close()
        self.addInTVBouquets()
        # self.ClearDoubleMarker(self.bouquetfile)

    def addInTVBouquets(self):
        f = open('/etc/enigma2/bouquets.tv', 'r')
        ret = f.read().split("\n")
        f.close()

        i = 0
        while i < len(ret):
            if ret[i].find("userbouquet.terrestrial_lcn.tv") >= 0:
                return
            i += 1

        f = open('/etc/enigma2/bouquets.tv', 'w')
        f.write(ret[0] + "\n")
        f.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial_lcn.tv" ORDER BY bouquet\n')
        i = 1
        while i < len(ret):
            f.write(ret[i] + "\n")
            i += 1

    def writeRadioBouquet(self):
        try:
            f = open('/etc/enigma2/userbouquet.terrestrial_lcn.radio', "w")
        except Exception as e:
            print(e)
            return

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
                # print x[0], " Detected 111111111111 service"
                f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")
                continue

            if len(self.markers) > 0:
                if x[0] > self.markers[0][0]:
                    f.write("#SERVICE 1:64:0:0:0:0:0:0:0:0:\n")
                    f.write("#DESCRIPTION ------- " + self.markers[0][1] + " -------\n")
                    self.markers.remove(self.markers[0])
            refstr = "1:0:2:%x:%x:%x:%x:0:0:0:" % (x[4], x[3], x[2], x[1])  # temporary ref
            refsplit = eServiceReference(refstr).toString().split(":")
            added = False
            for tref in self.e2services:
                tmp = tref.split(":")
                if tmp[3] == refsplit[3] and tmp[4] == refsplit[4] and tmp[5] == refsplit[5] and tmp[6] == refsplit[6]:
                    f.write("#SERVICE " + tref + "\n")
                    added = True
                    break

            if not added:  # no service found? something wrong? a log should be a good idea. Anyway we add an empty line so we keep the numeration
                f.write("#SERVICE 1:832:d:0:0:0:0:0:0:0:\n")

        f.close()
        self.addInRadioBouquets()

    def addInRadioBouquets(self):
        f = open('/etc/enigma2/bouquets.radio', 'r')
        ret = f.read().split("\n")
        f.close()

        i = 0
        while i < len(ret):
            if ret[i].find("userbouquet.terrestrial_lcn.radio") >= 0:
                return
            i += 1

        f = open('/etc/enigma2/bouquets.radio', 'w')
        f.write(ret[0] + "\n")
        f.write('#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.terrestrial_lcn.radio" ORDER BY bouquet\n')
        i = 1
        while i < len(ret):
            f.write(ret[i] + "\n")
            i += 1

    def reloadBouquets(self):
        # eDVBDB.getInstance().reloadBouquets()
        ReloadBouquets(0)


class LCNBuildHelper():
    def __init__(self):
        self.bouquetlist = []
        for x in self.readBouquetsTvList("/etc/enigma2"):
            self.bouquetlist.append((x[0], x[1]))

        self.rulelist = []
        mdom = parse(os.path.dirname(sys.modules[__name__].__file__) + "/rules.xml")
        for x in mdom.getroot():
            if x.tag == "ruleset":
                self.rulelist.append((x.get("name"), x.get("name")))
            # if x.tag == "ruleset" and x.get("name") == 'Italy':
                # self.rulelist.append((x.get("name"), x.get("name")))

        config.lcn = ConfigSubsection()
        config.lcn.enabled = ConfigYesNo(True)
        config.lcn.bouquet = ConfigSelection(default="userbouquet.LastScanned.tv", choices=self.bouquetlist)
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
                break

        bouquet = self.rulelist[0][0]
        for x in self.bouquetlist:
            if x[0] == config.lcn.bouquet.value:
                bouquet = x[0]
                break

        # lcn = LCN(resolveFilename(SCOPE_CONFIG, "lcndb"), os.path.dirname(sys.modules[__name__].__file__) + "/rules.xml", rule, resolveFilename(SCOPE_CONFIG, bouquet))
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

    # def reloadBouquets(self):
        # ReloadBouquets(0)


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


'''
# def LCNScannerMain(session, **kwargs):
    # session.open(LCNScannerPlugin)


# def LCNScannerSetup(menuid, **kwargs):
    # if menuid == "scan":
        # return [("LCN Scanner", LCNScannerMain, "lcnscanner", None)]
    # else:
        # return []


# def Plugins(**kwargs):
    # return PluginDescriptor(name="LCN", description=_("LCN plugin for DVB-T/T2 services"), where=PluginDescriptor.WHERE_MENU, fnc=LCNScannerSetup)
    # # return PluginDescriptor(name="LCN", description=_("LCN plugin for DVB-T/T2 services"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc=LCNScannerMain)
'''
