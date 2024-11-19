#!/bin/sh

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro ]; then
	echo "> removing package please wait..."
	sleep 3s 
	
	rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon.* > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars.* > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText.* > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo.* > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition.* > /dev/null 2>&1
	rm -f /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution.* > /dev/null 2>&1
	status='/var/lib/opkg/status'
	package='enigma2-plugin-extensions-multistalkerpro'
	
	if grep -q $package $status; then
		opkg remove $package > /dev/null 2>&1
	fi
	
	echo "*******************************************"
	echo "*             Removed Finished            *"
	echo "*            Uploaded By Eliesat          *"
	echo "*******************************************"
	sleep 3s

else

	#Check and install dependencies
	#check python version
	python=$(python -c "import platform; print(platform.python_version())")
	
	deps=( 
	"enigma2-plugin-systemplugins-serviceapp" "exteplayer3" "gstplayer" 
	"libc6" "libgcc1" "libstdc++6" "python3-core" "python3-cryptography" 
	"python3-dateutil" "python3-fuzzywuzzy" "python3-levenshtein" 
	"python3-pillow" "python3-rarfile" "python3-requests" "python3-six" 
	"python3-sqlite3" "python3-zoneinfo" "uchardet" 
	)
	
	#check python version
	python=$(python -c "import platform; print(platform.python_version())")
	sleep 1;
	case $python in 
		3.9.9)
			deps+=( "libpython3.9-1.0" )
			;;
		3.12.*)
			deps+=( "libpython3.12-1.0" )
			;;
		*)
			echo "> your image python version: $python is not supported"
			sleep 3
			exit 1
			;;
	esac
	
	left=">>>>"
	right="<<<<"
	LINE1="---------------------------------------------------------"
	LINE2="-------------------------------------------------------------------------------------"
	
	if [ -f /etc/opkg/opkg.conf ]; then
		STATUS='/var/lib/opkg/status'
		OSTYPE='Opensource'
		OPKG='opkg update'
		OPKGINSTAL='opkg install'
	elif [ -f /etc/apt/apt.conf ]; then
		STATUS='/var/lib/dpkg/status'
		OSTYPE='DreamOS'
		OPKG='apt-get update'
		APTINSTAL='apt-get install -y'
	fi
	
	install() {
		if ! grep -qs "Package: $1" "$STATUS"; then
			$OPKG >/dev/null 2>&1
			rm -rf /run/opkg.lock
			echo -e "> Need to install ${left} $1 ${right} please wait..."
			echo "$LINE2"
			sleep 0.8
			echo
            if [ "$OSTYPE" = "Opensource" ]; then
                $OPKGINSTAL "$1"
                sleep 1
                clear
            elif [ "$OSTYPE" = "DreamOS" ]; then
                $APTINSTAL "$1"
                sleep 1
                clear
            fi
		fi
	}
	
	for i in "${deps[@]}"; do
		install "$i"
	done
	
	# Configuration
	plugin="multistalker-pro"
	version="1.2"
	targz_file="$plugin-$version.tar.gz"
	temp_dir="/tmp"
	
	# Determine url 
	#check arch armv7l aarch64 mips 7401c0 sh4
	arch=$(uname -m)
	#check python version
	pythonversion=$(python -c "import platform; print(platform.python_version())")
	sleep 3s
	
	if [ "$arch" == "aarch64" ]; then
		case $pythonversion in 
			3.12.*)
				#check image name 
				if [ -f /usr/lib/enigma2/python/Screens/BpBlue.pyc ]; then
					echo ""
					IMAGE=openblackhole
				elif [ -r /usr/lib/enigma2/python/Plugins/SystemPlugins/ViX ]; then
					echo ""
					IMAGE=openvix
				else
					echo ""
				fi
				if [[ "$IMAGE" == "openvix" || "$IMAGE" == "openblackhole" ]]; then
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-aarch64-bv.tar.gz
					sleep 3
				else
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-aarch64-ape.tar.gz
					sleep 3
				fi
				;;
			*)
				echo "> your image python version: $python is not supported"
				sleep 3
				exit 1
				;;
		esac
	
	elif [ "$arch" == "mips" ]; then
		case $pythonversion in 
			3.12.*)
				#check image name 
				if [ -f /usr/lib/enigma2/python/Screens/BpBlue.pyc ]; then
					echo ""
					IMAGE=openblackhole
				elif [ -r /usr/lib/enigma2/python/Plugins/SystemPlugins/ViX ]; then
					echo ""
					IMAGE=openvix
				else
					echo ""
				fi
				if [[ "$IMAGE" == "openvix" || "$IMAGE" == "openblackhole" ]]; then
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-mips-bv.tar.gz
					sleep 3
				else
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-mips-ape.tar.gz
					sleep 3
				fi
				;;
			3.9.9)
				url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.9/multi-stalkerpro-1.2-mips.tar.gz
				;;
			*)
				echo "> your image python version: $python is not supported"
				sleep 3
				exit 1
				;;
		esac
	
	elif [ "$arch" == "armv7l" ]; then
		case $pythonversion in 
			3.12.*)
				#check image name 
				if [ -f /usr/lib/enigma2/python/Screens/BpBlue.pyc ]; then
					echo ""
					IMAGE=openblackhole
				elif [ -r /usr/lib/enigma2/python/Plugins/SystemPlugins/ViX ]; then
					echo ""
					IMAGE=openvix
				else
					echo ""
				fi
				if [[ "$IMAGE" == "openvix" || "$IMAGE" == "openblackhole" ]]; then
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-arm-bv.tar.gz
					sleep 3
				else
					url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.12/multi-stalkerpro-1.2-arm-ape.tar.gz
					sleep 3
				fi
				;;
			3.9.9)
				url=https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/py3.9/multi-stalkerpro-1.2-arm.tar.gz
				;;
			*)
				echo "> your image python version: $python is not supported"
				sleep 3
				exit 1
				;;
		esac
	fi
	
	#Download & install package
	echo "> Downloading $plugin-$version package  please wait ..."
	sleep 3
	wget --show-progress -qO $temp_dir/$targz_file --no-check-certificate $url
	set -e
	if [ -e /etc/enigma2/MultiStalkerPro.json ]; then
		mv -f /etc/enigma2/MultiStalkerPro.json /tmp
	fi
	tar -xzf $temp_dir/$targz_file -C /
	extract=$?
	rm -rf $temp_dir/$targz_file >/dev/null 2>&1
	
	echo ''
	if [ $extract -eq 0 ]; then
		set -e
		if [ -e /tmp/MultiStalkerPro.json ]; then
			rm -f /etc/enigma2/MultiStalkerPro.json
			mv -f /tmp/MultiStalkerPro.json /etc/enigma2/MultiStalkerPro.json
			rm -f /tmp/MultiStalkerPro.json
		fi
		echo "> $plugin-$version package installed successfully"
		sleep 3
		echo "> Uploaded By ElieSat"
		else
		echo "> $plugin-$version package installation failed"
		sleep 3
	fi
	
fi