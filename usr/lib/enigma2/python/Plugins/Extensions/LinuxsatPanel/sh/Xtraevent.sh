#!/bin/bash
#DESCRIPTION=xtraevent-install
##setup command=wget -q "--no-check-certificate" https://github.com/popking159/xtraeventplugin/raw/main/xtraevent-install.sh -O - | /bin/bash
echo ''
echo '************************************************************'
echo "**                       STARTED                          **"
echo '************************************************************'
echo "**                  Uploaded by: MNASR                    **"
echo "************************************************************"
echo ''
sleep 3s

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/xtraEvent ]; then
echo "> removing package please wait..."
sleep 3s 
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/xtraEvent > /dev/null 2>&1
fi

status='/var/lib/opkg/status'
package='enigma2-plugin-extensions-xtraevent'

if grep -q $package $status; then
opkg remove $package > /dev/null 2>&1
fi

sleep 3s

echo "downloading xtraevent..."
wget -O  /var/volatile/tmp/xtraeventcore.tar.gz https://github.com/popking159/xtraeventplugin/raw/main/xtraeventcore.tar.gz
echo "Installing xtraevent..."
tar -xzf /var/volatile/tmp/xtraeventcore.tar.gz -C /
rm -rf /var/volatile/tmp/xtraeventcore.tar.gz
sync
echo "#########################################################"
echo "#########################################################"

SETTINGS="/etc/enigma2/settings"
echo "Adding new settings for xtraEvent..."
echo ""
echo ">>>>>>>>>     RESTARTING     <<<<<<<<<"
echo ""
init 4
sleep 3
sed -i "/xtraEvent/d" $SETTINGS
{
    echo "config.plugins.xtraEvent.apis=True"
	echo "config.plugins.xtraEvent.deletFiles=False"
	echo "config.plugins.xtraEvent.extra3=True"
 	echo "config.plugins.xtraEvent.fanartAPI=6d231536dea4318a88cb2520ce89473b"
	echo "config.plugins.xtraEvent.FanartSearchType=movies"
 	echo "config.plugins.xtraEvent.imgNmbr=2"
	echo "config.plugins.xtraEvent.loc=/media/hdd/"
 	echo "config.plugins.xtraEvent.logoFiles=True"
 	echo "config.plugins.xtraEvent.maze=True"
  	echo "config.plugins.xtraEvent.omdbAPI=cb1d9f55"
   	echo "config.plugins.xtraEvent.PB=backdrops"
	echo "config.plugins.xtraEvent.searchMANUELnmbr=1"
	echo "config.plugins.xtraEvent.searchNUMBER=8"
	echo "config.plugins.xtraEvent.searchType=movie"
	echo "config.plugins.xtraEvent.timerHour=2"
	echo "config.plugins.xtraEvent.timerMod=Period"
	echo "config.plugins.xtraEvent.tmdbAPI=c7ca0c239088f1ae72a197d1b4be51b8"
	echo "config.plugins.xtraEvent.tvdb=True"
	echo "config.plugins.xtraEvent.tvdbAPI=a99d487bb3426e5f3a60dea6d3d3c7ef"
	
} >> $SETTINGS

# ============================================================================================================
sleep 2
sync
init 3
echo "==================================================================="
echo "===                          FINISHED                           ==="
echo "                         script by MNASR                        ==="
echo "                   thanks to digiteng & kitte888                ==="
echo "==================================================================="
sleep 2
exit 0