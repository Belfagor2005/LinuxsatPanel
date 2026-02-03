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

from __future__ import absolute_import
from Components.config import config
from os import remove
from Tools.Directories import SCOPE_PLUGINS
try:
    from Tools.Directories import SCOPE_SKIN as SCOPE_GUISKIN
except ImportError:
    from Tools.Directories import SCOPE_GUISKIN
from Tools.Directories import fileExists, resolveFilename
import os
import sys


colorend = '\033[m'
colorstart = '\033[31m'
PY3 = sys.version_info.major >= 3
pythonFull = float("%s.%s" % (sys.version_info.major, sys.version_info.minor))
tmplog = '/tmp/'
mvi = '/usr/share/'
cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')
skin_base_fold = "%senigma2/%s/" % (mvi, cur_skin)
user_skin_file = tmplog + 'merged_' + cur_skin + '.xml'
user_log = tmplog + 'my_debug.log'


# Funzione di logging compatibile con Python 2 e 3
try:
    if PY3:
        # Python 3: usa encoding
        with open(user_log, "w", encoding="utf-8") as log_file:
            log_file.write("Log Initialized\n")
    else:
        # Python 2: no encoding parameter
        with open(user_log, "w") as log_file:
            log_file.write("Log Initialized\n")
except Exception as e:
    print("Error initializing log: %s" % str(e))


def checklogskin(data):
    try:
        print(colorstart + str(data) + colorend)  # stampa sul terminale
        if PY3:
            # Python 3
            with open(user_log, "a", encoding="utf-8") as log_file:
                log_file.write("\n:> " + str(data))
        else:
            # Python 2
            with open(user_log, "a") as log_file:
                log_file.write("\n:> " + str(data).encode('utf-8'))
    except Exception as e:
        print("Error logging data: %s" % str(e))
        print("Logging failed!")


# Legge un file XML ignorando i commenti
def readXMLfile(XMLfilename):
    try:
        myPath = os.path.realpath(XMLfilename)
        if not os.path.exists(myPath):
            return ''

        filecontent = ''
        inittag = '<!--'
        endtag = '-->'

        if PY3:
            # Python 3
            with open(myPath, "r", encoding="utf-8") as myFile:
                for line in myFile:
                    if inittag in line and endtag in line:
                        continue
                    filecontent += line
        else:
            # Python 2
            with open(myPath, "r") as myFile:
                for line in myFile:
                    if inittag in line and endtag in line:
                        continue
                    filecontent += line.decode(
                        'utf-8') if isinstance(line, bytes) else line
        return filecontent

    except Exception as e:
        checklogskin("Error reading XML file %s: %s" % (XMLfilename, str(e)))
        return ''


# Verifica i componenti e i file necessari
def checkComponent(myContent, look4Component, myPath, found_files):
    checklogskin("RESEARCH IN PROGRESS...")

    def upShowFile(name):
        checklogskin("Missing component found: %s" % name)

    try:
        from re import findall
        r = findall(r' %s="([a-zA-Z0-9_/\.]+)"' % look4Component, myContent)
        r = list(set(r))
        checklogskin("I found components: %s" % r)

        if r:
            for component in r:
                full_component_path = os.path.join(myPath, component)

                # Gestione dei componenti Renderer e Converter
                if look4Component in ['render', 'Convert']:
                    compiled_extension = ".pyc" if PY3 else ".pyo"
                    if not fileExists(
                            full_component_path +
                            compiled_extension) and fileExists(
                            full_component_path +
                            ".py"):
                        upShowFile(full_component_path + compiled_extension)

                # Gestione di immagini e pixmap
                elif look4Component in ['pixmap', 'image']:
                    if component.startswith('/'):
                        # Percorso assoluto
                        if not os.path.exists(component):
                            upShowFile(component)
                        else:
                            found_files.add(component)
                    else:
                        # Percorso relativo
                        relative_path = os.path.join(
                            mvi, "enigma2", cur_skin, component)
                        if not os.path.exists(relative_path):
                            upShowFile(relative_path)
                        else:
                            found_files.add(relative_path)

    except Exception as e:
        checklogskin("Error in checkComponent: %s" % str(e))


# Trova i file immagine non utilizzati
def find_unused_images(base_path, used_files):
    unused_images = []

    def upShowFile(name):
        unused_images.append(name)

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                full_path = os.path.join(root, file)
                if full_path not in used_files:
                    upShowFile(full_path)

    if unused_images:
        checklogskin("Unused images found:")
        for image in unused_images:
            checklogskin(image)

    return unused_images


# Controlla la skin e i file correlati
def check_module_skin():
    if fileExists(user_skin_file):
        remove(user_skin_file)
    if fileExists(user_log):
        remove(user_log)

    checklogskin("==INIT CHECK MY SKIN %s==" % cur_skin)
    checklogskin("skin_base_fold %s" % skin_base_fold)
    checklogskin("python ver. %s" % pythonFull)

    try:
        user_skin = ""
        used_files = set()

        # Unisci i contenuti XML da skin_base_fold
        for root, dirs, files in os.walk(skin_base_fold):
            for f in files:
                if f.endswith('.xml'):
                    user_skin += readXMLfile(os.path.join(root, f))

        if user_skin:
            user_skin = "<skin>\n" + user_skin + "</skin>\n"
            if PY3:
                with open(user_skin_file, "w", encoding="utf-8") as myFile:
                    checklogskin("write myFile %s" % user_skin_file)
                    myFile.write(user_skin)
            else:
                with open(user_skin_file, "w") as myFile:
                    checklogskin("write myFile %s" % user_skin_file)
                    myFile.write(user_skin.encode('utf-8'))

        # Esegui `checkComponent` su ciascun tipo
        checkComponent(
            user_skin,
            'render',
            resolveFilename(
                SCOPE_PLUGINS,
                '../Components/Renderer/'),
            used_files)
        checkComponent(
            user_skin,
            'Convert',
            resolveFilename(
                SCOPE_PLUGINS,
                '../Components/Converter/'),
            used_files)
        checkComponent(
            user_skin,
            'pixmap',
            resolveFilename(
                SCOPE_GUISKIN,
                ''),
            used_files)
        checkComponent(
            user_skin,
            'image',
            resolveFilename(
                SCOPE_GUISKIN,
                ''),
            used_files)

        # Trova immagini non utilizzate
        unused_images = find_unused_images(skin_base_fold, used_files)

        # MOSTRA le immagini non utilizzate
        if unused_images:
            checklogskin("=== UNUSED IMAGES FOUND ===")
            for image in unused_images:
                checklogskin("Unused: %s" % image)
            checklogskin("Total unused images: %d" % len(unused_images))
        else:
            checklogskin("No unused images found.")

    except Exception as e:
        checklogskin("Error in check_module_skin: %s" % str(e))

    checklogskin("==FINISH CHECK MY SKIN %s==" % cur_skin)
