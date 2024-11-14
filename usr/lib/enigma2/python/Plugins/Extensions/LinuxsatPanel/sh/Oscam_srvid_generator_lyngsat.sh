#!/bin/bash
## DESCRIPTION=SRVID-LYNGSAT
HEADER="
######################################################################################
### - the script serves as a generator of the 'oscam.srvid' file for Enigma2
### - based on data parsing from website: https://www.lyngsat.com/packages/XXXXXX.html
### - adapted, $(date '+%Y-%m-%d')
######################################################################################
"
# exec > >(tee -a /tmp/SRVID_LYNGSAT_debug.txt) 2>&1
# set -x

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
    local PACKAGE="$1"
    local CAIDS="$2"
    local PROVIDER="$3"
    local URL="https://www.lyngsat.com/packages/${PACKAGE}.html"
    local TEMP_FILE="/tmp/los_$(date '+%Y%m%d%H%M%S').html"

    if wget -q -O "$TEMP_FILE" "$URL"; then
        echo "URL download successful:  ${URL}"
    else
        echo "URL download FAILED:  ${URL}"
        exit 1
    fi

    local CHN_MATCH='<font face="Arial"><font size='
    local SID_MATCH='<td align="center" bgcolor="#[0-9a-f]+"><font face="Verdana" size=[0-9]+>[0-9 ]+</td>'
    local LIST=$(grep -E -e "$CHN_MATCH" -e "$SID_MATCH" "$TEMP_FILE")
    rm -f "$TEMP_FILE"

    if (( $(echo "$LIST" | grep -c "^") % 2 )); then
        echo -e "ERROR !\nIncomplete SID + CAID list (odd number of lines).\nScript aborted."
        exit 1
    fi

    local RESULT=""
    while IFS= read -r LINE; do
        SID=$(echo "$LINE" | cut -d '>' -f 3 | cut -d '<' -f 1)
        SIDHEX=$(printf "%04X" "$SID")
        IFS= read -r LINE
        CHN=$(echo "$LINE" | grep -oE 'html">.*' | cut -d '>' -f 2 | cut -d '<' -f 1)
        if [ -n "$SIDHEX" ] && [ -n "$CHN" ]; then
            RESULT+="${CAIDS}:${SIDHEX}|${PROVIDER}|${CHN}\n"
        fi
    done <<< "$LIST"

    echo -e "$RESULT" > "/tmp/oscam__${PACKAGE}.srvid"
}

echo "$HEADER"

OSCAM_CFGDIR=$(find_oscam_cfg_dir)
[ -z "$OSCAM_CFGDIR" ] && { echo "WARNING ! Defaulting output directory to '/tmp'."; OSCAM_CFGDIR="/tmp"; }

OSCAM_SRVID="${OSCAM_CFGDIR}/oscam.srvid"

create_srvid_file "Skylink" "0D96,0624" "Skylink"
create_srvid_file "Antik-Sat" "0B00" "AntikSAT"
create_srvid_file "Orange-Slovensko" "0B00,0609" "Orange SK"
create_srvid_file "Sky-Deutschland" "1833,1834,1702,1722,09C4,09AF" "SKY DE"

BACKUP_FILE="/tmp/oscam_-_backup_$(date '+%Y-%m-%d_%H-%M-%S').srvid"
[ -f "$OSCAM_SRVID" ] && { mv "$OSCAM_SRVID" "$BACKUP_FILE"; echo "Backup created at: $BACKUP_FILE"; }

echo "$HEADER" > "$OSCAM_SRVID"
echo -e "### File creation date: $(date '+%Y-%m-%d %H:%M:%S')\n" >> "$OSCAM_SRVID"
cat /tmp/oscam__* >> "$OSCAM_SRVID"
rm -f /tmp/oscam__*

[ -f "$OSCAM_SRVID" ] && echo "Generated 'oscam.srvid' file path:  ${OSCAM_SRVID}"

exit 0



