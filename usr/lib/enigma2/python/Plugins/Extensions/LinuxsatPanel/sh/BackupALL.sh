#!/bin/bash
#DESCRIPTION=BACKUPALL
rm -rf /media/hdd/#Backups#
mkdir -p /media/hdd/#Backups#/BackupALL/etc/enigma2
cp -r /etc/epgimport /media/hdd//#Backups#/BackupALL/etc/
cp -r /etc/enigma2 /media/hdd//#Backups#/BackupALL/etc/
cp -r /etc/fstab /media/hdd//#Backups#/BackupALL/etc/fstab
mkdir -p /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom
mkdir -p /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/providers
cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom/sat_282_sky_uk_CustomMix.xml /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom/sat_282_sky_uk_CustomMix.xml  2>/dev/null
cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/providers/cable_uk_virgin.xml /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/providers/cable_uk_virgin.xml  2>/dev/null
cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/providers/sat_282_sky_uk.xml /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/providers/sat_282_sky_uk.xml  2>/dev/null
cp -r /usr/keys /media/hdd/#Backups#/BackupALL/usr
mkdir -p /media/hdd/#Backups#/BackupALL/etc/tuxbox/config
mkdir -p /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Screens
cp -r /etc/tuxbox/config /media/hdd/#Backups#/BackupALL/etc/tuxbox
([ -f /etc/CCcam.cfg ] && cp -r /etc/CCcam.cfg /media/hdd/#Backups#/BackupALL/etc/CCcam.cfg);
([ -f /usr/lib/enigma2/python/Screens/EpgSelection.py ] && cp -r /usr/lib/enigma2/python/Screens/EpgSelection.py /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Screens/EpgSelection.py);
## LINEBACKUP
mkdir -p /media/hdd/#Backups#/LineBackup/usr
cp -r /usr/keys /media/hdd/#Backups#/LineBackup/usr
mkdir -p /media/hdd/#Backups#/LineBackup/etc/tuxbox/config
cp -r /etc/tuxbox/config /media/hdd/#Backups#/LineBackup/etc/tuxbox
([ -f /etc/CCcam.cfg ] && cp -r /etc/CCcam.cfg /media/hdd/#Backups#/LineBackup/etc/CCcam.cfg);
## BOUQUETSBACKUP
mkdir -p /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/*.tv /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/*.radio /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/lamedb /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/lamedb5 /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
([ -f /usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom/favourites.xml ] && cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom/favourites.xml /media/hdd/#Backups#/BackupALL/usr/lib/enigma2/python/Plugins/SystemPlugins/AutoBouquetsMaker/custom/favourites.xml);
## EPGIMPORTBACKUP
mkdir -p /media/hdd/#Backups#/EPGimportBackup/etc
mkdir -p /media/hdd/#Backups#/EPGimportBackup/etc/enigma2
cp -r /etc/epgimport /media/hdd/#Backups#/EPGimportBackup/etc/
([ -f /etc/enigma2/epgimport.conf ] && cp -r /etc/enigma2/epgimport.conf /media/hdd/#Backups#/EPGimportBackup/etc/enigma2/epgimport.conf);
## TIMERSBACKUP
mkdir -p /media/hdd/#Backups#/TimerBackup/etc/enigma2
cp -r /etc/enigma2/autotimer.xml /media/hdd/#Backups#/TimerBackup/etc/enigma2/autotimer.xml
cp -r /etc/enigma2/timers.xml /media/hdd/#Backups#/TimerBackup/etc/enigma2/timers.xml
echo " "

echo " "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " *                                                             * "
echo " *                	 BACKUP UTILITY                   		 * "
echo " *                                                             * "
echo " *                                                             * "
echo " *                                                             * "
echo " *          YOUR SETTINGS HAVE BEEN BACKED UP TO:              * "
echo " *                                                             * "
echo " *                 /media/hdd/#Backups#/                       * "
echo " *                                                             * "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " "

exit 0