#!/usr/bin/python
# -*- coding: utf-8 -*-

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#  Lululla coder 2022.07.20
# NOT REMOVE DISCLAIMER!!!

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
pythonFull = float(str(sys.version_info.major) + "." + str(sys.version_info.minor))
mvi = '/usr/share/'
cur_skin = config.skin.primary_skin.value.replace('/skin.xml', '')


def checklogskin(data):
    print(colorstart + str(data) + colorend)
    with open("/tmp/my_debug.log", "a") as log_file:
        log_file.write("\n:> " + str(data))


def crea_file_temporaneo(xml_files, temp_path="/tmp/merged.xml"):
    with open(temp_path, 'w', encoding='utf-8') as temp_file:
        for file_path in xml_files:
            with open(file_path, 'r', encoding='utf-8') as xml_file:
                temp_file.write(xml_file.read())
    return temp_path


def check_module_skin():
    path = "%senigma2/%s" % (mvi, cur_skin)
    listDir = []
    for (root, dirs, files) in os.walk(path):
        listDir.extend(dirs)

    user_skin = ""
    user_skin2 = ""
    skin_base_fold = "%senigma2/%s/" % (mvi, cur_skin)
    user_skin_file = '/tmp/merged_' + cur_skin + '.xml'
    user_log = '/tmp/my_debug.log'

    if fileExists(user_skin_file):
        remove(user_skin_file)
    if fileExists(user_log):
        remove(user_log)

    checklogskin("==INIT CHECK MY SKIN %s==" % cur_skin)
    checklogskin("skin_base_fold %s" % skin_base_fold)
    checklogskin("python ver. %s" % pythonFull)

    # Unisci i contenuti XML da skin_base_fold
    for f in os.listdir(skin_base_fold):
        if f.endswith('.xml'):
            user_skin += readXMLfile(os.path.join(skin_base_fold, f))

    # Verifica i file extra nelle sottocartelle di skin_base_fold
    for root, dirs, files in os.walk(skin_base_fold):
        for f in files:
            if f.endswith('.xml'):
                user_skin2 += readXMLfile(os.path.join(root, f))

    if user_skin:
        user_skin = "<skin>\n" + user_skin + '\n' + user_skin2 + "</skin>\n"
        with open(user_skin_file, "w") as myFile:
            checklogskin("write myFile %s" % user_skin_file)
            myFile.write(user_skin)

    # Esegui `checkComponent` su ciascun tipo
    checkComponent(user_skin, 'render', resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/'))
    checkComponent(user_skin, 'Convert', resolveFilename(SCOPE_PLUGINS, '../Components/Converter/'))
    checkComponent(user_skin, 'pixmap', resolveFilename(SCOPE_GUISKIN, ''))
    checkComponent(user_skin, 'image', resolveFilename(SCOPE_GUISKIN, ''))

    checklogskin("==FINISH CHECK MY SKIN %s==" % cur_skin)


def checkComponent(myContent, look4Component, myPath):
    checklogskin("RESEARCH IN PROGRESS...")

    def upShowFile(name):
        checklogskin("Missing component found: %s" % name)

    r = re.findall(r' %s="([a-zA-Z0-9_/\.]+)"' % look4Component, myContent)
    r = list(set(r))
    checklogskin("I found components: %s" % r)

    if r:
        try:
            checklogskin("Research for %s components" % look4Component)
            for component in r:
                component_path = component
                full_component_path = myPath + component_path

                # Gestione dei componenti Renderer e Converter
                if look4Component in ['render', 'Convert']:
                    compiled_extension = ".pyc" if PY3 else ".pyo"
                    if not fileExists(full_component_path + compiled_extension) and fileExists(full_component_path + ".py"):
                        upShowFile(full_component_path + compiled_extension)

                # Gestione di immagini e pixmap
                elif look4Component in ['pixmap', 'image']:
                    if component.startswith('/'):
                        # Percorso assoluto
                        if not os.path.exists(component_path):
                            upShowFile(component_path)
                    else:
                        # Percorso relativo
                        relative_path = os.path.join(mvi, "enigma2", cur_skin, component_path)
                        if not os.path.exists(relative_path):
                            upShowFile(relative_path)
        except Exception as e:
            error_message = "Error:", str(e)
            print(error_message)
            checklogskin(error_message)
    return


def readXMLfile(XMLfilename):
    myPath = os.path.realpath(XMLfilename)
    if not os.path.exists(myPath):
        return ''

    filecontent = ''
    inittag = '<!--'
    endtag = '-->'

    with open(myPath, "r") as myFile:
        for line in myFile:
            if inittag in line and endtag in line:
                continue
            filecontent += line
    return filecontent
