# Based on a plugin from Sif Team.
# This version created by IanSav and the OpenATV team.

from Components.PluginComponent import plugins
from Components.config import ConfigSelection, ConfigSubsection, ConfigYesNo, config
from Tools.Directories import SCOPE_CONFIG, SCOPE_PLUGIN_ABSOLUTE, fileReadLines, fileReadXML, fileWriteLines, resolveFilename
from enigma import eDVBDB, eServiceCenter, eServiceReference
from os.path import join
from sys import maxsize
import glob
import os
import re
import sys

MODULE_NAME = __name__.split(".")[-1]

config.plugins.LCNScanner = ConfigSubsection()
config.plugins.LCNScanner.showInPluginsList = ConfigYesNo(default=False)
config.plugins.LCNScanner.showInPluginsList.addNotifier(plugins.reloadPlugins, initial_call=False, immediate_feedback=False)


class LCNScanner:
    MODE_TV = "1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)"
    MODE_RADIO = "1:7:2:0:0:0:0:0:0:0:(type == 2) || (type == 10)"
    MODES = {
        "TV": (1, 17, 22, 25, 134, 195),
        "Radio": (2, 10)
    }

    OLDDB_NAMESPACE = 0
    OLDDB_ONID = 1
    OLDDB_TSID = 2
    OLDDB_SID = 3
    OLDDB_LCN = 4
    OLDDB_SIGNAL = 5

    DB_SID = 0
    DB_TSID = 1
    DB_ONID = 2
    DB_NAMESPACE = 3
    DB_SIGNAL = 4
    DB_LCN_BROADCAST = 5
    DB_LCN_SCANNED = 6
    DB_LCN_GUI = 7
    DB_PROVIDER = 8  # Max 255 characters.
    DB_PROVIDER_GUI = 9
    DB_SERVICENAME = 10  # Max 255 characters.
    DB_SERVICENAME_GUI = 11

    LCNS_MEDIUM = 0
    LCNS_TRIPLET = 1
    LCNS_SERVICEREFERENCE = 2
    LCNS_SIGNAL = 3
    LCNS_LCN_BROADCAST = 4
    LCNS_LCN_SCANNED = 5
    LCNS_LCN_GUI = 6
    LCNS_PROVIDER = 7
    LCNS_PROVIDER_GUI = 8
    LCNS_SERVICENAME = 9
    LCNS_SERVICENAME_GUI = 10

    SERVICE_PROVIDER = 0
    SERVICE_SERVICEREFERENCE = 1
    SERVICE_NAME = 2

    def __init__(self):
        self.configPath = resolveFilename(SCOPE_CONFIG)
        self.ruleList = {}
        self.rulesDom = fileReadXML(resolveFilename(SCOPE_PLUGIN_ABSOLUTE, "rules.xml"), default="<rulesxml />", source=MODULE_NAME)
        if self.rulesDom is not None:
            rulesIndex = 1
            for rules in self.rulesDom.findall("rules"):
                name = rules.get("name")
                if name:
                    self.ruleList[name] = name
                else:
                    name = "Rules{}".format(rulesIndex)
                    rules.set("name", name)
                    self.ruleList[name] = name
                    rulesIndex += 1

        config.plugins.LCNScanner.rules = ConfigSelection(default="Italy", choices=self.ruleList)
        config.plugins.LCNScanner.useSpacerLines = ConfigYesNo(default=False)
        config.plugins.LCNScanner.addServiceNames = ConfigYesNo(default=False)
        config.plugins.LCNScanner.useDescriptionLines = ConfigYesNo(default=False)

    def lcnScan(self, callback=None):
        def getModes(element):
            mode = element.get("mode", "All")
            match mode:
                case "All" | "Both":
                    modes = ("TV", "Radio")
                case "TV":
                    modes = ("TV",)
                case "Radio":
                    modes = ("Radio",)
                case _:
                    print("[LCNScanner] Error: Invalid mode specified, 'All' assumed!  (Only 'All', 'Both', 'Radio' or 'TV' permitted.)", mode)
                    modes = ("TV", "Radio")
            return modes

        def loadLCNs():
            print("[LCNScanner] Loading 'lcndb' file.")
            lcndb = []
            for lcn in fileReadLines(join(self.configPath, "lcndb"), default=[], source=MODULE_NAME):
                if lcn not in lcndb:
                    lcndb.append(lcn)
                else:
                    print(f"[LCNScanner] Error: Duplicated line detected in lcndb!  ({lcn}).")
            return lcndb

        def loadServices(mode):
            print("[LCNScanner] Loading mode services.", mode)
            services = {}
            serviceHandler = eServiceCenter.getInstance()
            match mode:
                case "TV":
                    # providerQuery = f"{self.MODE_TV} FROM PROVIDERS ORDER BY name"
                    providerQuery = self.MODE_TV + " FROM PROVIDERS ORDER BY name"
                case "Radio":
                    # providerQuery = f"{self.MODE_RADIO} FROM PROVIDERS ORDER BY name"
                    providerQuery = self.MODE_RADIO + " FROM PROVIDERS ORDER BY name"
            providers = serviceHandler.list(eServiceReference(providerQuery))
            if providers:
                for serviceQuery, providerName in providers.getContent("SN", True):
                    serviceList = serviceHandler.list(eServiceReference(serviceQuery))
                    for serviceReference, serviceName in serviceList.getContent("SN", True):
                        services[":".join(serviceReference.split(":")[3:7])] = (providerName, serviceReference, serviceName)
            return services

        def matchLCNsAndServices(mode, lcndb, services, duplicate, renumbers):
            print("[LCNScanner] Matching LCN entries with services mod:", mode)
            lcns = []
            try:
                version = int(lcndb[0][9:]) if lcndb[0].startswith("#VERSION ") else 1
            except Exception:
                version = 1
            match version:
                case 1:
                    for line in lcndb:
                        line = line.strip()
                        if len(line) != 38:
                            continue
                        item = line.split(":")
                        if len(item) != 6:
                            continue
                        match item[self.OLDDB_NAMESPACE][:4].upper():
                            case "DDDD":
                                medium = "A"
                            case "EEEE":
                                medium = "T"
                            case "FFFF":
                                medium = "C"
                            case _:
                                medium = "S"
                        # service = f"{item[self.OLDDB_SID].lstrip("0")}:{item[self.OLDDB_TSID].lstrip("0")}:{item[self.OLDDB_ONID].lstrip("0")}:{item[self.OLDDB_NAMESPACE].lstrip("0")}".upper()
                        service = "{}:{}:{}:{}".format(
                            item[self.OLDDB_SID].lstrip("0"),
                            item[self.OLDDB_TSID].lstrip("0"),
                            item[self.OLDDB_ONID].lstrip("0"),
                            item[self.OLDDB_NAMESPACE].lstrip("0")
                        ).upper()
                        lcns.append([
                            medium,
                            service,
                            services[service][self.SERVICE_SERVICEREFERENCE] if service in services else "",
                            int(item[self.OLDDB_SIGNAL]),
                            int(item[self.OLDDB_LCN]),
                            0,
                            0,
                            services[service][self.SERVICE_PROVIDER] if service in services else "",
                            "",
                            services[service][self.SERVICE_NAME] if service in services else "",
                            ""
                        ])
                case 2:
                    for line in lcndb:
                        if line.startswith("#"):
                            continue
                        item = line.split(":")
                        match item[self.DB_NAMESPACE][:4]:
                            case "DDDD":
                                medium = "A"
                            case "EEEE":
                                medium = "T"
                            case "FFFF":
                                medium = "C"
                            case _:
                                medium = "S"
                        # service = f"{item[self.DB_SID]}:{item[self.DB_TSID]}:{item[self.DB_ONID]}:{item[self.DB_NAMESPACE]}"
                        service = "{}:{}:{}:{}".format(
                            item[self.DB_SID],
                            item[self.DB_TSID],
                            item[self.DB_ONID],
                            item[self.DB_NAMESPACE]
                        )
                        lcns.append([
                            medium,
                            service,
                            services[service][self.SERVICE_SERVICEREFERENCE] if service in services else "",
                            int(item[self.DB_SIGNAL]),
                            int(item[self.DB_LCN_BROADCAST]),
                            int(item[self.DB_LCN_SCANNED]),
                            int(item[self.DB_LCN_GUI]),
                            services[service][self.SERVICE_PROVIDER] if service in services else "",
                            item[self.DB_PROVIDER_GUI],
                            services[service][self.SERVICE_NAME] if service in services else "",
                            item[self.DB_SERVICENAME_GUI]
                        ])
                case _:
                    print("[LCNScanner] Error: LCN db file format unrecognized!")
            scannerLCN = duplicate[mode][0]
            scannerLast = duplicate[mode][1]
            cableCache = {}  # Cache to check for unique cable LCNs.
            satelliteCache = {}  # Cache to check for unique satellite LCNs.
            terrestrialCache = {}  # Cache to check for unique terrestrial LCNs.
            cableLCNs = {}  # Dictionary for available and unique cable LCNs.
            satelliteLCNs = {}  # Dictionary for available and unique satellite LCNs.
            terrestrialLCNs = {}  # Dictionary for available and unique terrestrial LCNs.
            for data in lcns:
                service = data[self.LCNS_TRIPLET]
                serviceReference = data[self.LCNS_SERVICEREFERENCE].split(":")
                lcn = data[self.LCNS_LCN_BROADCAST]
                match data[self.LCNS_MEDIUM]:
                    case "C":
                        lcnCache = cableCache
                        serviceLCNs = cableLCNs
                    case "S":
                        lcnCache = satelliteCache
                        serviceLCNs = satelliteLCNs
                    case "A" | "T":
                        lcnCache = terrestrialCache
                        serviceLCNs = terrestrialLCNs
                if service in services:  # Check if the service represented by this LCN entry is still a valid service.
                    if lcn in lcnCache:  # Check if the LCN already exists.
                        if data[self.LCNS_TRIPLET] == lcnCache[lcn][self.LCNS_TRIPLET] and data[self.LCNS_SIGNAL] > lcnCache[lcn][self.LCNS_SIGNAL]:
                            data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                            lcnCache[lcn] = data  # Replace the existing weaker signal with the stronger one.
                        elif scannerLCN > scannerLast:  # Check if there is no more space for duplicates.
                            # print(f"[LCNScanner] Warning: Duplicate LCN {lcn} found for servine '{data[self.LCNS_SERVICEREFERENCE]}' but duplicate LCN range exhausted!")
                            print("[LCNScanner] Warning: Duplicate LCN  found for servine data[self.LCNS_SERVICEREFERENCE] but duplicate LCN range exhausted!")
                        else:  # Allocate a new LCN from the duplicate pool.
                            # print(f"[LCNScanner] Duplicate LCN found, renumbering {lcn} to {scannerLCN}.")
                            print("[LCNScanner] Duplicate LCN found, renumbering lcn to scannerLCN.")
                            lcn = scannerLCN
                            data[self.LCNS_LCN_SCANNED] = lcn
                            lcnCache[lcn] = data
                            scannerLCN += 1
                    else:
                        data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                        lcnCache[lcn] = data
                elif len(serviceReference) > 2 and serviceReference[2] in self.MODES[mode]:  # Skip all LCN entries of the same type that are not a valid service.
                    # print(f"[LCNScanner] Service '{service}' with LCN {lcn} not a valid {mode} service!")
                    print("[LCNScanner] Service with LCN not a valid mode service!")
                    continue
                else:
                    continue
                for renumber in renumbers[mode]:  # Process the LCN renumbering rules.
                    if renumber[0][0] <= lcn <= renumber[0][1]:
                        try:
                            # startingLCN = lcn
                            lcn = int(eval(renumber[1].replace("LCN", str(lcn))))
                            # print(f"[LCNScanner] LCN {startingLCN} is renumbered to {lcn} via rule range {renumber[0][0]}-{renumber[0][1]} and formula='{renumber[1]}'.")
                            if lcn in lcnCache:
                                # print(f"[LCNScanner] Renumbered LCN {startingLCN} is now a duplicated LCN {lcn}, renumbering {startingLCN} to {scannerLCN}.")
                                data[self.LCNS_LCN_SCANNED] = scannerLCN
                                scannerLCN += 1
                            else:
                                data[self.LCNS_LCN_SCANNED] = lcn
                        except ValueError as err:
                            # print(f"[LCNScanner] Error: LCN renumber formula '{renumber[1]}' is invalid!  ({err})")
                            print("[LCNScanner] Error: LCN renumber formula is invalid!",  err)
                serviceLCNs[lcn] = tuple(data)

            return (cableLCNs, satelliteLCNs, terrestrialLCNs)

        def writeBouquet(mode, medium, serviceLCNs, markers):
            def insertMarker(mode, lcn):
                if lcn in markers[mode]:
                    # bouquet.append(f"#SERVICE 1:64:0:0:0:0:0:0:0:0::{markers[mode][lcn]}")
                    bouquet.append("#SERVICE 1:64:0:0:0:0:0:0:0:0::{}".format(markers[mode][lcn]))
                    if useDescriptionLines:
                        # bouquet.append(f"#DESCRIPTION {markers[mode][lcn]}")
                        bouquet.append("#DESCRIPTION {}".format(markers[mode][lcn]))
                return bouquet

            useDescriptionLines = config.plugins.LCNScanner.useDescriptionLines.value if config.plugins.LCNScanner.addServiceNames.value else False
            bouquet = []
            bouquet.append("#NAME {} {} LCN".format(medium, mode))
            bouquet.append("#SERVICE 1:64:0:0:0:0:0:0:0:0::{} {} LCN".format(medium, mode))
            # bouquet.append(f"#NAME {medium} {mode} LCN")
            # bouquet.append(f"#SERVICE 1:64:0:0:0:0:0:0:0:0::{medium} {mode} LCN")
            if useDescriptionLines:
                # bouquet.append(f"#DESCRIPTION {medium} {mode} LCN")
                bouquet.append("#DESCRIPTION {} {} LCN".format(medium, mode))
            index = 0
            useSpacerLines = config.plugins.LCNScanner.useSpacerLines.value
            for lcn in sorted(serviceLCNs.keys()):
                index += 1
                while lcn > index:
                    bouquet = insertMarker(mode, index)
                    if useSpacerLines:
                        bouquet.append("#SERVICE 1:832:D:0:0:0:0:0:0:0:")
                    index += 1
                bouquet = insertMarker(mode, index)
                name = serviceLCNs[lcn][self.LCNS_SERVICENAME]
                # serviceName = f":{name}" if config.plugins.LCNScanner.addServiceNames.value else ""
                serviceName = ":{}".format(name) if config.plugins.LCNScanner.addServiceNames.value else ""
                # bouquet.append(f"#SERVICE {serviceLCNs[lcn][self.LCNS_SERVICEREFERENCE]}{serviceName}")
                bouquet.append("#SERVICE {}{}".format(serviceLCNs[lcn][self.LCNS_SERVICEREFERENCE], serviceName))
                if useDescriptionLines:
                    bouquet.append("#DESCRIPTION {}".format(name))
            extension = mode.lower()
            # bouquetName = f"userbouquet.{medium.lower()}_lcn.{extension}"
            bouquetName = "userbouquet.{}_lcn.{}".format(medium.lower(), extension)
            bouquetsPath = join(self.configPath, bouquetName)
            if fileWriteLines(bouquetsPath, bouquet, source=MODULE_NAME):
                # print(f"[LCNScanner] Bouquet '{bouquetsPath}' saved.")
                print("[LCNScanner] Bouquet saved.")
            else:
                # print(f"[LCNScanner] Error: Bouquet '{bouquetsPath}' could not be saved!")
                print("[LCNScanner] Error: Bouquet could not be saved!")
            bouquetsPath = join(self.configPath, f"bouquets.{extension}")
            bouquets = fileReadLines(bouquetsPath, default=[], source=MODULE_NAME)
            for bouquet in bouquets:
                if bouquet.find(bouquetName) != -1:
                    print("[LCNScanner] Bouquet is already in bouquetsPath.")
                    break
            else:
                bouquets.append(f"#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET \"{bouquetName}\" ORDER BY bouquet")
                if fileWriteLines(bouquetsPath, bouquets, source=MODULE_NAME):
                    print("[LCNScanner] Bouquet added to bouquetsPath.")
                else:
                    print("[LCNScanner] Error: Bouquet bouquetName could not be added to bouquetsPath!")

        def buildLCNs(serviceLCNs):
            lcndb = []
            for lcn in sorted(serviceLCNs.keys()):
                data = []
                for field in (self.LCNS_TRIPLET, self.LCNS_SIGNAL, self.LCNS_LCN_BROADCAST, self.LCNS_LCN_SCANNED, self.LCNS_LCN_GUI):
                    data.append(str(serviceLCNs[lcn][field]))
                data.extend(["", "", "", ""])  # This keeps the record length as defined while all the fields are not available.
                lcndb.append(":".join(data))
            return lcndb

        print("[LCNScanner] LCN scan started.")
        duplicate = {
            "TV": [99000, maxsize],
            "Radio": [99000, maxsize]
        }
        renumbers = {
            "TV": [],
            "Radio": []
        }
        markers = {
            "TV": {},
            "Radio": {}
        }
        rules = config.plugins.LCNScanner.rules.value if config.plugins.LCNScanner.rules.value else 'Default'  # in self.ruleList.keys() else self.ruleList[0][0]
        # dom = self.rulesDom.findall(f".//rules[@name='{rules}']/rule[@type='duplicate']")
        dom = self.rulesDom.findall(".//rules[@name='{}']/rule[@type='duplicate']".format(rules))
        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcnRange = element.get("range", "99000-99999")
                    rangeMsg = "starting with 99000"
                    markerMsg = ""
                    try:
                        duplicate[mode] = [int(x) for x in lcnRange.split("-", 1)]
                        if len(duplicate[mode]) == 1:
                            duplicate[mode].append(maxsize)
                            rangeMsg = "starting with {}".format(duplicate[mode][0])
                        else:
                            rangeMsg = "within the range {} to {}".format(duplicate[mode][0], duplicate[mode][1])
                        marker = element.text
                        if marker:
                            markers[mode][duplicate[mode][0]] = marker
                            markerMsg = " with a preceding marker of '{}'".format(marker)
                    except ValueError as err:
                        print("[LCNScanner] Error: Duplicate range '{}' is invalid! ({})".format(lcnRange, err))
                    print("[LCNScanner] Duplicated LCNs for {} will be allocated new numbers {}{}.".format(mode, rangeMsg, markerMsg))
        dom = self.rulesDom.findall(f".//rules[@name='{rules}']/rule[@type='renumber']")
        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcnRange = element.get("range")
                    try:
                        lcnRange = [int(x) for x in lcnRange.split("-", 1)]
                        if len(lcnRange) != 2:
                            raise ValueError("Range format is a pair of numbers separated by a hyphen: <LOWER_LIMIT>-<HIGHER_LIMIT>")
                        renumbers[mode].append((lcnRange, element.text))
                        print("[LCNScanner] LCNs for {} in the range {} to {} will be renumbered with the formula '{}'.".format(mode, lcnRange[0], lcnRange[1], element.text))
                        # print(f"[LCNScanner] LCNs for {mode} in the range {lcnRange[0]} to {lcnRange[1]} will be renumbered with the formula '{element.text}'.")
                    except ValueError as err:
                        print("[LCNScanner] Error: Renumber range '{}' is invalid! ({})".format(lcnRange, err))
        dom = self.rulesDom.findall(f".//rules[@name='{rules}']/rule[@type='marker']")
        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcn = element.get("position")
                    if lcn:
                        try:
                            lcn = int(lcn)
                            markers[mode][lcn] = element.text
                            print("[LCNScanner] Marker '{}' will be added before {} LCN {}.".format(element.text, mode, lcn))
                        except ValueError as err:
                            print("[LCNScanner] Error: Invalid marker LCN '{}' specified!  ({})".format(lcn, err))
        # The actual scanning process starts here.
        lcndb = loadLCNs()
        lcns = []
        for mode in ("TV", "Radio"):
            services = loadServices(mode)
            cableLCNs, satelliteLCNs, terrestrialLCNs = matchLCNsAndServices(mode, lcndb, services, duplicate, renumbers)
            if cableLCNs or satelliteLCNs or terrestrialLCNs:
                if cableLCNs:
                    writeBouquet(mode, "Cable", cableLCNs, markers)
                    lcns += buildLCNs(cableLCNs)
                if satelliteLCNs:
                    writeBouquet(mode, "Satellite", satelliteLCNs, markers)
                    lcns += buildLCNs(satelliteLCNs)
                if terrestrialLCNs:
                    writeBouquet(mode, "Terrestrial", terrestrialLCNs, markers)
                    lcns += buildLCNs(terrestrialLCNs)
            else:
                print("[LCNScanner] Error: No valid entries found in the LCN database! Run a service scan.")
        if lcns:
            lcns.insert(0, "#VERSION 2")
            if fileWriteLines(join(self.configPath, "lcndb"), lcns, source=MODULE_NAME):
                print("[LCNScanner] The 'lcndb' file has been updated.")
            else:
                print("[LCNScanner] Error: The 'lcndb' file could not be updated!")
            eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
        print("[LCNScanner] LCN scan finished.")



def ReloadBouquets(x):
    print('\n----Reloading bouquets----\n')
    try:
        from enigma import eDVBDB
    except ImportError:
        eDVBDB = None
    print("\n----Reloading bouquets----")

    global setx  # for linuxsat panel
    if x == 1:
        setx = 0
        print("\n----Reloading Terrestrial----")
        # terrestrial_rest()

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