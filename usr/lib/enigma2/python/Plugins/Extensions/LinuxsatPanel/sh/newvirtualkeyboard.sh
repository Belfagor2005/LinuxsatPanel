#!/bin/sh
#DESCRIPTION=newvirtualkeyboard
# Configuration
#########################################
plugin="newvirtualkeyboard"
git_url="https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh"
version=$(wget $git_url/version -qO- | awk 'NR==1')
plugin_path="/usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard"
package="enigma2-plugin-extensions-$plugin"
targz_file="$plugin.tar.gz"
url="$git_url/$targz_file"
temp_dir="/tmp"

# Determine package manager
#########################################
if command -v dpkg &> /dev/null; then
package_manager="apt"
status_file="/var/lib/dpkg/status"
uninstall_command="apt-get purge --auto-remove -y"
else
package_manager="opkg"
status_file="/var/lib/opkg/status"
uninstall_command="opkg remove --force-depends"
fi

#check and_remove package old version
#########################################
check_and_remove_package() {
if [ -d $plugin_path ]; then
echo "> removing package old version please wait..."
sleep 3 
rm -rf $plugin_path > /dev/null 2>&1

if grep -q "$package" "$status_file"; then
echo "> Removing existing $package package, please wait..."
$uninstall_command $package > /dev/null 2>&1
fi
echo "*******************************************"
echo "*             Removed Finished            *"
echo "*******************************************"
sleep 3
exit 1
else
echo " " 
fi  }
check_and_remove_package

#download & install package
#########################################
download_and_install_package() {
echo "> Downloading $plugin-$version package  please wait ..."
cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard/skins/kle /tmp/ >/dev/null 2>&1
rm -rf /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyboard >/dev/null 2>&1
sleep 3
wget --show-progress -qO $temp_dir/$targz_file --no-check-certificate $url
tar -xzf $temp_dir/$targz_file -C / > /dev/null 2>&1
extract=$?
rm -rf $temp_dir/$targz_file >/dev/null 2>&1

if [ $extract -eq 0 ]; then
if [ -f '/tmp/kle' ]; then
	cp -f /tmp/kle/* /usr/lib/enigma2/python/Plugins/SystemPlugins/NewVirtualKeyBoard/skins/kle
fi
cd /tmp 
if [ -d /usr/lib/enigma2/python/Plugins/Extensions/SubsSupport ]; then
	rm -f /usr/lib/enigma2/python/Plugins/Extensions/SubsSupport/subtitles.py > /dev/null 2>&1
	mv subtitles.py /usr/lib/enigma2/python/Plugins/Extensions/SubsSupport  > /dev/null 2>&1
else
rm -f subtitles.py
fi
cd ..
  echo "> $plugin-$version package installed successfully"
  sleep 3
  echo ""
else
  echo "> $plugin-$version package download failed"
  sleep 3
fi  }
download_and_install_package

# Remove unnecessary files and folders
#########################################
print_message() {
echo "> [$(date +'%Y-%m-%d')] $1"
}
cleanup() {
[ -d "/CONTROL" ] && rm -rf /CONTROL >/dev/null 2>&1
rm -rf /control /postinst /preinst /prerm /postrm /tmp/*.ipk /tmp/*.tar.gz >/dev/null 2>&1
print_message "> Uploaded done"
}
cleanup
    