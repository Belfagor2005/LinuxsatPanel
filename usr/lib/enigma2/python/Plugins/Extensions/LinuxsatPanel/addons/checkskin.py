#!/usr/bin/python
# -*- coding: utf-8 -*-

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#  Lululla coder 2022.07.20
# NOT REMOVE DISCLAIMER!!!
# Made from @Lululla 122023 - v.1.2

from __future__ import absolute_import
from Components.config import config
from Tools.Directories import SCOPE_PLUGINS
try:
    from Tools.Directories import SCOPE_SKIN as SCOPE_GUISKIN
except ImportError:
    from Tools.Directories import SCOPE_GUISKIN
from Tools.Directories import fileExists, resolveFilename
import os
import re
import sys
from os import remove

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



# Funzione di logging
with open(user_log, "w", encoding="utf-8") as log_file:
    log_file.write("Log Initialized\n")


def checklogskin(data):
    try:
        print(colorstart + str(data) + colorend)  # stampa sul terminale
        with open(user_log, "a", encoding="utf-8") as log_file:
            log_file.write("\n:> " + str(data))  # scrive nel file di log
    except Exception as e:
        print("Error logging data: %s" % str(e))  # gestisce gli errori
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

        with open(myPath, "r", encoding="utf-8") as myFile:
            for line in myFile:
                if inittag in line and endtag in line:
                    continue
                filecontent += line
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
        r = re.findall(r' %s="([a-zA-Z0-9_/\.]+)"' % look4Component, myContent)
        r = list(set(r))
        checklogskin("I found components: %s" % r)

        if r:
            for component in r:
                full_component_path = os.path.join(myPath, component)

                # Gestione dei componenti Renderer e Converter
                if look4Component in ['render', 'Convert']:
                    compiled_extension = ".pyc" if PY3 else ".pyo"
                    if not fileExists(full_component_path + compiled_extension) and fileExists(full_component_path + ".py"):
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
                        relative_path = os.path.join(mvi, "enigma2", cur_skin, component)
                        if not os.path.exists(relative_path):
                            upShowFile(relative_path)
                        else:
                            found_files.add(relative_path)

    except Exception as e:
        checklogskin("Error in checkComponent: %s" % str(e))


"""
# def find_unused_images(base_path, used_files):
    # unused_images = []

    # def upShowFile(name):
        # checklogskin("Unused images found: %s" % name)

    # for root, dirs, files in os.walk(base_path):
        # for file in files:
            # if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # full_path = os.path.join(root, file)
                # if full_path not in used_files:
                    # # unused_images.append(full_path)
                    # upShowFile(full_path)
    # # return unused_images
"""


# Trova i file immagine non utilizzati
def find_unused_images(base_path, used_files):
    unused_images = []

    def upShowFile(name):
        unused_images.append(name)  # Aggiungi il file alla lista degli inutilizzati

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Verifica se il file è un'immagine
                full_path = os.path.join(root, file)
                if full_path not in used_files:  # Se il file non è nella lista dei file usati
                    upShowFile(full_path)  # Aggiungi il file alla lista di quelli non usati

    if unused_images:
        checklogskin("Unused images found:")
        for image in unused_images:
            checklogskin(image)


# Controlla la skin e i file correlati
def check_module_skin():
    # path = "%senigma2/%s" % (mvi, cur_skin)
    # skin_base_fold = "%senigma2/%s/" % (mvi, cur_skin)
    # user_skin_file = '/tmp/merged_' + cur_skin + '.xml'
    # user_log = '/tmp/my_debug.log'
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
            with open(user_skin_file, "w", encoding="utf-8") as myFile:
                checklogskin("write myFile %s" % user_skin_file)
                myFile.write(user_skin)

        # Esegui `checkComponent` su ciascun tipo
        checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/'), used_files)
        checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/'), used_files)
        checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_GUISKIN, ''), used_files)
        checkComponent(user_skin, 'image', resolveFilename(SCOPE_GUISKIN, ''), used_files)

        # Trova immagini non utilizzate
        unused_images = find_unused_images(skin_base_fold, used_files)
        if unused_images:
            checklogskin("Unused images found:")
            for image in unused_images:
                checklogskin(image)

    except Exception as e:
        checklogskin("Error in check_module_skin: %s" % str(e))

    checklogskin("==FINISH CHECK MY SKIN %s==" % cur_skin)
