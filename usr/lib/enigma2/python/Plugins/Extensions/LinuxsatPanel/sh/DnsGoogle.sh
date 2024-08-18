#!/bin/sh
rm -f /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
echo "nameserver 8.8.4.4" >> /etc/resolv.conf

/etc/init.d/avahi-daemon stop
/etc/init.d/networking stop
killall -9 udhcpc
rm /var/run/udhcpc*
/etc/init.d/networking start
/etc/init.d/avahi-daemon start

echo ""
echo "* NETWORK RESTARTED*"
echo "* GOOGLE DNS APPEND TO NAMESERVER *"
exit 0
