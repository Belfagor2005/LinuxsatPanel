#!/bin/bash
#DESCRIPTION=SRVID-TWOJEIP
HEADER="
#################################################################################
### Script is designed to download and replace the 'oscam.srvid' file.
### The '.srvid' generator is used via the online web page: HTTP://KOS.TWOJEIP.NET
### Script written by s3n0, 2021-02-17: https://github.com/s3n0
#################################################################################
"
exec > >(tee -a /tmp/SRVID_TWOJEIP_debug.txt) 2>&1
set -x

#################################################################################

# Function to find the Oscam configuration directory
find_oscam_cfg_dir() {
    local RET_VAL=""
    local DIR_LIST="/etc /var /usr /config /etc/tuxbox/config /usr/keys"
    
    for FOLDER in $DIR_LIST; do
        FILEPATH=$(find "$FOLDER" -iname "oscam.conf" 2>/dev/null | head -n 1)
        if [ -f "$FILEPATH" ]; then
            RET_VAL="${FILEPATH%/*.conf}"
            break
        fi
    done

    if [ -z "$RET_VAL" ]; then
        OSCAM_BIN=$(find /usr/bin /usr/local/bin -iname 'oscam*' 2>/dev/null | head -n 1)
        if [ -z "$OSCAM_BIN" ]; then
            echo -e "ERROR !\nOscam binary not found. Unable to locate Oscam config directory.\nScript terminating."
            exit 1
        else
            RET_VAL="$($OSCAM_BIN -V 2>/dev/null | grep -i 'configdir' | awk '{print substr($2, 1, length($2)-1)}')"
        fi
    fi

    [ -z "$RET_VAL" ] && echo "WARNING ! Oscam configuration directory not found!"
    echo "$RET_VAL"
}

#################################################################################

echo "$HEADER"

# The URL for the .srvid file, adjust if necessary
URL="http://kos.twojeip.net/download.php?download[]=pack-hdplus&download[]=pack-mtv&download[]=pack-skylink&download[]=pack-austriasat&download[]=pack-orfdigital&download[]=pack-skygermany"

# Find the Oscam configuration directory
OSCAM_CFGDIR=$(find_oscam_cfg_dir)

# Validate that the Oscam configuration directory is found
if [ -z "$OSCAM_CFGDIR" ]; then
    echo "ERROR: Oscam configuration directory not found!"
    exit 1
fi

# Backup the current oscam.srvid file
cp -f "${OSCAM_CFGDIR}/oscam.srvid" "/tmp/oscam.srvid_backup"
echo "Backup of current oscam.srvid created at /tmp/oscam.srvid_backup."

# Start downloading the new oscam.srvid file
echo -e "Downloading file...\n- from: ${URL}\n- to: ${OSCAM_CFGDIR}/oscam.srvid"

# Validate the URL before attempting to download
if wget --spider "${URL}" 2>/dev/null; then
    wget -q -O "${OSCAM_CFGDIR}/oscam.srvid" "${URL}"
    if [ $? -eq 0 ]; then
        echo "...Download completed successfully!"
    else
        echo "...ERROR: Failed to download the file!"
        exit 1
    fi
else
    echo "...ERROR: The online URL ${URL} does not exist!"
    exit 1
fi
exit 0
