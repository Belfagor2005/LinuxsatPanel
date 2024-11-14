#!/bin/bash
#DESCRIPTION=CLOUDFARE DNS
if [ ! -f /etc/resolv-backup.conf ] 
then
grep "nameserver.*" /etc/resolv.conf >> //etc/resolv-backup.conf
fi
> /etc/resolv.conf
rm -f /etc/resolv.conf
echo "nameserver 1.1.1.1" > /etc/resolv.conf
echo "nameserver 1.0.0.1" >> /etc/resolv.conf
echo ""
echo "* NETWORK RESTARTED*
* CLOUDFARE DNS APPEND TO NAMESERVER *
> done
> your device will restart now please wait..."; 
sleep 3s; killall -9 enigma2
exit 0