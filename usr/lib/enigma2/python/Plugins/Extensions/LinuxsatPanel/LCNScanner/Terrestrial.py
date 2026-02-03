#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from .. import _
from enigma import eDVBDB
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigSelection
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
# from Screens.ChannelSelection import MODE_TV, MODE_RADIO
from Screens.Setup import Setup
from Tools.BoundFunction import boundFunction
from ServiceReference import ServiceReference
try:
    from Screens.ChannelSelection import MODE_TV, MODE_RADIO
except ImportError:
    MODE_TV = "1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)"
    MODE_RADIO = "1:7:2:0:0:0:0:0:0:0:(type == 2) || (type == 10)"


# MODES = {
    # "TV": (1, 17, 22, 25, 134, 195),
    # "Radio": (2, 10)
# }


providers = {
    "other": {},
    "it": {
        "name": _("Italy"),
        "sections": {
            1: _("Entertainment"),
            10: _("Local Broadcasters"),
            20: _("Semi-Generalists"),
            40: _("Local Broadcasters"),
            48: _("Information and Culture"),
            58: _("Sports"),
            66: _("Music"),
            71: _("Regional Broadcasters"),
            101: _("Test Channels"),
            204: _("Promo H264"),
            230: _("Regional Broadcasters"),
            409: _("Premium"),
            417: _("Europe7"),
            455: _("Sky Channels"),
            500: _("SD Provisionals"),
            504: _("HD Channels"),
            601: _("Regional Broadcasters"),
            710: _("Regional Radio"),
            801: _("Duplicates"),
            1000: _("LCN Duplicates"),

        }},
    "uk": {
        "name": _("UK"),
        "bouquetname": "FreeView",
        "sections": {
            1: _("Entertainment"),
            100: _("High Definition"),
            201: _("Children"),
            230: _("News"),
            260: _("BBC Interactive"),
            670: _("Adult"),
            700: _("Radio"), }},

    "au": {
        "name": _("Australia"),
        "duplicates": {"lower": 350, "upper": 399}}}


choices = [(k, providers[k].get("name", _("Italy"))) for k in providers.keys()]
config.plugins.terrestrialbouquet = ConfigSubsection()
config.plugins.terrestrialbouquet.enabled = ConfigYesNo()
config.plugins.terrestrialbouquet.providers = ConfigSelection(
    default=choices[0][0], choices=choices)
config.plugins.terrestrialbouquet.makeradiobouquet = ConfigYesNo()
config.plugins.terrestrialbouquet.skipduplicates = ConfigYesNo(True)


