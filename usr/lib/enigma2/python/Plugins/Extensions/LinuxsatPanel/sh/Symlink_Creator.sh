#!/bin/sh
## DESCRIPTION=This script created by Levi45\nThis script will create symlink
if [ -f /lib/ld-2.32.so ]; then
	ln -s /lib/ld-2.32.so /lib/ld-linux.so.3
	echo "ld-2.32.so symlink created"
else
	echo "ld-2.32.so not found"
fi

if [ -f /lib/ld-2.30.so ]; then
	ln -s /lib/ld-2.30.so /lib/ld-linux.so.3
	echo "ld-2.30.so symlink created"
else
	echo "ld-2.30.so not found"
fi


if [ -f /lib/ld-2.28.so ]; then
	ln -s /lib/ld-2.28.so /lib/ld-linux.so.3
	echo "ld-2.28.so symlink created"
else
	echo "ld-2.28.so not found"
fi

if [ -f /lib/ld-2.26.so ]; then
	ln -s /lib/ld-2.26.so /lib/ld-linux.so.3
	echo "ld-2.26.so symlink created"
else
	echo "ld-2.26.so not found"
fi

if [ -f /usr/lib/libcrypto.so.1.0.2 ]; then
	ln -sf /usr/lib/libcrypto.so.1.0.2 /usr/lib/libcrypto.so.1.0.0
	ln -sf /usr/lib/libcrypto.so.1.0.2 /usr/lib/libcrypto.so.0.9.8
	ln -sf /usr/lib/libcrypto.so.1.0.2 /usr/lib/libcrypto.so.0.9.7
	echo "libcrypto.so.1.0.2 symlinks created"
else
	echo "libcrypto.so.1.0.2 not found"
fi

if [ -f /usr/lib/libssl.so.1.0.2 ]; then
	ln -sf /usr/lib/libssl.so.1.0.2 /usr/lib/libssl.so.1.0.0
	ln -sf /usr/lib/libssl.so.1.0.2 /usr/lib/libssl.so.0.9.8
	ln -sf /usr/lib/libssl.so.1.0.2 /usr/lib/libssl.so.0.9.7
	echo "libssl.so.1.0.2 symlinks created"
else
	echo "libssl.so.1.0.2 not found"
fi
sync
echo "#########################################################"
echo "#                SYMLINKS CREATED SUCCESSFULLY          #"
echo "#########################################################"

exit 0
