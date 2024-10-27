#!/usr/bin/python
# -*- coding: utf-8 -*-

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#  Lululla coder 2022.07.20
# NOT REMOVE DISCLAIMER!!!

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
# from Screens.HelpMenu import HelpableScreen
from Screens.Screen import Screen
from Tools.Directories import fileExists
from enigma import eLabel
from errno import ENOENT
from os import system


DEFAULT_MODULE_NAME = __name__.split(".")[-1]
pname = _("File Commander - Addon")
pdesc = _("play/show Files")
pversion = "1.0-r1"


'''
# def answercheck(self, answer=None):
    # if answer is None:
        # self.session.openWithCallback(self.answercheck, MessageBox, _("This operation checks if the skin has its components (is not sure)..\nDo you really want to continue?"))
    # else:
        # zaddons = os.path.join(thisdir, 'addons')
        # if os.path.exists(zaddons):
            # from .addons import checkskin
            # self.check_module = eTimer()
            # check = checkskin.check_module_skin()
            # try:
                # self.check_module_conn = self.check_module.timeout.connect(check)
            # except:
                # self.check_module.callback.append(check)
            # self.check_module.start(100, True)
            # self.openVi()

# def openVi(self):
    # from .addons.type_utils import File_Commander
    # user_log = '/tmp/my_debug.log'
    # if fileExists(user_log):
        # self.session.open(File_Commander, user_log)
'''


# Calls onto the static function in eLabel. This avoids causing an invalidate
# on the parent container which is detrimental to UI performance,
# particularly in a complex screen like the graph EPG


def getTextBoundarySize(instance, font, targetSize, text):
    return eLabel.calculateTextSize(font, text, targetSize)


def fileReadLines(filename, default=None, source=DEFAULT_MODULE_NAME, debug=False):
    lines = None
    try:
        with open(filename, "r") as fd:
            lines = fd.read().splitlines()
    except OSError as err:
        if err.errno != ENOENT:  # ENOENT - No such file or directory.
            print("[%s] Error %d: Unable to read lines from file '%s'!  (%s)" % (source, err.errno, filename, err.strerror))
        lines = default
    return lines


class File_Commander(Screen):

    skin = """
        <screen name="File_Commander" position="40,80" size="1900,900" title="Linuxsat-support - File Commander">
            <widget name="list_head" position="8,10" size="1850,45" font="Regular;20" foregroundColor="#00fff000" />
            <widget name="filedata" scrollbarMode="showOnDemand" position="10,60" size="1850,750" itemHeight="50" />
            <widget name="key_red" position="100,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_green" position="395,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_yellow" position="690,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_blue" position="985,840" size="260,25" transparent="1" font="Regular;20" />
            <ePixmap position="70,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
            <ePixmap position="365,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
            <ePixmap position="660,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
            <ePixmap position="955,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
        </screen>"""

    def __init__(self, session, file):
        self.skin = File_Commander.skin
        Screen.__init__(self, session)
        # HelpableScreen.__init__(self)
        self.file_name = file
        title = "Linuxsat-support - File Commander"
        self.list = []
        self["filedata"] = MenuList(self.list)
        self["actions"] = ActionMap(["WizardActions", "ColorActions", "DirectionActions"], {
            "ok": self.exitEditor,
            "green": self.exitEditor,
            "back": self.exitEditor,
            "red": self.exitEditor,
            "yellow": self.SaveFile,
            "blue": self.exitEditor,
            # "chplus": self.posStart,
            # "chminus": self.posEnd,
        }, -1)
        self["list_head"] = Label(self.file_name)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Exit"))
        self["key_yellow"] = Label(_("Save"))
        self["key_blue"] = Label(_("Exit"))
        self.selLine = None
        self.oldLine = None
        self.isChanged = False
        self.skinName = "vEditorScreen"
        self.GetFileData(file)
        self.newtitle = title == 'vEditorScreen' and ('Console') or title
        self.onShown.append(self.updateTitle)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def exitEditor(self):
        # if fileExists(self.file_name):
            # remove(self.file_name)
        self.close()

    def GetFileData(self, fx):
        lines = fileReadLines(fx)
        if lines:
            for idx, line in enumerate(lines):
                self.list.append(str(idx + 1).zfill(4) + ": " + line)
        self["list_head"] = Label(fx)

    def posStart(self):
        self.selLine = 0
        self["filedata"].moveToIndex(0)

    def posEnd(self):
        self.selLine = len(self.list)
        self["filedata"].moveToIndex(len(self.list) - 1)

    def del_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        if len(self.list) > 1:
            self.isChanged = True
            del self.list[self.selLine]
            self.refreshList()

    def ins_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        self.list.insert(self.selLine, "0000: " + "" + '\n')
        self.isChanged = True
        self.refreshList()

    def refreshList(self):
        lineno = 1
        for x in self.list:
            my_x = x.partition(": ")[2]
            self.list.remove(x)
            self.list.insert(lineno - 1, str(lineno).zfill(4) + ": " + my_x)  # '\n')
            lineno += 1
        self["filedata"].setList(self.list)

    def SaveFile(self, answer):
        if answer is True:
            try:
                if fileExists(self.file_name):
                    system("cp " + self.file_name + " " + self.file_name + ".bak")
                eFile = open(self.file_name, "w")
                for x in self.list:
                    my_x = x.partition(": ")[2]
                    eFile.writelines(my_x)
                eFile.close()
            except OSError:
                pass
            self.close()
        else:
            self.close()
