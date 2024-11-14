#!/bin/bash
# DESCRIPTION=SRVID-SATELINATV
HEADER="
#################################################################################
###     Shell script written by s3n0, 2021-03-02, updated by <YourName>       ###
#################################################################################
###  Shell script to parse data from the web page https://www.satelitnatv.sk  ###
###         and then generate the 'oscam.srvid' file from parsed data         ###
#################################################################################
###  !!! The mentioned web-site www.satelitnatv.sk unfortunately provides !!! ###
###  !!!    only DVB services from Slovakia and the Czech Republic        !!! ###
#################################################################################
"

# exec > >(tee -a /tmp/SRVID_SATELINATV_debug.txt) 2>&1
# set -x

check_command() {
    command -v "$1" >/dev/null 2>&1 || { echo "ERROR: Command '$1' not found. Please install it and re-run the script."; exit 1; }
}

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

create_srvid_file() {
    local URL="$1"
    local PROVIDER="$2"
    local CAIDS="$3"
    
    echo "Downloading data from: ${URL}"
    local TEMP_FILE="/tmp/satelitnatv_$(date '+%Y%m%d%H%M%S').html"
    if ! wget -q -O "$TEMP_FILE" "$URL"; then
        echo "ERROR: Failed to download data from ${URL}"
        exit 1
    fi
    
    sed -i 's/<tr>/\n/g' "$TEMP_FILE"
    local LIST=$(sed -n 's/.*<strong><a href=\/.*\/?id=[0-9]\{4\}\([0-9]*\)>\(.*\)<\/a><\/strong>.*/\1 \2/p' "$TEMP_FILE")

    local FILE_OUTPUT="/tmp/oscam__$(basename "$URL" | tr -d "/").srvid"
    rm -f "$FILE_OUTPUT"

    while IFS= read -r LINE; do
        local SRN=$(echo "$LINE" | cut -d " " -f 2-)
        local SID=$(echo "$LINE" | cut -d " " -f 1 | awk '{print $1 + 0}')
        local SIDHEX=$(printf "%04X" $SID)
        [ -n "$SIDHEX" ] && [ -n "$SRN" ] && echo "${CAIDS}:${SIDHEX}|${PROVIDER}|${SRN}" >> "$FILE_OUTPUT"
    done <<< "$LIST"
    
    rm -f "$TEMP_FILE"
    
    if [ -f "$FILE_OUTPUT" ]; then
        echo "The new file was created: ${FILE_OUTPUT}\n"
    else
        echo "ERROR: File was not created: ${FILE_OUTPUT}"
        echo -e "Function arguments:\n${URL} ${PROVIDER} ${CAIDS}\n"
    fi
}

echo "$HEADER"

check_command wget
check_command sed
check_command awk

OSCAM_CFGDIR=$(find_oscam_cfg_dir)
[ -z "$OSCAM_CFGDIR" ] && { echo "WARNING: The output directory for the 'oscam.srvid' file was changed to '/tmp'!"; OSCAM_CFGDIR="/tmp"; }

OSCAM_SRVID="${OSCAM_CFGDIR}/oscam.srvid"

create_srvid_file "https://www.satelitnatv.sk/frekvencie/skylink-sk-19e/" "Skylink" "0D96,0624,FFFE"
create_srvid_file "https://www.satelitnatv.sk/frekvencie/freesat-sk/" "FreeSAT" "0D97,0653,0B02"
create_srvid_file "https://www.satelitnatv.sk/frekvencie/antik-sat-sk/" "AntikSAT" "0B00"

fileSRC="${OSCAM_SRVID}"
fileDST="/tmp/oscam_-_backup_$(date '+%Y-%m-%d_%H-%M-%S').srvid"
[ -f "$fileSRC" ] && mv "$fileSRC" "$fileDST" && echo "The original file was backed up: ${fileSRC} >>> ${fileDST}"

echo "$HEADER" > "$OSCAM_SRVID"
echo -e "### File creation date: $(date '+%Y-%m-%d %H:%M:%S')\n" >> "$OSCAM_SRVID"
cat /tmp/oscam__* >> "$OSCAM_SRVID"
rm -f /tmp/oscam__*

if [ -f "$OSCAM_SRVID" ]; then
    echo "All generated '.srvid' files have been merged into one and moved to: ${OSCAM_SRVID}"
else
    echo "ERROR: The final '.srvid' file could not be created."
fi

exit 0
