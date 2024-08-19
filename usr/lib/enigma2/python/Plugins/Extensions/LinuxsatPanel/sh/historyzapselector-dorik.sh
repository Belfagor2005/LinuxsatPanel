#!/bin/sh

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector ]; then
echo "> removing package please wait..."
sleep 3s 
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/HistoryZapSelector > /dev/null 2>&1

status='/var/lib/opkg/status'
package='enigma2-plugin-extensions-historyzapselector'

if grep -q $package $status; then
opkg remove $package > /dev/null 2>&1
fi

echo "*******************************************"
echo "*             Removed Finished            *"
echo "*            Uploaded By Eliesat          *"
echo "*******************************************"
sleep 3s

else

#remove unnecessary files and folders
if [  -d "/CONTROL" ]; then
rm -r  /CONTROL >/dev/null 2>&1
fi
rm -rf /control >/dev/null 2>&1
rm -rf /postinst >/dev/null 2>&1
rm -rf /preinst >/dev/null 2>&1
rm -rf /prerm >/dev/null 2>&1
rm -rf /postrm >/dev/null 2>&1
rm -rf /tmp/*.ipk >/dev/null 2>&1
rm -rf /tmp/*.tar.gz >/dev/null 2>&1

#config
plugin=historyzapselector-dorik
version=1.0.41
url=https://gitlab.com/eliesat/extensions/-/raw/main/historyzapselector/historyzapselector-dorik-1.0.41.tar.gz
package=/var/volatile/tmp/$plugin-$version.tar.gz

if [ -f /etc/image-version ]; then
    image=$(cat /etc/image-version | grep -iF "creator" | cut -d"=" -f2 | xargs)
elif [ -f /etc/issue ]; then
    image=$(cat /etc/issue | head -n1 | awk '{print $1;}')
else
    image=''
fi
[[ ! -z "$image" ]] && echo -e "${YELLOW}$image${NC} image detected"

#download & install
echo "> Downloading $plugin-$version package  please wait ..."
sleep 3s

wget --show-progress -qO $package --no-check-certificate $url
tar -xzf $package -C /
extract=$?
rm -rf $package >/dev/null 2>&1

PluginName="HistoryZapSelector"
pyver=$(python -V 2>&1 | cut -d\  -f2 | awk -F "." '{print $1$2}')
destination="/usr/lib/enigma2/python/Plugins/Extensions/$PluginName"
cp -a $destination/$pyver/. $destination/ > /dev/null 2>&1

if [ $? -eq 0 ];then
    echo $'27\n38\n39\n310\n311\n312\n' | xargs -I{} rm -fr $destination/{}
    find . -name "enigma2-plugin-extensions-historyzap_*.*" -type f -delete
    cur_year=$(date +'%Y')
    echo $'\n'
    echo "> $plugin-$version package installed successfully"
echo "> Uploaded By ElieSat"
sleep 3s
    
else
    echo "> $plugin-$version package installation failed"
sleep 3s
    exit 1
fi

fi
exit 0