class TerrestrialBouquet:
    def __init__(self):
        self.config = config.plugins.terrestrialbouquet
        self.bouquetFilename = "userbouquet.TerrestrialBouquet.tv"
        self.bouquetName = _('Terrestrial')
        self.services = {}
        self.VIDEO_ALLOWED_TYPES = [1, 17, 22, 25, 31,
                                    32] + [4, 5, 24, 27]  # tv (live and NVOD)
        self.AUDIO_ALLOWED_TYPES = [2, 10]

    def getTerrestrials(self, mode):
        terrestrials = {}
        query = "1:7:%s:0:0:0:0:0:0:0:%s ORDER BY name" % (1 if mode == MODE_TV else 2, " || ".join(
            ["(type == %s)" % i for i in self.getAllowedTypes(mode)]))
        if (servicelist := ServiceReference.list(
                ServiceReference(query))) is not None:
            while (service := servicelist.getNext()) and service.valid():
                if service.getUnsignedData(4) >> 16 == 0xeeee or service.getUnsignedData(
                        4) >> 16 == 61166:  # filter (only terrestrial)
                    stype, sid, tsid, onid, ns = [
                        int(x, 16) for x in service.toString().split(":", 7)[2:7]]
                    name = ServiceReference.getServiceName(service)
                    terrestrials["%08x:%04x:%04x:%04x" % (ns, onid, tsid, sid)] = {
                        "name": name, "namespace": ns, "onid": onid, "tsid": tsid, "sid": sid, "type": stype}
        return terrestrials

    def getAllowedTypes(self, mode):
        # tv (live and NVOD) and radio allowed service types
        return self.VIDEO_ALLOWED_TYPES if mode == MODE_TV else self.AUDIO_ALLOWED_TYPES

    def readLcnDb(self):
        LCNs = {}
        if LCNData := eDVBDB.getInstance().getLcnDBData():
            for service in LCNData:
                ns, onid, tsid, sid, lcn, signal = service
                # filter (only terrestrial)
                if ns >> 16 == 0xeeee or ns >> 16 == 61166:
                    LCNs["%08x:%04x:%04x:%04x" % (ns, onid, tsid, sid)] = {
                        "lcn": lcn, "signal": signal}
            LCNs = {
                k: v for k, v in sorted(
                    list(
                        LCNs.items()), key=lambda x: (
                        x[1]["lcn"], abs(
                            x[1]["signal"] - 65535)))} if LCNs else LCNs
        return LCNs

    def rebuild(self):
        if not self.config.enabled.value:
            return _("Terrestrial Bouquet plugin is not enabled.")
        msg = _("Try running a manual scan of terrestrial frequencies with network scan enabled. If this fails maybe there is no lcn data available in your area.")
        self.services.clear()
        if not (LCNs := self.readLcnDb()):
            return (_("There is currently no LCN data stored.")) + " " + msg
        for mode in (MODE_TV, MODE_RADIO):
            terrestrials = self.getTerrestrials(mode)
            for k in terrestrials:
                if k in LCNs:
                    terrestrials[k] |= LCNs[k]
            self.services |= terrestrials
        self.services = {
            k: v for k, v in sorted(
                list(
                    self.services.items()), key=lambda x: (
                    "lcn" in x[1] and x[1]["lcn"] or 65535, "signal" in x[1] and abs(
                        x[1]["signal"] - 65536) or 65535))}
        # duplicates (we are already ordered by highest signal strength)
        LCNsUsed = []
        for k in list(self.services.keys(
        )):  # use list to avoid RuntimeError: dictionary changed size during iteration
            if "lcn" not in self.services[k] or self.services[k]["lcn"] in LCNsUsed:
                if self.config.skipduplicates.value:
                    del self.services[k]
                else:
                    self.services[k]["duplicate"] = True
            else:
                LCNsUsed.append(self.services[k]["lcn"])
        if not self.services:
            return _("No corresponding terrestrial services found.") + " " + msg
        self.createBouquet()

    def createBouquet(self):
        radio_services = [x for x in self.services.values(
        ) if x["type"] in self.AUDIO_ALLOWED_TYPES and "lcn" in x]
        for mode in (MODE_TV, MODE_RADIO):
            if mode == MODE_RADIO and (
                    not radio_services or not self.config.makeradiobouquet.value):
                break
            allowed_service_types = not self.config.makeradiobouquet.value and self.VIDEO_ALLOWED_TYPES + \
                self.AUDIO_ALLOWED_TYPES or self.getAllowedTypes(mode)
            lcnindex = {v["lcn"]: k for k, v in self.services.items() if not v.get(
                "duplicate") and v.get("lcn") and v.get("type") in allowed_service_types}
            highestLCN = max(list(lcnindex.keys()))
            sections = providers[self.config.providers.value].get(
                "sections", {})
            active_sections = [max((x for x in list(sections.keys()) if int(
                x) <= key)) for key in list(lcnindex.keys())] if sections else []
            if not self.config.skipduplicates.value and (duplicates := sorted([(k, v) for k, v in self.services.items(
            ) if v.get("duplicate") and v.get("type") in allowed_service_types], key=lambda x: x[1]["name"].lower())):
                duplicate_range = {
                    "lower": highestLCN + 1, "upper": 65535} | providers[self.config.providers.value].get("duplicates", {})
                for i in range(
                        duplicate_range["lower"],
                        duplicate_range["upper"] + 1):
                    if i not in lcnindex:
                        duplicate = duplicates.pop(0)
                        lcnindex[i] = duplicate[0]
                        if not len(duplicates):
                            break
                sections[duplicate_range["lower"]] = _("Duplicates")
                active_sections.append(duplicate_range["lower"])
                highestLCN = max(list(lcnindex.keys()))
            bouquet_name = providers[self.config.providers.value].get(
                "bouquetname", self.bouquetName)
            bouquet_list = []
            # for number in range(1, (highestLCN) // 1000 * 1000 + 1001):   # ceil bouquet length to nearest 1000, range needs + 1
            # if mode == MODE_TV and number in active_sections:
            # bouquet_list.append("1:64:0:0:0:0:0:0:0:0:%s" % sections[number])

            for number in range(
                    1,
                    (highestLCN) //
                    1000 *
                    1000 +
                    1001):  # ceil bouquet length to nearest 1000, range needs + 1
                # Aggiungi un marker per le categorie (sezioni)
                if mode == MODE_TV and number in sections:
                    section_name = sections[number]
                    bouquet_list.append(
                        "1:64:0:0:0:0:0:0:0:0:%s" %
                        section_name)  # Marker per la categoria
                    # Aggiungere opzionalmente una descrizione
                    # bouquet_list.append("#DESCRIPTION %s" % section_name)

                if number in lcnindex:
                    service = self.services[lcnindex[number]]
                    bouquet_list.append(
                        "1:0:%x:%x:%x:%x:%x:0:0:0:" %
                        (service["type"],
                         service["sid"],
                            service["tsid"],
                            service["onid"],
                            service["namespace"]))
                else:
                    bouquet_list.append(
                        "1:320:0:0:0:0:0:0:0:0:")  # bouquet spacer
            eDVBDB.getInstance().addOrUpdateBouquet(bouquet_name,
                                                    self.bouquetFilename[:-2] + ("tv" if mode == MODE_TV else "radio"),
                                                    bouquet_list,
                                                    True)


