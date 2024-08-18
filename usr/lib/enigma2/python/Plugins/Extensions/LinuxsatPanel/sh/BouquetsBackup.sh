#!/bin/bash
mkdir -p /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
mkdir -p /media/hdd/#Backups#/BackupALL/etc/enigma2
cp -r /etc/enigma2/*.tv /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/*.radio /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/lamedb /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/lamedb5 /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /etc/enigma2/*.tv /media/hdd/#Backups#/BackupALL/etc/enigma2
cp -r /etc/enigma2/*.radio /media/hdd/#Backups#/BackupALL/etc/enigma2
cp -r /etc/enigma2/lamedb /media/hdd/#Backups#/BackupALL/etc/enigma2
cp -r /etc/enigma2/lamedb5 /media/hdd/#Backups#/BackupALL/etc/enigma2
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " *                                                             * "
echo " *                WILLOBUILD BACKUP UTILITY                    * "
echo " *                                                             * "
echo " *                                                             * "
echo " *                                                             * "
echo " *          YOUR BOUQUETS HAVE BEEN BACKED UP TO:              * "
echo " *                                                             * "
echo " *          /media/hdd/#Backups#/BouquetsBackup                * "
echo " *                                                             * "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
exit 0