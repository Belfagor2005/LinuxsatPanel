#!/bin/bash
#DESCRIPTION=TimerBackup
echo " "
echo " "
mkdir -p /media/hdd/#Backups#/TimerBackup/etc/enigma2
cp -r /etc/enigma2/autotimer.xml /media/hdd/#Backups#/TimerBackup/etc/enigma2/autotimer.xml
cp -r /etc/enigma2/timers.xml /media/hdd/#Backups#/TimerBackup/etc/enigma2/timers.xml
cp -r /etc/enigma2/autotimer.xml /media/hdd/#Backups#/BackupALL/etc/enigma2/autotimer.xml
cp -r /etc/enigma2/timers.xml /media/hdd/#Backups#/BackupALL/etc/enigma2/timers.xml
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
echo " *              YOUR TIMERS HAVE BEEN BACKED UP TO:            * "
echo " *                                                             * "
echo " *             /media/hdd/#Backups#/TimerBackup/               * "
echo " *                                                             * "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " "
echo " "
echo " "
echo " "
echo " "
echo " "
exit 0