#!/bin/bash
rm -rf /etc/enigma2/lamedb
rm -rf /etc/enigma2/lamedb5
rm -rf /etc/enigma2/*.tv
rm -rf /etc/enigma2/*.radio
mkdir -p /media/hdd/#Backups#/BouquetsBackup/etc/enigma2
cp -r /media/hdd/#Backups#/BouquetsBackup/etc/enigma2/*.tv /etc/enigma2
cp -r /media/hdd/#Backups#/BouquetsBackup/etc/enigma2/*.radio /etc/enigma2
cp -r /media/hdd/#Backups#/BouquetsBackup/etc/enigma2/lamedb /etc/enigma2
cp -r /media/hdd/#Backups#/BouquetsBackup/etc/enigma2/lamedb5 /etc/enigma2
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " *                                                             * "
echo " *                WILLOBUILD RESTORE UTILITY                   * "
echo " *                                                             * "
echo " *                                                             * "
echo " *                                                             * "
echo " *       YOUR BOUQUETS HAVE BEEN RESTORED FROM BACKUP          * "
echo " *                                                             * "
echo " *       YOUR RECEIVER WILL RESTART TO RELOAD BOUQUETS         * "
echo " *                                                             * "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " "
echo " "
echo " "
echo " "
echo " "
sleep 5
init 4
init 3