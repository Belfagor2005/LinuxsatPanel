#!/bin/sh

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/BissFeedAutoKey ]; then
echo "> removing package please wait..."
sleep 3s 
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/BissFeedAutoKey > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/ProgressPixmap.py  > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/ServiceName2.py  > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/ServiceInfo2.py  > /dev/null 2>&1

status='/var/lib/opkg/status'
package='enigma2-plugin-extensions-bissfeed-autokey'
package1='enigma2-plugin-extensions-bissfeedautokey'

if grep -q $package $status; then
opkg remove $package
fi
if grep -q $package1 $status; then
opkg remove $package1
fi

echo "*******************************************"
echo "*             Removed Finished            *"
echo "*            Uploaded By Eliesat          *"
echo "*******************************************"
sleep 3s

else

##remove unnecessary files and folders
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

##check install deps
## Check python
pyVersion=$(python -c"from sys import version_info; print(version_info[0])")

##config
plugin=bissfeedautokey
version=2.8

if [ "$pyVersion" = 3 ]; then
url=https://gitlab.com/eliesat/extensions/-/raw/main/bissfeedautokey/bissfeedautokey-py3-2.8.tar.gz
package=/var/volatile/tmp/$plugin-py3-$version.tar.gz
else
url=https://gitlab.com/eliesat/extensions/-/raw/main/bissfeedautokey/bissfeedautokey-py2-2.8.tar.gz
package=/var/volatile/tmp/$plugin-py2-$version.tar.gz
fi

##download & install
echo "> Downloading $plugin-$version package  please wait ..."
sleep 3s

wget -O $package --no-check-certificate $url
tar -xzf $package -C /
extract=$?
rm -rf $package >/dev/null 2>&1


echo ''
if [ $extract -eq 0 ]; then
echo "> $plugin-$version package installed successfully"
echo "> Uploaded By ElieSat"
sleep 3s

else

echo "> $plugin-$version package installation failed"
sleep 3s
fi

fi
exit
