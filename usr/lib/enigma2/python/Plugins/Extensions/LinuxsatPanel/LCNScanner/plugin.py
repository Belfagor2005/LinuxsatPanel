#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on a plugin from Sif Team.
# This version created by IanSav and the OpenATV team.
# mod from Lululla 20230512
# from Components.PluginComponent import plugins
from Components.config import ConfigSelection, ConfigSubsection, ConfigYesNo, config
from Tools.Directories import SCOPE_CONFIG, SCOPE_PLUGINS, resolveFilename
from enigma import eDVBDB, eServiceCenter, eServiceReference
from os.path import join
from sys import maxsize
from xml.etree.ElementTree import Element, ParseError, fromstring, parse
from errno import ENOENT

DEFAULT_MODULE_NAME = MODULE_NAME = __name__.split(".")[-1]
plugin_path = resolveFilename(SCOPE_PLUGINS,
                              "Extensions/{}".format('LinuxsatPanel'))
config.plugins.LCNScanner = ConfigSubsection()
config.plugins.LCNScanner.showInPluginsList = ConfigYesNo(default=False)


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
        self.rulesDom = fileReadXML(
            resolveFilename(
                SCOPE_PLUGINS,
                "Extensions/LinuxsatPanel/LCNScanner/rules.xml"),
            default="<rulesxml />",
            source=MODULE_NAME)
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

        config.plugins.LCNScanner.rules = ConfigSelection(
            default="Default", choices=self.ruleList)
        config.plugins.LCNScanner.useSpacerLines = ConfigYesNo(default=False)
        config.plugins.LCNScanner.addServiceNames = ConfigYesNo(default=False)
        config.plugins.LCNScanner.useDescriptionLines = ConfigYesNo(
            default=False)

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
                print(
                    "[LCNScanner] Error: Invalid mode '{}' specified, 'All' assumed!  (Only 'All', 'Both', 'Radio' or 'TV' permitted.)".format(mode))
                modes = ("TV", "Radio")
            return modes

        def loadLCNs():
            print("[LCNScanner] Loading 'lcndb' file.")
            lcndb = []
            for lcn in fileReadLines(
                    join(
                        self.configPath,
                        "lcndb"),
                    default=[],
                    source=MODULE_NAME):
                if lcn not in lcndb:
                    lcndb.append(lcn)
                else:
                    print(
                        "[LCNScanner] Error: Duplicated line detected in lcndb!  ({}).".format(lcn))
            return lcndb

        def loadServices(mode):
            print("[LCNScanner] Loading {} services.".format(mode))
            services = {}
            serviceHandler = eServiceCenter.getInstance()
            # Sostituzione del match-case con if-elif
            if mode == "TV":
                providerQuery = "{} FROM PROVIDERS ORDER BY name".format(
                    self.MODE_TV)
            elif mode == "Radio":
                providerQuery = "{} FROM PROVIDERS ORDER BY name".format(
                    self.MODE_RADIO)
            else:
                print("[LCNScanner] Error: Unsupported mode '{}'!".format(mode))
                return services

            providers = serviceHandler.list(eServiceReference(providerQuery))
            if providers:
                for serviceQuery, providerName in providers.getContent(
                        "SN", True):
                    serviceList = serviceHandler.list(
                        eServiceReference(serviceQuery))
                    for serviceReference, serviceName in serviceList.getContent(
                            "SN", True):
                        services[":".join(serviceReference.split(":")[3:7])] = (
                            providerName, serviceReference, serviceName)
            return services

        def matchLCNsAndServices(mode, lcndb, services, duplicate, renumbers):
            print(
                "[LCNScanner] Matching LCN entries with {} services.".format(mode))
            lcns = []
            try:
                version = int(lcndb[0][9:]) if lcndb[0].startswith(
                    "#VERSION ") else 1
            except Exception:
                version = 1

            # Sostituzione di match-case per la versione
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
                return None

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
                        if data[self.LCNS_TRIPLET] == lcnCache[lcn][self.LCNS_TRIPLET] and data[self.LCNS_SIGNAL] > lcnCache[lcn][self.LCNS_SIGNAL]:
                            data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                            lcnCache[lcn] = data
                        elif scannerLCN > scannerLast:
                            print("[LCNScanner] Warning: Duplicate LCN {} found for service '{}' but duplicate LCN range exhausted!".format(
                                lcn, data[self.LCNS_SERVICEREFERENCE]))
                        else:
                            print(
                                "[LCNScanner] Duplicate LCN found, renumbering {} to {}.".format(
                                    lcn, scannerLCN))
                            lcn = scannerLCN
                            data[self.LCNS_LCN_SCANNED] = lcn
                            lcnCache[lcn] = data
                            scannerLCN += 1
                    else:
                        data[self.LCNS_LCN_SCANNED] = data[self.LCNS_LCN_BROADCAST]
                        lcnCache[lcn] = data
                elif len(serviceReference) > 2 and serviceReference[2] in self.MODES[mode]:
                    print(
                        "[LCNScanner] Service '{}' with LCN {} not a valid {} service!".format(
                            service, lcn, mode))
                    continue
                else:
                    continue

                for renumber in renumbers[mode]:
                    if renumber[0][0] <= lcn <= renumber[0][1]:
                        try:
                            startingLCN = lcn
                            lcn = int(
                                eval(
                                    renumber[1].replace(
                                        "LCN",
                                        str(lcn))))
                            print(
                                "[LCNScanner] LCN {} is renumbered to {} via rule range {} and formula='{}'.".format(
                                    startingLCN, lcn, renumber[0][0] - renumber[0][1], renumber[1]))
                            if lcn in lcnCache:
                                print(
                                    "[LCNScanner] Renumbered LCN {} is now a duplicated LCN {}, renumbering {} to {}.".format(
                                        startingLCN, lcn, startingLCN, scannerLCN))
                                data[self.LCNS_LCN_SCANNED] = scannerLCN
                                scannerLCN += 1
                            else:
                                data[self.LCNS_LCN_SCANNED] = lcn
                        except ValueError as err:
                            print(
                                "[LCNScanner] Error: LCN renumber formula '{}' is invalid!  ({})".format(
                                    renumber[1], err))

                serviceLCNs[lcn] = tuple(data)

            return (cableLCNs, satelliteLCNs, terrestrialLCNs)

        def writeBouquet(mode, medium, serviceLCNs, markers):
            def insertMarker(mode, lcn):
                if lcn in markers[mode]:
                    bouquet.append(
                        "#SERVICE 1:64:0:0:0:0:0:0:0:0::{}".format(
                            markers[mode][lcn]))
                    if useDescriptionLines:
                        bouquet.append(
                            "#DESCRIPTION {}".format(
                                markers[mode][lcn]))
                return bouquet

            useDescriptionLines = config.plugins.LCNScanner.useDescriptionLines.value if config.plugins.LCNScanner.addServiceNames.value else False
            bouquet = []
            bouquet.append("#NAME {} {} LCN".format(medium, mode))
            bouquet.append(
                "#SERVICE 1:64:0:0:0:0:0:0:0:0::{} {} LCN".format(
                    medium, mode))
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
                serviceName = ":{}".format(
                    name) if config.plugins.LCNScanner.addServiceNames.value else ""
                bouquet.append("#SERVICE {}{}".format(
                    serviceLCNs[lcn][self.LCNS_SERVICEREFERENCE], serviceName))
                if useDescriptionLines:
                    bouquet.append("#DESCRIPTION {}".format(name))
            # Save bouquet and, if required, add this bouquet to the list of
            # bouquets.
            extension = mode.lower()
            # This code is not currently needed but is being kept in case needs change.
            # bouquetName = getattr(config.plugins.LCNScanner, f"{medium.lower()}Bouquet{mode}", f"userbouquet.{medium.lower()}_lcn.{mode}").value
            bouquetName = "userbouquet.{}_lcn.{}".format(
                medium.lower(), extension)
            bouquetsPath = join(self.configPath, bouquetName)
            if fileWriteLines(bouquetsPath, bouquet, source=MODULE_NAME):
                print("[LCNScanner] Bouquet '{}' saved.".format(bouquetsPath))
            else:
                print(
                    "[LCNScanner] Error: Bouquet {} could not be saved!".format(bouquetsPath))
            bouquetsPath = join(
                self.configPath,
                "bouquets.{}".format(extension))
            bouquets = fileReadLines(
                bouquetsPath, default=[], source=MODULE_NAME)
            for bouquet in bouquets:
                if bouquet.find(bouquetName) != -1:
                    print(
                        "[LCNScanner] Bouquet '{}' is already in '{}'.".format(
                            bouquetName, bouquetsPath))
                    break
            else:
                bouquets.append(
                    "#SERVICE 1:7:2:0:0:0:0:0:0:0:FROM BOUQUET \"{}\" ORDER BY bouquet".format(bouquetName))
                if fileWriteLines(bouquetsPath, bouquets, source=MODULE_NAME):
                    print(
                        "[LCNScanner] Bouquet '{}' added to '{}'.".format(
                            bouquetName, bouquetsPath))
                else:
                    print(
                        "[LCNScanner] Error: Bouquet '{}' could not be added to '{}'!".format(
                            bouquetName, bouquetsPath))

        def buildLCNs(serviceLCNs):
            lcndb = []
            for lcn in sorted(serviceLCNs.keys()):
                data = []
                for field in (
                        self.LCNS_TRIPLET,
                        self.LCNS_SIGNAL,
                        self.LCNS_LCN_BROADCAST,
                        self.LCNS_LCN_SCANNED,
                        self.LCNS_LCN_GUI):
                    data.append(str(serviceLCNs[lcn][field]))
                # This keeps the record length as defined while all the fields
                # are not available.
                data.extend(["", "", "", ""])
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
        # in self.ruleList.keys() else self.ruleList[0][0]
        rules = config.plugins.LCNScanner.rules.value if config.plugins.LCNScanner.rules.value else 'Default'
        dom = self.rulesDom.findall(
            ".//rules[@name='{}']/rule[@type='duplicate']".format(rules))
        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcnRange = element.get("range", "99000-99999")
                    rangeMsg = "starting with 99000"
                    markerMsg = ""
                    try:
                        duplicate[mode] = [int(x)
                                           for x in lcnRange.split("-", 1)]
                        if len(duplicate[mode]) == 1:
                            duplicate[mode].append(maxsize)
                            rangeMsg = "starting with {}".format(
                                duplicate[mode][0])
                        else:
                            rangeMsg = "within the range {} to {}".format(
                                duplicate[mode][0], duplicate[mode][1])
                        marker = element.text
                        if marker:
                            markers[mode][duplicate[mode][0]] = marker
                            markerMsg = " with a preceding marker of '{}'".format(
                                marker)
                    except ValueError as err:
                        print(
                            "[LCNScanner] Error: Duplicate range '{}' is invalid!  ({})".format(
                                lcnRange, err))
                    print(
                        "[LCNScanner] Duplicated LCNs for {} will be allocated new numbers {}{}.".format(
                            mode, rangeMsg, markerMsg))
        dom = self.rulesDom.findall(
            ".//rules[@name='{}']/rule[@type='renumber']".format(rules))

        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcnRange = element.get("range")
                    try:
                        lcnRange = [int(x) for x in lcnRange.split("-", 1)]
                        if len(lcnRange) != 2:
                            raise ValueError(
                                "Range format is a pair of numbers separated by a hyphen: <LOWER_LIMIT>-<HIGHER_LIMIT>")
                        renumbers[mode].append((lcnRange, element.text))
                        print(
                            "[LCNScanner] LCNs for {} in the range {} to {} will be renumbered with the formula '{}'.".format(
                                mode, lcnRange[0], lcnRange[1], element.text))
                    except ValueError as err:
                        print(
                            "[LCNScanner] Error: Renumber range '{}' is invalid!  ({})".format(
                                lcnRange, err))
        dom = self.rulesDom.findall(
            ".//rules[@name='{}']/rule[@type='marker']".format(rules))
        if dom is not None:
            for element in dom:
                modes = getModes(element)
                for mode in modes:
                    lcn = element.get("position")
                    if lcn:
                        try:
                            lcn = int(lcn)
                            markers[mode][lcn] = element.text
                            print(
                                "[LCNScanner] Marker '{}' will be added before {} LCN {}.".format(
                                    element.text, mode, lcn))
                        except ValueError as err:
                            print(
                                "[LCNScanner] Error: Invalid marker LCN '{}' specified!  ({})".format(
                                    lcn, err))
        # The actual scanning process starts here.
        lcndb = loadLCNs()
        lcns = []
        for mode in ("TV", "Radio"):
            services = loadServices(mode)
            cableLCNs, satelliteLCNs, terrestrialLCNs = matchLCNsAndServices(
                mode, lcndb, services, duplicate, renumbers)
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
                print(
                    "[LCNScanner] Error: No valid entries found in the LCN database! Run a service scan.")
        if lcns:
            lcns.insert(0, "#VERSION 2")
            if fileWriteLines(
                    join(
                        self.configPath,
                        "lcndb"),
                    lcns,
                    source=MODULE_NAME):
                print("[LCNScanner] The 'lcndb' file has been updated.")
            else:
                print("[LCNScanner] Error: The 'lcndb' file could not be updated!")
            eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
        print("[LCNScanner] LCN scan finished.")


