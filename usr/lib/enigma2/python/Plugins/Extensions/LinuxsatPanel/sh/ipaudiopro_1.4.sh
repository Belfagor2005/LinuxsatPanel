#! /bin/sh

wget https://raw.githubusercontent.com/emil237/updates-enigma/main/update-all-python.sh  -O - | /bin/sh

plugin="ipaudiopro"

git_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main"

version="1.4"

PLUGIN_PATH="/usr/lib/enigma2/python/Plugins/Extensions/IPaudioPro"

package="enigma2-plugin-extensions-$plugin"

temp_dir="/tmp"

OPKG_DIR="/etc/opkg/"

PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')

if [ -z "$PYTHON_VERSION" ]; then

echo "Python is not installed or could not detect Python version."

exit 1

fi

if command -v apt-get > /dev/null 2>&1; then

INSTALL="apt-get install -y"

CHECK_INSTALLED="dpkg -l"

CHECK_VERSION="dpkg-query -W -f='\${Version}'"

OS='DreamOS'

elif command -v opkg > /dev/null 2>&1; then

INSTALL="opkg install --force-reinstall --force-depends"

CHECK_INSTALLED="opkg list-installed"

CHECK_VERSION="opkg info"

OS='Opensource'

else

echo "Unsupported OS"

exit 1

fi

if [ -d "$PLUGIN_PATH" ]; then

echo "Removing existing plugin..."

if command -v opkg > /dev/null; then

opkg remove enigma2-plugin-extensions-ipaudiopro

elif command -v apt-get > /dev/null; then

apt-get remove enigma2-plugin-extensions-ipaudiopro -y

fi

rm -rf "$PLUGIN_PATH"

fi

arch=$(uname -m)

case $PYTHON_VERSION in

3.9.*) PYTHON='PY3'; PY_VERSION='3_9';;

3.10.*) PYTHON='PY3'; PY_VERSION='3_11';;

3.11.*) PYTHON='PY3'; PY_VERSION='3_11';;

3.12.[1-5]) PYTHON='PY3'; PY_VERSION='3_12';;

3.12.[6-9]) PYTHON='PY3'; PY_VERSION='3_12_ff7';;

3.13.*) PYTHON='PY3'; PY_VERSION='py3_13_ff7';;

2.7.*) PYTHON='PY2'; PY_VERSION='2_7';;

*)

echo "Python version not supported."

sleep 4

exit 1

;;

esac

if [ "$arch" = "mips" ]; then

package_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main/enigma2-plugin-extensions-ipaudiopro_${version}_mips32el_py${PY_VERSION}.ipk"

elif [ "$arch" = "armv7l" ]; then

if ls "$OPKG_DIR" | grep -q "cortexa15hf-neon-vfpv4"; then

package_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main/enigma2-plugin-extensions-ipaudiopro_${version}_cortexa15hf-neon-vfpv4_py${PY_VERSION}.ipk"

elif ls "$OPKG_DIR" | grep -q "cortexa9hf-neon"; then

package_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main/enigma2-plugin-extensions-ipaudiopro_${version}_cortexa9hf-neon_py${PY_VERSION}.ipk"

elif ls "$OPKG_DIR" | grep -q "cortexa7hf-vfp"; then

package_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main/enigma2-plugin-extensions-ipaudiopro_${version}_cortexa7hf-vfp_py${PY_VERSION}.ipk"

elif ls "$OPKG_DIR" | grep -q "armv7ahf-neon"; then

package_url="https://github.com/emilnabil/ipaudiopro/raw/refs/heads/main/enigma2-plugin-extensions-ipaudiopro_${version}_armv7ahf-neon_py${PY_VERSION}.ipk"

else

echo "Unknown CPU architecture"

exit 1

fi

else

echo "Unsupported architecture"

exit 1

fi

cd /tmp || exit 1

wget "$package_url" -O enigma2-plugin-extensions-ipaudiopro.ipk

$INSTALL "/tmp/enigma2-plugin-extensions-ipaudiopro.ipk"

rm -f "/tmp/enigma2-plugin-extensions-ipaudiopro.ipk"

wget -O "/usr/lib/enigma2/python/Plugins/Extensions/IPaudioPro/logo.png" "https://dreambox4u.com/emilnabil237/plugins/ipaudiopro/logo.png"

wget -O "/etc/enigma2/IPAudioPro.json" "https://dreambox4u.com/emilnabil237/plugins/ipaudiopro/IPAudioPro.json"

echo "###############################################################"

echo "#             IPAudioPro version 1.4 installed                 #"

echo "#              Uploaded By Emil_Nabil                          #"

echo "###############################################################"

sleep 3

echo "          Your Device Will RESTART Now  "

sleep 2

if grep -q "DreamOS" /etc/issue; then

if command -v systemctl > /dev/null 2>&1; then

echo "Restarting Enigma2 using systemctl..."

systemctl restart enigma2

else

echo "Systemctl not found, restarting Enigma2 using killall..."

killall -9 enigma2

fi

else

echo "Killing and restarting Enigma2 process..."

killall -9 enigma2

fi

exit 0