class PluginSetup(Setup, TerrestrialBouquet):

    # <screen name="PluginSetup" position="0,0" size="1920,1080" title="Plugin Setup" backgroundColor="black" flags="wfNoBorder">
    # <panel name="timedate"/>
    # <panel name="bLogo"/>
    # <panel name="ScreenTemplateAllColorButtons_menu"/>
    # <widget source="session.VideoPicture" render="Pig" position="1280,120" zPosition="20" size="622,350" backgroundColor="transparent" transparent="0" cornerRadius="14"/>
    # <widget source="Title" render="Label" position="90,50" size="1167,52" font="Regular; 32" noWrap="1" transparent="1" valign="center" zPosition="1" halign="left"/>
    # <widget source="ScreenPath" render="Label" position="36,10" size="1380,22" backgroundColor="background" transparent="1" zPosition="1" font="Regular; 19" valign="center" halign="left"/>
    # <ePixmap position="33,36" size="66,54" pixmap="image_logo/nss/tLogo.png" alphatest="blend" transparent="1" zPosition="19"/>
    # <eLabel name="" position="20,110" size="1244,898" zPosition="-90" cornerRadius="30" backgroundColor="mcolor2" foregroundColor="mcolor2"/>
    # <eLabel backgroundColor="wpmc" cornerRadius="20" position="0,0" size="1920,1080" zPosition="-99"/>
    # <eLabel backgroundColor="buttonsc" cornerRadius="30" position="20,1014" size="1880,60" zPosition="-80"/>
    # <eLabel name="" position="1838,1018" size="52,52" backgroundColor="mcolor4" halign="center" valign="center" transparent="0" cornerRadius="26" font="Regular; 17" zPosition="1" text="EXIT"/>
    # <widget alphatest="blend" name="HelpWindow" position="194,802" size="906,188" transparent="1" zPosition="99" font="Regular; 30" halign="center"/>
    # <widget name="footnote" position="8,8" size="1,1" font="Regular; 26" halign="left" valign="bottom" foregroundColor="yellow" backgroundColor="background" transparent="1" zPosition="9"/>
    # <widget name="config" position="40,130" size="1200,630" valign="center" itemHeight="45" font="Regular; 30" itemCornerRadius="10" enableWrapAround="1" transparent="1" zPosition="9" scrollbarMode="showOnDemand" scrollbarSliderForegroundColor="mcolor5" scrollbarSliderBorderColor="mcolor2" scrollbarWidth="10" scrollbarSliderBorderWidth="1"/>
    # <widget name="description" position="1276,488" size="627,290" font="Regular; 28" halign="left" valign="top" foregroundColor="white" transparent="1" zPosition="55"/>
    # <eLabel backgroundColor="mcolor3" cornerRadius="3" position="40,776" size="534,3" zPosition="99"/>
    # <eLabel backgroundColor="mcolor3" cornerRadius="3" position="706,776" size="534,3" zPosition="99"/>
    # </screen>

    def __init__(self, session):
        TerrestrialBouquet.__init__(self)
        Setup.__init__(
            self,
            session,
            blue_button={
                'function': self.startrebuild,
                'helptext': _("Build/rebuild terrestrial bouquet now based on the last scan.")})
        self.title = _("Terrestrial Bouquet setup")
        self.updatebluetext()

    def createSetup(self):
        configlist = []
        indent = "- "
        configlist.append(
            (_("Enable terrestrial bouquet"),
             self.config.enabled,
             _("Enable creating a terrestrial bouquet based on LCN (logocal channel number) data.") +
                " " +
                _("This plugin depends on LCN data being broadcast by your local tansmitter.") +
                " " +
                _("Once configured the bouquet will be updated automatically when doing a manual scan.") +
                " " +
                _("Please make certain network search is enabled when scanning.")))
        if self.config.enabled.value:
            configlist.append(
                (indent + _("Region"),
                 self.config.providers,
                 _("Select your region.")))
            configlist.append(
                (indent + _("Create separate radio bouquet"),
                 self.config.makeradiobouquet,
                 _("Put radio services in a separate bouquet, not the main tv bouquet. This is required when the provider duplicates channel numbers for tv and radio.")))
            configlist.append(
                (indent + _("Skip duplicates"),
                 self.config.skipduplicates,
                 _("Do not add duplicated or non indexed channels to the bouquet.")))
        self["config"].list = configlist

    def changedEntry(self):
        Setup.changedEntry(self)
        self.updatebluetext()

    def updatebluetext(self):
        self["key_blue"].text = _(
            "Rebuild bouquet") if self.config.enabled.value else ""

    def startrebuild(self):
        if self.config.enabled.value:
            self.saveAll()
            if msg := self.rebuild():
                mb = self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
                mb.setTitle(_("Terrestrial Bouquet Error"))
            else:
                mb = self.session.open(
                    MessageBox,
                    _("Terrestrial bouquet successfully rebuilt."),
                    MessageBox.TYPE_INFO)
                mb.setTitle(_("Terrestrial Bouquet"))
                self.closeRecursive()


