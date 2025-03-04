#!/usr/bin/python
# -*- coding: utf-8 -*-

# Components
from .. import _
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Tools.Directories import fileExists
from enigma import eLabel
from errno import ENOENT
#   by lululla
DEFAULT_MODULE_NAME = __name__.split(".")[-1]
pname = _("File Commander - Addon")
pdesc = _("play/show Files")
pversion = "1.0-r2"


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
            <widget name="headright" position="8,10" size="1850,45" font="Regular;20" foregroundColor="#00fff000" />
            <!-- <widget name="filedata" scrollbarMode="showOnDemand" position="10,60" size="1850,750" itemHeight="50" /> -->
            <widget name="filedata" render="Listbox" position="10,60" size="1850,750" selectionDisabled="1" transparent="1" scrollbarMode="showNever">
            <!-- <widget source="filedata" render="Listbox" position="10,60" size="1850,750" selectionDisabled="1" transparent="1" scrollbarMode="showNever"> -->
                <convert type="TemplatedMultiContent">
                    {"template": [
                        MultiContentEntryText(pos= (20, 0), size=(848, 75), font = 1, flags = RT_HALIGN_LEFT | RT_WRAP, text = 0), # Index 26 is the current directory + the current file.
                        MultiContentEntryText(pos = (20, 75), size = (150, 45), font = 0, flags = RT_HALIGN_LEFT, color = 0x00dddddd, color_sel = 0x0067b0c2 text = 1), # index 16 is the sort
                        # MultiContentEntryText(pos = (210, 75), size = (120, 45), font = 0, flags = RT_HALIGN_LEFT, text = 1), # index 1 is a symbolic mode
                        # MultiContentEntryText(pos = (330, 75), size = (150, 45), font = 0, flags = RT_HALIGN_RIGHT, text = 11), # index 11 is the scaled size
                        # MultiContentEntryText(pos = (500, 75), size = (360, 45), font = 0, flags = RT_HALIGN_RIGHT, text = 13), # index 13 is the modification time
                        ],
                        "fonts": [gFont("Regular", 42),gFont("Regular", 32)],
                        "itemHeight": 80,
                        # "selectionEnabled": False
                    }
                </convert>
            </widget>
            <!--
            <widget name="key_red" position="100,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_green" position="395,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_yellow" position="690,840" size="260,25" transparent="1" font="Regular;20" />
            <widget name="key_blue" position="985,840" size="260,25" transparent="1" font="Regular;20" />
            <ePixmap position="70,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
            <ePixmap position="365,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
            <ePixmap position="660,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
            <ePixmap position="955,840" size="260,25" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
            -->
            <ePixmap pixmap="buttons/redbutton.png" position="32,874" size="300,6" alphatest="blend" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Pixmap" pixmap="buttons/redbutton.png" position="32,874" size="300,6" alphatest="blend" objectTypes="key_red,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_red" position="27,826" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,Button,Label" transparent="1" />
            <widget source="key_red" render="Label" position="27,826" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_red,StaticText" transparent="1" />
            <!--#####green####/-->
            <ePixmap pixmap="buttons/greenbutton.png" position="342,874" size="300,6" alphatest="blend" objectTypes="key_green,Button,Label" transparent="1" />
            <widget source="key_green" render="Pixmap" pixmap="buttons/greenbutton.png" position="342,874" size="300,6" alphatest="blend" objectTypes="key_green,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_green" position="337,826" size="310,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" objectTypes="key_green,Button,Label" transparent="1" />
            <widget source="key_green" render="Label" position="337,826" size="310,45" zPosition="11" font="Regular; 30" valign="center" halign="center" backgroundColor="background" objectTypes="key_green,StaticText" transparent="1" />
            <!--#####yellow####/-->
            <ePixmap pixmap="buttons/yellowbutton.png" position="652,874" size="300,6" alphatest="blend" objectTypes="key_yellow,Button,Label" transparent="1" />
            <widget source="key_yellow" render="Pixmap" pixmap="buttons/yellowbutton.png" position="652,874" size="300,6" alphatest="blend" objectTypes="key_yellow,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_yellow" position="647,826" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_yellow,Button,Label" transparent="1" />
            <widget source="key_yellow" render="Label" position="649,826" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_yellow,StaticText" transparent="1" />
            <!--#####blue####/-->
            <ePixmap pixmap="buttons/bluebutton.png" position="962,874" size="300,6" alphatest="blend" objectTypes="key_blue,Button,Label" transparent="1" />
            <widget source="key_blue" render="Pixmap" pixmap="buttons/bluebutton.png" position="962,874" size="300,6" alphatest="blend" objectTypes="key_blue,StaticText" transparent="1">
              <convert type="ConditionalShowHide" />
            </widget>
            <widget name="key_blue" position="957,826" size="310,45" zPosition="11" font="Regular; 30" noWrap="1" valign="center" halign="center" backgroundColor="background" objectTypes="key_blue,Button,Label" transparent="1" />

        </screen>"""

    def __init__(self, session, file):
        self.skin = File_Commander.skin
        Screen.__init__(self, session)
        # HelpableScreen.__init__(self)
        self.file_name = file
        title = "Lululla Commander"
        self.list = [""]
        self["filedata"] = MenuList(self.list)
        self["actions"] = ActionMap(["WizardActions", "ColorActions", "DirectionActions"], {
            "ok": self.exitEditor,
            "green": self.SaveFile,
            "back": self.exitEditor,
            "red": self.exitEditor,
            "yellow": self.del_Line,
            "blue": self.del_Line,
            "chplus": self.posStart,
            "chminus": self.posEnd,
        }, -1)
        self["list_head"] = Label(self.file_name)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_("Del Line"))
        self["key_blue"] = Label(_("Ins Line"))
        self.selLine = None
        self.oldLine = None
        self.isChanged = False
        self.GetFileData()
        self.newtitle = title == 'vEditorScreen' and ('Console') or title
        self.onShown.append(self.updateTitle)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def exitEditor(self):
        self.close()

    def GetFileData(self):
        lines = fileReadLines(self.file_name)
        self.list = []
        if lines:
            for idx, line in enumerate(lines):
                line = line.replace("\x1b", "")
                print("line:", line)
                self.list.append((str(idx + 1).zfill(4) + ": " + line,))
        self["filedata"].setList(self.list)
        self["list_head"].setText(self.file_name)

    def posStart(self):
        self.selLine = 0
        self["filedata"].moveToIndex(0)

    def posEnd(self):
        self.selLine = len(self.list)
        self["filedata"].moveToIndex(len(self.list) - 1)

    def del_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        self.list.insert(self.selLine, "0000: " + "" + '\n')
        self.isChanged = True
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

    def SaveFile(self):
        try:
            if fileExists(self.file_name):
                import shutil
                shutil.copy(self.file_name, self.file_name + ".bak")

            with open(self.file_name, "w") as eFile:
                for x in self.list:
                    if isinstance(x, tuple):
                        x = x[0]  # Take the first element of the tuple
                    my_x = x.partition(": ")[2]
                    eFile.write(my_x + "\n")  # Ensure each line ends properly

        except (OSError, IOError) as e:
            print("Error saving file:", str(e))
        self.close()
