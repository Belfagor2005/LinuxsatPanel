#!/bin/sh
if [ ! -f /etc/resolv-backup.conf ] 
then
grep "nameserver.*" /etc/resolv.conf >> //etc/resolv-backup.conf
fi
> /etc/resolv.conf

echo "nameserver 9.9.9.9" > /etc/resolv.conf; echo "nameserver 149.112.112.10" >> /etc/resolv.conf; echo "> done
> your device will restart now please wait..."; sleep 3s; killall -9 enigma2

exit 0