def fileReadLines(
        filename,
        default=None,
        source=DEFAULT_MODULE_NAME,
        debug=False):
    lines = None
    try:
        with open(filename) as fd:
            lines = fd.read().splitlines()
    except OSError as err:
        if err.errno != ENOENT:  # ENOENT - No such file or directory.
            print("[" +
                  source +
                  "] Error " +
                  str(err.errno) +
                  ": Unable to read lines from file '" +
                  filename +
                  "'!  (" +
                  err.strerror +
                  ")")
        lines = default
    return lines


def fileWriteLines(filename, lines, source=DEFAULT_MODULE_NAME, debug=False):
    try:
        with open(filename, "w") as fd:
            if isinstance(lines, list):
                lines.append("")
                lines = "\n".join(lines)
            fd.write(lines)
        result = 1
    except OSError as err:
        print("[" +
              source +
              "] Error " +
              str(err.errno) +
              ": Unable to write " +
              str(len(lines)) +
              " lines to file '" +
              filename +
              "'! " +
              err.strerror)
        result = 0
    return result


def fileReadXML(
        filename,
        default=None,
        source=DEFAULT_MODULE_NAME,
        debug=False):
    dom = None
    try:
        # This open gets around a possible file handle leak in Python's XML
        # parser.
        with open(filename) as fd:
            try:
                dom = parse(fd).getroot()
                print("Read")
            except ParseError as err:
                fd.seek(0)
                content = fd.readlines()
                line, column = err.position
                print("[" + source + "] XML Parse Error: '" +
                      str(err) + "' in '" + filename + "'!")
                data = content[line - 1].replace("\t", " ").rstrip()
                print("[" + source + "] XML Parse Error: '" + str(data) + "'")
                print("[" + source + "] XML Parse Error: '" + '-' *
                      column + "^" + ' ' * (len(data) - column - 1) + "'")
            except Exception as err:
                print(
                    "[" +
                    source +
                    "] Error: Unable to parse data in '" +
                    filename +
                    "' - '" +
                    str(err) +
                    "'!")
    except OSError as err:
        if err.errno == ENOENT:  # ENOENT - No such file or directory.
            print("[" + source + "] Warning: File '" +
                  filename + "' does not exist!")
        else:
            print("[%s] Error %d: Opening file '%s'!  (%s)" %
                  (source, err.errno, filename, err.strerror))
    except Exception as err:
        print(
            "[" +
            source +
            "] Error: Unexpected error opening/parsing file '" +
            filename +
            "'!  (" +
            str(err) +
            ")")
    if dom is None:
        if default and isinstance(default, str):
            dom = fromstring(default)
            print("Default (XML)")
        elif default and isinstance(default, Element):
            dom = default
            print("Default (DOM)")
        else:
            print("Failed to read")
    return dom