def PluginCallback(close, answer=None):
    if close and answer:
        close(True)


def PluginMain(session, close=None, **kwargs):
    session.openWithCallback(boundFunction(PluginCallback, close), PluginSetup)


def PluginStart(menuid, **kwargs):
    return menuid == "scan" and [
        (_("Terrestrial Bouquet"), PluginMain, "PluginMain", None)] or []


def Plugins(**kwargs):
    from Components.NimManager import nimmanager
    if nimmanager.hasNimType("DVB-T"):
        from Screens.ServiceScan import ServiceScan
        __origfunc = ServiceScan.ok

        def __newfunc(self, *args, **kwargs):
            if self["scan"].isDone() and "Terrestrial" in str(self.scanList):
                from .LCNScanner.Terrestrial import TerrestrialBouquet
                print(
                    "[TerrestrialBouquet] rebuilding terrestrial bouquet -",
                    TerrestrialBouquet().rebuild() or "was successful")
            __origfunc(self, *args, **kwargs)  # now run ServiceScan.ok
        ServiceScan.ok = __newfunc
        return [
            PluginDescriptor(
                name=_("Terrestrial Bouquet"),
                description=_("Create an ordered bouquet of terrestrial services based on LCN data from your local transmitter."),
                where=PluginDescriptor.WHERE_MENU,
                needsRestart=False,
                fnc=PluginStart)]
    return []
