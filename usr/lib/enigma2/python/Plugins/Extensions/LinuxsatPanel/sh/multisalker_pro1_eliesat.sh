#!/bin/sh

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro ]; then
    echo "> removing package please wait..."
    sleep 3s

    rm -rf /usr/lib/enigma2/python/Plugins/Extensions/MultiStalkerPro > /dev/null 2>&1
    rm -rf /etc/enigma2/MultiStalkerPro.json > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerAudioInfo* > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServicePosition* > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Converter/MultiStalkerProServiceResolution* > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerAudioIcon* > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProRunningText* > /dev/null 2>&1
    rm -rf /usr/lib/enigma2/python/Components/Renderer/MultiStalkerProStars* > /dev/null 2>&1

    status='/var/lib/opkg/status'
    package='enigma2-plugin-extensions-multistalkerpro'

    if grep -q $package $status; then
        opkg remove $package > /dev/null 2>&1
    fi

    echo "*******************************************"
    echo "*             Removal Finished            *"
    echo "*            Uploaded By ElieSat          *"
    echo "*******************************************"
    sleep 3s
else
    # Remove unnecessary files and folders
    if [ -d "/CONTROL" ]; then
        rm -r /CONTROL > /dev/null 2>&1
    fi
    rm -rf /control > /dev/null 2>&1
    rm -rf /postinst > /dev/null 2>&1
    rm -rf /preinst > /dev/null 2>&1
    rm -rf /prerm > /dev/null 2>&1
    rm -rf /postrm > /dev/null 2>&1
    rm -rf /tmp/*.ipk > /dev/null 2>&1
    rm -rf /tmp/*.tar.gz > /dev/null 2>&1

    # Check install deps
    # Check python
    status='/var/lib/opkg/status'
    pyt=$(python -c "import sys; print(sys.version_info.major)")

    if [ "$pyt" -eq 3 ]; then
        for pack in enigma2-plugin-systemplugins-serviceapp exteplayer3 libc6 python3-core python3-cryptography; do
            if grep -q $pack $status; then
                rm -rf /run/opkg.lock
                opkg install $pack > /dev/null 2>&1
            fi
        done
    else
        for pack in enigma2-plugin-systemplugins-serviceapp exteplayer3 libc6 python-core python-cryptography; do
            if grep -q $pack $status; then
                rm -rf /run/opkg.lock
                opkg install $pack > /dev/null 2>&1
            fi
        done
    fi

    arch=$(uname -m)
    python=$(python -c "import platform; print(platform.python_version())")

    sleep 1
    if [ "$arch" = "mips" ]; then
        case $python in
            2.7.18)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.0-mips-2.7.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.0-mips-2.7.tar.gz'
                ;;
            3.12.*)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.1-mips-3.12.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.1-mips-3.12.tar.gz'
                ;;
        esac
    elif [ "$arch" = "armv7l" ]; then
        case $python in
            2.7.18)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.0-arm-2.7.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.0-arm-2.7.tar.gz'
                ;;
            3.11.*)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.0-arm-3.11.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.0-arm-3.11.tar.gz'
                ;;
            3.12.*)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.0-arm-3.12.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.0-arm-3.12.tar.gz'
                ;;
        esac
    elif [ "$arch" = "aarch64" ]; then
        case $python in
            3.12.*)
                url='https://gitlab.com/eliesat/extensions/-/raw/main/multistalker-pro/multistalker-pro-1.1-aarch64-3.12.tar.gz'
                package='/var/volatile/tmp/multistalker-pro-1.1-aarch64-3.12.tar.gz'
                ;;
        esac
        rm -rf $proc > /dev/null 2>&1
    fi

    # Config
    plugin=multistalkerpro
    version=1.0

    # Download & install
    echo "> Downloading $plugin-$version package please wait ..."
    sleep 3s

    wget -O $package --no-check-certificate $url
    tar -xzf $package -C /
    extract=$?
    rm -rf $package > /dev/null 2>&1

    echo ''
    if [ $extract -eq 0 ]; then
        echo "> $plugin-$version package installed successfully"
        echo "> Uploaded By ElieSat"
        sleep 3s
    else
        echo "> $plugin-$version package installation failed"
        sleep 3s
    fi
fi

exit
