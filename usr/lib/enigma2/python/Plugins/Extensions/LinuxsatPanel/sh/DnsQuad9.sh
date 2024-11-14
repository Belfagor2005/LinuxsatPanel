#!/bin/bash
#DESCRIPTION=DNS QUAD9
if [ ! -f /etc/resolv-backup.conf ] 
then
grep "nameserver.*" /etc/resolv.conf >> //etc/resolv-backup.conf
fi
> /etc/resolv.conf
rm -f /etc/resolv.conf
echo "nameserver 9.9.9.9" > /etc/resolv.conf
echo "nameserver 149.112.112.10" >> /etc/resolv.conf
echo "
* NETWORK RESTARTED*
* DNS QUAD9 DNS APPEND TO NAMESERVER *
> done
> your device will restart now please wait..."; 
sleep 3s; killall -9 enigma2
exit 0