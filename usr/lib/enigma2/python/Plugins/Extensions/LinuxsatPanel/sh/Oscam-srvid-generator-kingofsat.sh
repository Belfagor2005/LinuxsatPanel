#!/bin/bash
# DESCRIPTION=SRVID-KINGOFSAT
HEADER="
#################################################################################
### - the script serves as a generator of the 'oscam.srvid' file for Enigma2
### - based on data parsing from website: http://en.KingOfSat.net/pack-XXXXXX.php
### - script adapted by <YourName>, $(date '+%Y-%m-%d')
#################################################################################
"
exec > >(tee -a /tmp/SRVID_KINGOFSAT_debug.txt) 2>&1
set -x

find_oscam_cfg_dir() {
    local RET_VAL=""
    local DIR_LIST="/etc /var /usr /config /etc/tuxbox/config /usr/keys"

    for FOLDER in $DIR_LIST; do
        FILEPATH=$(find "${FOLDER}" -iname "oscam.conf" 2>/dev/null | head -n 1)
        [ -f "$FILEPATH" ] && { RET_VAL="${FILEPATH%/*.conf}"; break; }
    done

    if [ -z "$RET_VAL" ]; then
        OSCAM_BIN=$(find /usr/bin /usr/local/bin -iname 'oscam*' 2>/dev/null | head -n 1)
        if [ -z "$OSCAM_BIN" ]; then
            echo -e "ERROR !\nOscam binary file was not found. Unable to locate Oscam configuration directory.\nTerminating script."
            exit 1
        else
            RET_VAL="$($OSCAM_BIN -V 2>/dev/null | grep -i 'configdir' | awk '{print substr($2, 0, length($2)-1)}')"
        fi
    fi

    [ -z "$RET_VAL" ] && echo "WARNING ! Oscam configuration directory not found !"
    echo "$RET_VAL"
}

create_srvid_file() {
    local URL="http://en.kingofsat.net/pack-${1,,}.php"
    local TEMP_FILE="/tmp/kos.html"

    if wget -q -O "$TEMP_FILE" "$URL"; then
        echo "URL download successful:   ${URL}"

        awk -F '>' -v CAIDS="${2}" -v PROVIDER="${1^^}" '
            BEGIN { CHNAME = "invalid" }
            /<i>|class="A3"/ { CHNAME = substr($2, 1, length($2) - 3) }
            /class="s">[0-9]+/ {
                SID = substr($2, 1, length($2) - 4)
                if (CHNAME == "invalid") next
                printf "%s:%04X|%s|%s\n", CAIDS, SID, PROVIDER, CHNAME
                CHNAME = "invalid"
            }' "$TEMP_FILE" > "/tmp/oscam__${1,,}.srvid"

        echo -e "The new file was created:  /tmp/oscam__${1,,}.srvid\n"
        rm -f "$TEMP_FILE"
    else
        echo "URL download failed !!! URL:  ${URL}"
    fi
}

#################################################################################

echo "$HEADER"

OSCAM_CFGDIR=$(find_oscam_cfg_dir)
[ -z "$OSCAM_CFGDIR" ] && { echo "WARNING ! The output directory for the 'oscam.srvid' file was changed to '/tmp' !"; OSCAM_CFGDIR="/tmp"; }

OSCAM_SRVID="${OSCAM_CFGDIR}/oscam.srvid"
create_srvid_file "skylink" "0D96,0624,FFFE"
create_srvid_file "antiksat" "0B00"
create_srvid_file "orangesk" "0B00,0609"
create_srvid_file "upc" "0D02,0D97,0B02,1815"
create_srvid_file "skygermany" "1833,1834,1702,1722,09C4,09AF"
fileSRC="${OSCAM_CFGDIR}/oscam.srvid"
fileDST="/tmp/oscam_-_backup_$(date '+%Y-%m-%d_%H-%M-%S').srvid"
[ -f "$fileSRC" ] && { cp "$fileSRC" "$fileDST"; echo -e "The original file was backed up: ${fileSRC} >>> ${fileDST}\n"; }
echo "$HEADER" > "$OSCAM_SRVID"
echo -e "### File creation date: $(date '+%Y-%m-%d %H:%M:%S')\n" >> "$OSCAM_SRVID"
cat /tmp/oscam__* >> "$OSCAM_SRVID"
rm -f /tmp/oscam__*
[ -f "$OSCAM_SRVID" ] && echo "All generated '.srvid' files have been merged into one and moved to the directory:  ${OSCAM_SRVID}"

exit 0
