#!/bin/sh
#DESCRIPTION=multi-stalkerpro
echo " DOWNLOAD AND INSTALL multi-stalkerpro "
versions="1.2"
TMPDIR='/tmp'
PLUGINPATH='/usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro'
SETTINGS='/etc/enigma2/settings'
URL='https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main'
PYTHON_VERSION=$(python -c"import platform; print(platform.python_version())")
if [ -f /etc/apt/apt.conf ] ; then
STATUS='/var/lib/dpkg/status'
OS='DreamOS'
elif [ -f /etc/opkg/opkg.conf ] ; then
STATUS='/var/lib/opkg/status'
OS='Opensource'
fi
if python --version 2>&1 | grep -q '^Python 3\.'; then
echo "You have Python3 image"
PYTHON='PY3'
else
echo "You have Python2 image"
PYTHON='PY2'
fi
if [ $PYTHON = "PY3" ]; then
opkg update && opkg upgrade
opkg install p7zip
opkg install wget
opkg install curl
opkg install python3-lxml
opkg install python3-requests
opkg install python3-beautifulsoup4
opkg install python3-cfscrape
opkg install livestreamersrv
opkg install python3-six
opkg install python3-sqlite3
opkg install python3-pycrypto
opkg install f4mdump python3-image
opkg install python3-imaging
opkg install python3-argparse
opkg install python3-multiprocessing
opkg install python3-mmap
opkg install python3-ndg-httpsclient
opkg install python3-pydoc
opkg install python3-xmlrpc
opkg install python3-certifi
opkg install python3-urllib3
opkg install python3-chardet
opkg install python3-pysocks
opkg install python3-js2py
opkg install python3-pillow
opkg update
opkg install enigma2-plugin-systemplugins-serviceapp
opkg install ffmpeg
opkg install exteplayer3
opkg install gstplayer
opkg update
opkg install gstreamer1.0-plugins-good
opkg install gstreamer1.0-plugins-ugly
opkg install gstreamer1.0-plugins-base
opkg install gstreamer1.0-plugins-bad
else
opkg update && opkg upgrade
opkg update
opkg install
opkg install wget
opkg install curl
opkg install hlsdl
opkg install python-lxml
opkg install python-requests
opkg install python-beautifulsoup4
opkg install python-cfscrape
opkg install livestreamer
opkg install vlivestreamersrv
opkg install python-six
opkg install python-sqlite3
opkg install python-pycrypto
opkg install f4mdump
opkg install python-image
opkg install python-imaging
opkg install python-argparse
opkg install python-multiprocessing
opkg install python-mmap
opkg install python-ndg-httpsclient
opkg install python-pydoc python-xmlrpc
opkg install python-certifi
opkg install python-urllib3
opkg install python-chardet
opkg install python-pysocks
opkg install enigma2-plugin-systemplugins-serviceapp
opkg install ffmpeg
opkg install exteplayer3
opkg install gstplayer
opkg update
opkg install gstreamer1.0-plugins-good
opkg install gstreamer1.0-plugins-ugly
opkg install gstreamer1.0-plugins-base
opkg install gstreamer1.0-plugins-bad
fi
echo ""
sync
echo ""
echo "#         Enigma TOOLS $version INSTALLED SUCCESSFULLY              #"
echo "**************************************************************"
echo "**************************************************************"
echo "   UPLOADED BY  >>>>   EMIL_NABIL "
sleep 4;
if [ -e /etc/enigma2/MultiStalkerPro.json ]; then
cp -f /etc/enigma2/MultiStalkerPro.json /tmp
fi
echo " Remove Old Package "
opkg remove enigma2-plugin-extensions-multi-stalkerpro
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars* > /dev/null 2>&1
echo "Old Package removed "
if [ "$PYTHON_VERSION" == 3.11.0 -o "$PYTHON_VERSION" == 3.11.1 -o "$PYTHON_VERSION" == 3.11.2 -o "$PYTHON_VERSION" == 3.11.3 -o "$PYTHON_VERSION" == 3.11.4 -o "$PYTHON_VERSION" == 3.11.5 ]; then
echo ":You have $PYTHON_VERSION image ..."
PYTHONLASTV='PY3'
IMAGING='python3-imaging'
PYSIX='python3-six'
opkg install enigma2-plugin-systemplugins-serviceapp exteplayer3 gstplayer libc6 python3-core python3-cryptography python3-fuzzywuzzy python3-levenshtein python3-rarfile python3-requests python3-six python3-sqlite3 uchardet
elif [ "$PYTHON_VERSION" == 3.12.0 -o "$PYTHON_VERSION" == 3.12.1 -o "$PYTHON_VERSION" == 3.12.2 -o "$PYTHON_VERSION" == 3.12.3 -o "$PYTHON_VERSION" == 3.12.4 -o "$PYTHON_VERSION" == 3.12.5 ]; then
echo ":You have $PYTHON_VERSION image ..."
PYTHONLASTER='PY3'
IMAGING='python3-imaging'
PYSIX='python3-six'
opkg install enigma2-plugin-systemplugins-serviceapp exteplayer3 gstplayer libc6 python3-core python3-cryptography python3-fuzzywuzzy python3-levenshtein python3-rarfile python3-requests python3-six python3-sqlite3 uchardet
opkg install alsa-plugins, enigma2 libasound2 libavcodec60 libavformat60 libc6 libgcc1 libpython3.12-1.0 libstdc++6 python3-cryptography
elif [ "$PYTHON_VERSION" == 3.9.9 -o "$PYTHON_VERSION" == 3.9.7 -o "$PYTHON_VERSION" == 3.9.6 -o "$PYTHON_VERSION" == 3.8.5 ]; then
echo ":You have $PYTHON_VERSION image ..."
PYTHONL='PY3'
IMAGING='python3-imaging'
PYSIX='python3-six'
opkg install enigma2-plugin-systemplugins-serviceapp exteplayer3 gstplayer libc6 python3-core python3-cryptography python3-fuzzywuzzy python3-levenshtein python3-rarfile python3-requests python3-six python3-sqlite3 uchardet
elif [ "$PYTHON_VERSION" == 2.7.18 ]; then
echo ":You have $PYTHON_VERSION image ..."
PYTHON='PY2'
IMAGING='python-imaging'
PYSIX='python-six'
else
echo "Python is not supported"
sleep 4;
exit 1
fi
if grep -q $IMAGING $STATUS; then
imaging='Installed'
fi
if grep -q $PYSIX $STATUS; then
six='Installed'
fi
if [ "$imaging" = "Installed" -a "$six" = "Installed" ]; then
echo "All dependecies are installed"
else
if [ $OS = "Opensource" ]; then
echo "=========================================================================="
echo "Some Depends Need to Be downloaded From Feeds ...."
echo "=========================================================================="
echo "Opkg Update ..."
sleep 2;
echo "========================================================================"
opkg update
echo "========================================================================"
echo " Downloading $IMAGING , $PYSIX ......"
opkg install $IMAGING
echo "========================================================================"
opkg install $PYSIX
echo "========================================================================"
else
echo "=========================================================================="
echo "Some Depends Need to Be downloaded From Feeds ...."
echo "=========================================================================="
echo "apt Update ..."
echo "========================================================================"
apt-get update
echo "========================================================================"
echo " Downloading $IMAGING , $PYSIX ......"
apt-get install $IMAGING -y
echo "========================================================================"
apt-get install $PYSIX -y
echo "========================================================================"
fi
fi
if grep -q $IMAGING $STATUS; then
echo ""
else
echo "#########################################################"
echo "#       $IMAGING Not found in feed                      #"
echo "#########################################################"
fi
if grep -q $PYSIX $STATUS; then
echo ""
else
echo "#########################################################"
echo "#       $PYSIX Not found in feed                        #"
echo "#########################################################"
exit 1
fi
CHECK='/tmp/check'
uname -m > $CHECK
sleep 1;
if grep -qs -i 'mips' cat $CHECK ; then
echo "[ Your device is MIPS ]"
if [ "$PYTHON" = "PY2" ]; then
wget -q  "--no-check-certificate" https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py2.7_mips32el.tar.gz -O /tmp/multi-stalkerpro-py2.7_mips32el.tar.gz
tar -xzf /tmp/multi-stalkerpro-py2.7_mips32el.tar.gz -C /
sleep 2;
rm -f /tmp/multi-stalkerpro-py2.7_mips32el.tar.gz
elif [ "$PYTHONLASTER" = "PY3" ]; then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_mips32el.ipk" > /tmp/multi-stalkerpro-py3.12_mips32el.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_mips32el.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_mips32el.ipk
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif (grep -qs -i "openvix" /etc/image-version); then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_mips32el.ipk" > /tmp/python3-rarfile_4.1-r0_mips32el.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_mips32el.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_mips32el.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk" > /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
echo ""
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif (grep -qs -i "openbh" /etc/image-version); then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText* > /dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_mips32el.ipk" > /tmp/python3-rarfile_4.1-r0_mips32el.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_mips32el.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_mips32el.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk" > /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_mips32el-openvix-openbh.ipk
echo ""
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif [ "$PYTHONL" = "PY3" ]; then
if (grep -qs -i openpli /etc/issue); then
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3.9-rarfile_4.1-r0_mips32el.ipk" > /tmp/python3.9-rarfile_4.1-r0_mips32el.ipk
opkg install --force-depends /tmp/python3.9-rarfile_4.1-r0_mips32el.ipk
sleep 2
rm -f /tmp/python3.9-rarfile_4.1-r0_mips32el.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3.9-levenshtein_0.12.0-r0_mips32el.ipk" > /tmp/python3.9-levenshtein_0.12.0-r0_mips32el.ipk
opkg install --force-depends /tmp/python3.9-levenshtein_0.12.0-r0_mips32el.ipk
sleep 2
rm -f /tmp/python3.9-levenshtein_0.12.0-r0_mips32el.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3.9-fuzzywuzzy_0.18.0-r0_mips32el.ipk" > /tmp/python3.9-fuzzywuzzy_0.18.0-r0_mips32el.ipk
opkg install --force-depends /tmp/python3.9-fuzzywuzzy_0.18.0-r0_mips32el.ipk
sleep 2
rm -f /tmp/python3.9-fuzzywuzzy_0.18.0-r0_mips32el.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro_mipsel-py3.9-openpli-develop.ipk" > /tmp/multi-stalkerpro_mipsel-py3.9-openpli-develop.ipk
opkg install --force-depends /tmp/multi-stalkerpro_mipsel-py3.9-openpli-develop.ipk
sleep 2
rm -f /tmp/multi-stalkerpro_mipsel-py3.9-openpli-develop.ipk
echo ""
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
else
echo ""
sleep 4;
fi
fi
elif grep -qs -i 'armv7l' cat $CHECK ; then
echo "[ Your device is armv7l ]"
if [ "$PYTHONLASTV" = "PY3" ]; then
wget -q  "--no-check-certificate" https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.11_arm.tar.gz -O /tmp/multi-stalkerpro-py3.11_arm.tar.gz
tar -xzf /tmp/multi-stalkerpro-py3.11_arm.tar.gz -C /
sleep 2;
rm -f /tmp/multi-stalkerpro-py3.11_arm.tar.gz
elif [ "$PYTHONLASTER" = "PY3" ]; then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
sleep 1
if (grep -qs -i "openvix" /etc/image-version); then
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk" > /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk" > /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
echo ""
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif (grep -qs -i "openbh" /etc/image-version); then
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk" > /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_cortexa15hf-neon-vfpv4.ipk
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk" > /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_arm-openvix-openbh.ipk
echo ""
wget -O /etc/enigma2/MultiStalkerPro.json "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/MultiStalkerPro.json"
echo ""
else
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://github.com/emilnabil/multi-stalkerpro/raw/main/multi-stalkerpro-py3.12_arm.ipk" > /tmp/multi-stalkerpro-py3.12_arm.ipk
sleep 1
cd /tmp
opkg install --force-depends multi-stalkerpro-py3.12_arm.ipk
echo ""
echo ""
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
echo ""
echo ""
echo ""
echo ""
sleep 1
rm /tmp/multi-stalkerpro-py3.12_arm.ipk
fi
fi
fi
if [ "$PYTHONL" = "PY3" ]; then
if (grep -qs -i openpli /etc/issue); then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_armv7ahf-neon.ipk" > /tmp/python3-rarfile_4.1-r0_armv7ahf-neon.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_armv7ahf-neon.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_armv7ahf-neon.ipk
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-levenshtein_0.12.0-r0_armv7ahf-neon.ipk" > /tmp/python3-levenshtein_0.12.0-r0_armv7ahf-neon.ipk
opkg install --force-depends /tmp/python3-levenshtein_0.12.0-r0_armv7ahf-neon.ipk
sleep 2
rm -f /tmp/python3-levenshtein_0.12.0-r0_armv7ahf-neon.ipk
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-fuzzywuzzy_0.18.0-r0_armv7ahf-neon.ipk" > /tmp/python3-fuzzywuzzy_0.18.0-r0_armv7ahf-neon.ipk
opkg install --force-depends /tmp/python3-fuzzywuzzy_0.18.0-r0_armv7ahf-neon.ipk
sleep 2
rm -f /tmp/python3-fuzzywuzzy_0.18.0-r0_armv7ahf-neon.ipk
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro_openpli-develop.ipk" > /tmp/multi-stalkerpro_openpli-develop.ipk
opkg install --force-depends /tmp/multi-stalkerpro_openpli-develop.ipk
sleep 2
rm -f /tmp/multi-stalkerpro_openpli-develop.ipk
sleep 1;
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
echo ""
fi
fi
if [ "$PYTHON" = "PY2" ]; then
wget -q  "--no-check-certificate" https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py2.7_arm.tar.gz -O /tmp/multi-stalkerpro-py2.7_arm.tar.gz
sleep 1;
tar -xzf /tmp/multi-stalkerpro-py2.7_arm.tar.gz -C /
sleep 2;
rm -f /tmp/multi-stalkerpro-py2.7_arm.tar.gz
echo ""
sleep 2;
fi
echo ""
if grep -qs -i 'aarch64' cat $CHECK ; then
echo "[ Your device is aarch64 ]"
if [ "$PYTHONLASTER" = "PY3" ]; then
opkg remove enigma2-plugin-extensions-multi-stalkerpro
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12_aarch64.ipk" > /tmp/multi-stalkerpro-py3.12_aarch64.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12_aarch64.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12_aarch64.ipk
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif (grep -qs -i "openvix" /etc/image-version); then
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_aarch64.ipk" > /tmp/python3-rarfile_4.1-r0_aarch64.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_aarch64.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_aarch64.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk" > /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
elif (grep -qs -i "openbh" /etc/image-version); then
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/python3-rarfile_4.1-r0_aarch64.ipk" > /tmp/python3-rarfile_4.1-r0_aarch64.ipk
opkg install --force-depends /tmp/python3-rarfile_4.1-r0_aarch64.ipk
sleep 2
rm -f /tmp/python3-rarfile_4.1-r0_aarch64.ipk
echo ""
sleep 1;
cd /tmp
curl  -k -Lbk -m 55532 -m 555104 "https://raw.githubusercontent.com/emilnabil/multi-stalkerpro/main/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk" > /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
opkg install --force-depends /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
sleep 2
rm -f /tmp/multi-stalkerpro-py3.12-openvix-openbh_aarch64.ipk
echo ""
if [ -e /tmp/MultiStalkerPro.json ]; then
rm -f /etc/enigma2/MultiStalkerPro.json
cp -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
fi
echo ""
else
echo ""
fi
else
echo ""
sleep 2;
fi
echo ""
echo "#########################################################"
echo "**                                                                    *"
echo "**                       multi-stalkerpro                     *"
echo "**                                                                    *"
echo "***********************************************************************"
echo "   UPLOADED BY  >>>>   EMIL_NABIL "
sleep 4;
echo "   >>>>         RESTARING         <<<<"
sleep 3; 
if [ $OS = 'DreamOS' ]; then
    systemctl restart enigma2
else
    killall -9 enigma2
fi
exit 0

