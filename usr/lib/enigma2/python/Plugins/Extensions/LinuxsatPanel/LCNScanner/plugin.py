#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on a plugin from Sif Team.
# This version created by IanSav and the OpenATV team.

from Components.PluginComponent import plugins
from Components.config import ConfigSelection, ConfigSubsection, ConfigYesNo, config
from Tools.Directories import SCOPE_CONFIG, SCOPE_PLUGIN_ABSOLUTE, fileReadLines, fileReadXML, fileWriteLines, resolveFilename
from enigma import eDVBDB, eServiceCenter, eServiceReference
from os.path import join
from sys import maxsize

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

        config.plugins.LCNScanner.rules = ConfigSelection(default="Default", choices=self.ruleList)
        config.plugins.LCNScanner.useSpacerLines = ConfigYesNo(default=False)
        config.plugins.LCNScanner.addServiceNames = ConfigYesNo(default=False)
        config.plugins.LCNScanner.useDescriptionLines = ConfigYesNo(default=False)

    def lcnScan(self, callback=None):
        def getModes(element):
            mode = element.get("mode", "All")
            if mode in ("All", "Both"):
                modes = ("TV", "Radio")
            elif mode == "TV":
                modes = ("TV",)
            elif mode == "Radio":
                modes = ("Radio",)
            else:
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
                    print("[LCNScanner] Error: Duplicated line detected in lcndb!", lcn)
            return lcndb

        def loadServices(mode):
            print("[LCNScanner] Loading mode services.", mode)
            services = {}
            serviceHandler = eServiceCenter.getInstance()

            if mode == "TV":
                # providerQuery = f"{self.MODE_TV} FROM PROVIDERS ORDER BY name"
                providerQuery = self.MODE_TV + " FROM PROVIDERS ORDER BY name"
            elif mode == "Radio":
                # providerQuery = f"{self.MODE_RADIO} FROM PROVIDERS ORDER BY name"
                providerQuery = self.MODE_RADIO + " FROM PROVIDERS ORDER BY name"
            else:
                print("[LCNScanner] Error: Invalid mode specified. Please use 'TV' or 'Radio'.")
                return services  # Restituisci un dizionario vuoto se il mode non è valido

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
            if version == 1:
                for line in lcndb:
                    line = line.strip()
                    if len(line) != 38:
                        continue
                    item = line.split(":")
                    if len(item) != 6:
                        continue
                    if item[self.OLDDB_NAMESPACE][:4].upper() == "DDDD":
                        medium = "A"
                    elif item[self.OLDDB_NAMESPACE][:4].upper() == "EEEE":
                        medium = "T"
                    elif item[self.OLDDB_NAMESPACE][:4].upper() == "FFFF":
                        medium = "C"
                    else:
                        medium = "S"

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
            elif version == 2:
                for line in lcndb:
                    if line.startswith("#"):
                        continue
                    item = line.split(":")
                    if item[self.DB_NAMESPACE][:4] == "DDDD":
                        medium = "A"
                    elif item[self.DB_NAMESPACE][:4] == "EEEE":
                        medium = "T"
                    elif item[self.DB_NAMESPACE][:4] == "FFFF":
                        medium = "C"
                    else:
                        medium = "S"

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
            else:
                print("[LCNScanner] Error: LCN db file format unrecognized!")

            scannerLCN = duplicate[mode][0]
            scannerLast = duplicate[mode][1]
            cableCache = {}
            satelliteCache = {}
            terrestrialCache = {}
            cableLCNs = {}
            satelliteLCNs = {}
            terrestrialLCNs = {}

            for data in lcns:
                service = data[self.LCNS_TRIPLET]
                serviceReference = data[self.LCNS_SERVICEREFERENCE].split(":")
                lcn = data[self.LCNS_LCN_BROADCAST]

                if data[self.LCNS_MEDIUM] == "C":
                    lcnCache = cableCache
                    serviceLCNs = cableLCNs
                elif data[self.LCNS_MEDIUM] == "S":
                    lcnCache = satelliteCache
                    serviceLCNs = satelliteLCNs
                elif data[self.LCNS_MEDIUM] in ("A", "T"):
                    lcnCache = terrestrialCache
                    serviceLCNs = terrestrialLCNs

                if service in services:
                    if lcn in lcnCache:
                        if (data[self.LCNS_TRIPLET] == lcnCache[lcn][self.LCNS_TRIPLET] and
                                data[self.LCNS_SIGNAL] > lcnCache[lcn][self.LCNS_SIGNAL]):
                            data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                            lcnCache[lcn] = data
                        elif scannerLCN > scannerLast:
                            print("[LCNScanner] Warning: Duplicate LCN found for service data[LCNS_SERVICEREFERENCE] but duplicate LCN range exhausted!")
                        else:
                            print("[LCNScanner] Duplicate LCN found, renumbering lcn to scannerLCN.")
                            lcn = scannerLCN
                            data[self.LCNS_LCN_SCANNED] = lcn
                            lcnCache[lcn] = data
                            scannerLCN += 1
                    else:
                        data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                        lcnCache[lcn] = data
                elif (len(serviceReference) > 2 and
                      serviceReference[2] in self.MODES[mode]):
                    print("[LCNScanner] Service with LCN not a valid mode service!")
                    continue
                else:
                    continue

                for renumber in renumbers[mode]:
                    if renumber[0][0] <= lcn <= renumber[0][1]:
                        try:
                            lcn = int(eval(renumber[1].replace("LCN", str(lcn))))
                            if lcn in lcnCache:
                                data[self.LCNS_LCN_SCANNED] = scannerLCN
                                scannerLCN += 1
                            else:
                                data[self.LCNS_LCN_SCANNED] = lcn
                        except ValueError as err:
                            print("[LCNScanner] Error: LCN renumber formula is invalid!", err)

                serviceLCNs[lcn] = tuple(data)

            return (cableLCNs, satelliteLCNs, terrestrialLCNs)

        def writeBouquet(mode, medium, serviceLCNs, markers):
            def insertMarker(mode, lcn):
                if lcn in markers[mode]:
                    bouquet.append("#SERVICE 1:64:0:0:0:0:0:0:0:0::{}".format(markers[mode][lcn]))
                    if useDescriptionLines:
                        bouquet.append("#DESCRIPTION {}".format(markers[mode][lcn]))
                return bouquet

            useDescriptionLines = config.plugins.LCNScanner.useDescriptionLines.value if config.plugins.LCNScanner.addServiceNames.value else False
            bouquet = []
            bouquet.append("#NAME {} {} LCN".format(medium, mode))
            bouquet.append("#SERVICE 1:64:0:0:0:0:0:0:0:0::{} {} LCN".format(medium, mode))
            if useDescriptionLines:
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
                bouquet.append("#SERVICE {}{}".format(serviceLCNs[lcn][self.LCNS_SERVICEREFERENCE], serviceName))
                if useDescriptionLines:
                    bouquet.append("#DESCRIPTION {}".format(name))
            extension = mode.lower()
            bouquetName = "userbouquet.{}_lcn.{}".format(medium.lower(), extension)
            bouquetsPath = join(self.configPath, bouquetName)
            if fileWriteLines(bouquetsPath, bouquet, source=MODULE_NAME):
                print("[LCNScanner] Bouquet saved.")
            else:
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
