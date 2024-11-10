#!/bin/bash
#DESCRIPTION=TimerRestore
rm tempfl.txt 2> /dev/null
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
echo " *         YOUR RECORDING TIMERS HAVE BEEN RESTORED            * "
echo " *                                                             * "
echo " *   YOUR RECEIVER WILL RESTART FOR CHANGES TO TAKE EFFECT     * "
echo " *                                                             * "
echo " * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * "
echo " "
echo " "
echo " "
echo " "
echo " "
sleep 5
init 4
rm -rf /etc/enigma2/timers.xml
cp -R /media/hdd/#Backups#/TimerBackup/. /
killall -9 enigma2
init 3