#!/bin/bash
## setup command=wget -q "--no-check-certificate" https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/installer.sh -O - | /bin/sh

## Only This 2 lines to edit with new version ######
version='2.5.3'
changelog='\nFix Script\nreduced source code\n'

##############################################################

TMPPATH=/tmp/LinuxsatPanel-main
FILEPATH=/tmp/main.tar.gz

if [ ! -d /usr/lib64 ]; then
	PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/LinuxsatPanel
else
	PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/LinuxsatPanel
fi

## check depends packges
if [ -f /var/lib/dpkg/status ]; then
   STATUS=/var/lib/dpkg/status
   OSTYPE=DreamOs
else
   STATUS=/var/lib/opkg/status
   OSTYPE=OE20
fi
echo ""
if python --version 2>&1 | grep -q '^Python 3\.'; then
	echo "You have Python3 image"
	PYTHON=PY3
	Packagesix=python3-six
	Packagerequests=python3-requests
else
	echo "You have Python2 image"
	PYTHON=PY2
	Packagerequests=python-requests
fi


if [ -f /usr/bin/wget ]; then
    echo "wget exist"
else
	if [ $OSTYPE = "DreamOs" ]; then
		echo "dreamos"
		apt-get update && apt-get install wget
	else
		opkg update && opkg install wget
	fi
fi


if [ $PYTHON = "PY3" ]; then
	if grep -qs "Package: $Packagesix" cat $STATUS ; then
		echo ""
	else
		opkg update && opkg --force-reinstall --force-overwrite install python3-six
	fi
fi
echo ""
if grep -qs "Package: $Packagerequests" cat $STATUS ; then
	echo ""
else
	echo "Need to install $Packagerequests"
	echo ""
	if [ $OSTYPE = "DreamOs" ]; then
		apt-get update && apt-get install python-requests -y
	 
	elif [ $PYTHON = "PY3" ]; then
		opkg update && opkg --force-reinstall --force-overwrite install python3-requests
	elif [ $PYTHON = "PY2" ]; then
	  
		opkg update && opkg --force-reinstall --force-overwrite install python-requests
	
	fi
fi
echo ""

## Remove tmp directory
[ -r $TMPPATH ] && rm -f $TMPPATH > /dev/null 2>&1

## Remove tmp directory
[ -r $FILEPATH ] && rm -f $FILEPATH > /dev/null 2>&1

## Remove old plugin directory
[ -r $PLUGINPATH ] && rm -rf $PLUGINPATH

## Download and install plugin
## check depends packges
mkdir -p $TMPPATH
cd $TMPPATH
set -e
if [ $OSTYPE = "DreamOs" ]; then
   echo "# Your image is OE2.5/2.6 #"
   echo ""
else
   echo "# Your image is OE2.0 #"
   echo ""
fi

# if [ $OSTYPE != "DreamOs" ]; then
	# opkg update && opkg --force-reinstall --force-overwrite install ffmpeg gstplayer exteplayer3 enigma2-plugin-systemplugins-serviceapp
# fi
sleep 2

wget --no-check-certificate 'https://github.com/Belfagor2005/LinuxsatPanel/archive/refs/heads/main.tar.gz'
tar -xzf main.tar.gz
cp -r 'LinuxsatPanel-main/usr' '/'
set +e
cd
sleep 2

## Check if plugin installed correctly
if [ ! -d $PLUGINPATH ]; then
	echo "Some thing wrong .. Plugin not installed"
	rm -rf $TMPPATH > /dev/null 2>&1
	exit 1
fi

# Identify the box type from the hostname file
FILE="/etc/image-version"
box_type=$(head -n 1 /etc/hostname)
distro_value=$(grep '^distro=' "$FILE" | awk -F '=' '{print $2}')
distro_version=$(grep '^version=' "$FILE" | awk -F '=' '{print $2}')
echo "^^^^^^^^^^Debug information:" > /tmp/LinuxsatPanel_debug.txt
echo "BOX MODEL: $box_type" >> /tmp/LinuxsatPanel_debug.txt
echo "OO SYSTEM: $OSTYPE" >> /tmp/LinuxsatPanel_debug.txt
echo "PYTHON: $PYTHON" >> /tmp/LinuxsatPanel_debug.txt
echo "PLUGINPATH: $PLUGINPATH" >> /tmp/LinuxsatPanel_debug.txt
echo "IMAGE NAME: $distro_value" >> /tmp/LinuxsatPanel_debug.txt
echo "IMAGE VERSION: $distro_version" >> /tmp/LinuxsatPanel_debug.txt
echo "   "

rm -rf $TMPPATH > /dev/null 2>&1
sync
echo ""
echo ""
echo "#########################################################"
echo "#          LinuxsatPanel INSTALLED SUCCESSFULLY         #"
echo "#                developed by LULULLA                   #"
echo "#                                                       #"
echo "#               https://corvoboys.org                   #"
echo "#########################################################"
echo "#           your Device will RESTART Now                #"
echo "#########################################################"
sleep 5
killall -9 enigma2
exit 0