#!/bin/sh
#DESCRIPTION=iSettingE2
if [ -d /usr/lib/enigma2/python/Plugins/Extensions/iSettingE2 ]; then
echo "> removing package please wait..."
sleep 3s 
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/iSettingE2 > /dev/null 2>&1

status='/var/lib/opkg/status'
package='enigma2-plugin-extensions-isettinge2'

if grep -q $package $status; then
opkg remove $package > /dev/null 2>&1
fi

echo "*******************************************"
echo "*             Removed Finished            *"
echo "*******************************************"
sleep 3s

else

#remove unnecessary files and folders
if [  -d "/CONTROL" ]; then
rm -r  /CONTROL >/dev/null 2>&1
fi
rm -rf /control >/dev/null 2>&1
rm -rf /postinst >/dev/null 2>&1
rm -rf /preinst >/dev/null 2>&1
rm -rf /prerm >/dev/null 2>&1
rm -rf /postrm >/dev/null 2>&1
rm -rf /tmp/*.ipk >/dev/null 2>&1
rm -rf /tmp/*.tar.gz >/dev/null 2>&1

#config
plugin=isetting-e2
version=3.2
url=https://github.com/Belfagor2005/upload/raw/main/oe2.0/plugin_settings/isettings/isetting.tar
package=/var/volatile/tmp/$plugin-$version.tar.gz

#download & install
echo "> Downloading $plugin-$version package  please wait ..."
sleep 3s

wget -O $package --no-check-certificate $url
tar -xzf $package -C /
extract=$?

echo ''
if [ $extract -eq 0 ]; then
echo "> $plugin-$version package installed successfully"
echo "> Uploaded By Lululla"
sleep 3s

else
rm -rf $package >/dev/null 2>&1
echo "> $plugin-$version package installation failed"
sleep 3s
fi

fi

echo
echo "--- PostInst * IPK Scripting v1.6 - date 16.02.2024 ---"
echo 
echo '#!/usr/bin/python' >> /tmp/connect.py
echo '' >> /tmp/connect.py
echo 'import os, sys' >> /tmp/connect.py
echo 'init = """import sys' >> /tmp/connect.py
echo '' >> /tmp/connect.py
echo 'try:' >> /tmp/connect.py
echo '   from . import connectra' >> /tmp/connect.py
echo 'except ImportError:' >> /tmp/connect.py
echo '   import connectra' >> /tmp/connect.py 
echo '   sys.modules["%s.connectra" % __name__] = connectra"""' >> /tmp/connect.py
echo '' >> /tmp/connect.py          
echo 'pathP = sys.path' >> /tmp/connect.py
echo 'pyth = ""' >> /tmp/connect.py
echo 'pynum = ""' >> /tmp/connect.py
echo 'for p in pathP:' >> /tmp/connect.py
echo '     if p.find("site-packages") != -1 and p.find("site-packages/") == -1:' >> /tmp/connect.py
echo '          pyth = p+"/pyConnect"' >> /tmp/connect.py
echo '          pynum = (p.split("/python")[1].split("/")[0]).replace(".","")' >> /tmp/connect.py
echo 'if not os.path.exists(pyth+"/connectra.pyo") and not os.path.exists(pyth+"/connectra.pyc"):' >> /tmp/connect.py
echo '      if not os.path.isdir(pyth):' >> /tmp/connect.py
echo '          os.mkdir(pyth)' >> /tmp/connect.py     
echo '      if os.path.isdir(pyth):' >> /tmp/connect.py
echo '          a = open(pyth+"/connectra.py", "w")' >> /tmp/connect.py                    
echo '          a.write("#!/usr/bin/python\n")' >> /tmp/connect.py
echo '          a.write("import os\n")' >> /tmp/connect.py
echo '          a.write("Agent = '"'iSettingE2/3.5.9/20240124'"'\n")' >> /tmp/connect.py
echo '          a.close()' >> /tmp/connect.py
echo '          b = open(pyth+"/__init__.py", "w")' >> /tmp/connect.py               
echo '          b.write(init.strip("\n "))' >> /tmp/connect.py
echo '          b.close()' >> /tmp/connect.py                   
echo '      try:' >> /tmp/connect.py
echo '          import pyConnect.connectra' >> /tmp/connect.py              
echo '      except:pass' >> /tmp/connect.py                                 
echo '      if os.path.exists(pyth+"/connectra.py"):' >> /tmp/connect.py             
echo '            os.system("rm -rf "+pyth+"/connectra.py")' >> /tmp/connect.py
echo '            os.system("rm -rf "+pyth+"/__init__.py")' >> /tmp/connect.py                
echo '      if os.path.exists(pyth+"/__pycache__/connectra.cpython-"+pynum+".pyc"):' >> /tmp/connect.py                  
echo '            os.system("mv "+pyth+"/__pycache__/connectra.cpython-"+pynum+".pyc "+pyth+"/connectra.pyc")' >> /tmp/connect.py
echo '            os.system("mv "+pyth+"/__pycache__/__init__.cpython-"+pynum+".pyc "+pyth+"/__init__.pyc")' >> /tmp/connect.py                
echo '            os.system("rmdir "+pyth+"/__pycache__")' >> /tmp/connect.py
echo '      elif os.path.exists(pyth+"/__pycache__/connectra.cpython-"+pynum+".pyo"):' >> /tmp/connect.py                  
echo '           os.system("mv "+pyth+"/__pycache__/connectra.cpython-"+pynum+".pyo "+pyth+"/connectra.pyo")' >> /tmp/connect.py
echo '           os.system("mv "+pyth+"/__pycache__/__init__.cpython-"+pynum+".pyo "+pyth+"/__init__.pyo")' >> /tmp/connect.py    
echo '           os.system("rmdir "+pyth+"/__pycache__")' >> /tmp/connect.py
echo
echo '      if os.path.exists(pyth+"/connectra.pyc") and not os.path.exists(pyth+"/connectra.pyo"):' >> /tmp/connect.py
echo '           os.system("cp "+pyth+"/connectra.pyc "+pyth+"/connectra.pyo")' >> /tmp/connect.py   
echo '      if os.path.exists(pyth+"/connectra.pyo") and not os.path.exists(pyth+"/connectra.pyc"):' >> /tmp/connect.py
echo '           os.system("cp "+pyth+"/connectra.pyo "+pyth+"/connectra.pyc")' >> /tmp/connect.py
echo
echo '      if os.path.exists(pyth+"/__init__.pyc") and not os.path.exists(pyth+"/__init__.pyo"):' >> /tmp/connect.py
echo '           os.system("cp "+pyth+"/__init__.pyc "+pyth+"/__init__.pyo")' >> /tmp/connect.py
echo '      if os.path.exists(pyth+"/__init__.pyo") and not os.path.exists(pyth+"/__init__.pyc"):' >> /tmp/connect.py
echo '           os.system("cp "+pyth+"/__init__.pyo "+pyth+"/__init__.pyc")' >> /tmp/connect.py
echo
python /tmp/connect.py
rm -rf /tmp/connect* & > /dev/null

killall -9 enigma2

echo
echo "*******************************************"
echo "*           - Install finished -          *"
echo "*                   ***                   *"
echo "*         Restart GUI in progress ...     *"
echo "*                                         *"
echo "*                           by Diamondear *"
echo "*******************************************"
echo
exit 0

