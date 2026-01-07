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

from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from enigma import eLabel
from Screens.Screen import Screen
from Tools.Directories import fileExists  # , fileReadLines
from errno import ENOENT
import sys
from gettext import gettext

_ = gettext

PY3 = sys.version_info[0] >= 3

DEFAULT_MODULE_NAME = __name__.split(".")[-1]

pname = "File Commander - Addon"
pdesc = "play/show Files"
pversion = "1.0-r3"


def getTextBoundarySize(instance, font, targetSize, text):
    return eLabel.calculateTextSize(font, text, targetSize)


def fileReadLines(filename, default=None, source=DEFAULT_MODULE_NAME, debug=False):
    lines = None
    try:
        # Python 2 non ha encoding, Python 3 sì
        if PY3:
            with open(filename, "r", encoding="utf-8") as fd:
                lines = fd.read().splitlines()
        else:
            with open(filename, "r") as fd:
                lines = fd.read().decode("utf-8").splitlines()
    except (OSError, IOError) as err:
        if err.errno != ENOENT:  # ENOENT - No such file or directory.
            print("[%s] Error %d: Unable to read lines from file '%s'!  (%s)" % (source, err.errno, filename, err.strerror))
        lines = default
    except UnicodeDecodeError:
        # Fallback per file non UTF-8
        try:
            with open(filename, "r") as fd:
                lines = fd.read().splitlines()
        except:
            lines = default
    return lines


class File_Commander(Screen):

    skin = """
        <screen name="File_Commander" position="40,80" size="1900,900" title="Lululla Commander">
            <widget name="list_head" position="8,10" size="1850,45" font="Regular;24" foregroundColor="#00fff000" />
            <widget name="filedata" scrollbarMode="showOnDemand" itemHeight="45" position="9,78" size="1850,725" />
            <widget name="key_red" position="95,820" zPosition="19" size="260,40" transparent="1" font="Regular;24" halign="center" />
            <widget name="key_green" position="395,820" zPosition="19" size="260,40" transparent="1" font="Regular;24" halign="center" />
            <widget name="key_yellow" position="690,820" zPosition="19" size="260,40" transparent="1" font="Regular;24" halign="center" />
            <widget name="key_blue" position="985,820" zPosition="19" size="260,40" transparent="1" font="Regular;24" halign="center" />
            <ePixmap position="95,865" size="260,25" zPosition="0" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
            <ePixmap position="395,865" size="260,25" zPosition="0" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
            <ePixmap position="690,865" size="260,25" zPosition="0" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
            <ePixmap position="985,870" size="260,25" zPosition="0" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
        </screen>"""

    def __init__(self, session, file):
        self.skin = File_Commander.skin
        Screen.__init__(self, session)
        # HelpableScreen.__init__(self)
        self.file_name = file
        title = "Lululla File Commander"
        # Operatore ternario compatibile Python 2
        self.newtitle = 'Console' if title == 'vEditorScreen' else title
        self.list = []
        self["filedata"] = MenuList(self.list)
        self["actions"] = ActionMap(["WizardActions", "ColorActions", "DirectionActions"], {
            "ok": self.edit_Line,
            "green": self.SaveFile,
            "back": self.exitEditor,
            "red": self.exitEditor,
            "yellow": self.del_Line,
            "blue": self.ins_Line,
            # "chplus": self.posStart,
            # "chminus": self.posEnd,
        }, -1)
        self["list_head"] = Label(self.file_name)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_("Del Line"))
        self["key_blue"] = Label(_("Ins Line"))
        self.selLine = None
        self.oldLine = None
        self.isChanged = False
        self.GetFileData(file)
        self.setTitle(self.newtitle)

    def exitEditor(self):
        self.close()

    def GetFileData(self, fx):
        lines = fileReadLines(fx)
        if lines:
            for idx, line in enumerate(lines):
                if not PY3 and isinstance(line, bytes):
                    try:
                        line = line.decode("utf-8")
                    except:
                        line = line.decode("latin-1")
                self.list.append(str(idx + 1).zfill(4) + ": " + line)
            self["filedata"].setList(self.list)
        self["list_head"].setText(fx)

    def posStart(self):
        self.selLine = 0
        self["filedata"].moveToIndex(0)

    def posEnd(self):
        if self.list:
            self.selLine = len(self.list) - 1
            self["filedata"].moveToIndex(self.selLine)

    def edit_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        if self.selLine is not None and 0 <= self.selLine < len(self.list):
            current_line_full = self.list[self.selLine]
            colon_pos = current_line_full.find(": ", 4)
            if colon_pos != -1:
                current_line_text = current_line_full[colon_pos + 2:]
            else:
                current_line_text = current_line_full

            from Screens.VirtualKeyBoard import VirtualKeyBoard
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard,
                                          title=_("Edit Line"), text=current_line_text)

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None:
            line_num = self.list[self.selLine][:6]  # Prendi "0001: "
            self.list[self.selLine] = line_num + callback
            self.isChanged = True
            self["filedata"].setList(self.list)
            self["filedata"].moveToIndex(self.selLine)

    def del_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        if self.selLine is not None and len(self.list) > 0:
            self.isChanged = True
            del self.list[self.selLine]
            self.refreshList()
            if self.selLine >= len(self.list):
                self.selLine = len(self.list) - 1
            if self.selLine >= 0:
                self["filedata"].moveToIndex(self.selLine)

    def ins_Line(self):
        self.selLine = self["filedata"].getSelectionIndex()
        if self.selLine is None:
            self.selLine = len(self.list)
        self.list.insert(self.selLine, "0000: " + "")
        self.isChanged = True
        self.refreshList()
        self["filedata"].moveToIndex(self.selLine)

    def refreshList(self):
        new_list = []
        for idx, line in enumerate(self.list):
            if ": " in line:
                text_part = line.split(": ", 1)[1]
            else:
                text_part = line
            new_list.append(str(idx + 1).zfill(4) + ": " + text_part)
        self.list = new_list
        self["filedata"].setList(self.list)

    def SaveFile(self):
        try:
            if fileExists(self.file_name):
                import shutil
                shutil.copy(self.file_name, self.file_name + ".bak")

            mode = "w"
            encoding = "utf-8"

            if PY3:
                with open(self.file_name, mode, encoding=encoding) as eFile:
                    for x in self.list:
                        if isinstance(x, tuple):
                            x = x[0]
                        if ": " in x:
                            text_to_save = x.split(": ", 1)[1]
                        else:
                            text_to_save = x
                        eFile.write(text_to_save + "\n")
            else:
                with open(self.file_name, mode) as eFile:
                    for x in self.list:
                        if isinstance(x, tuple):
                            x = x[0]
                        if ": " in x:
                            text_to_save = x.split(": ", 1)[1]
                        else:
                            text_to_save = x
                        eFile.write(str(text_to_save) + "\n")

            self.isChanged = False

        except (OSError, IOError) as e:
            print("Error saving file:", str(e))
        self.close()
