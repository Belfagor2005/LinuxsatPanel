#!/bin/bash
#DESCRIPTION=send emm
# mod by lululla 21/02/2025
# Aggiornato il $(date +"%d/%m/%Y")
# bash -x /usr/lib/enigma2/python/Plugins/Extensions/tvManager/data/emm_sender.sh

set -e
# set -x
## Funzione di cleanup
cleanup() {
    rm -f /tmp/*.tmp /tmp/*.html /tmp/emm.txt
}

trap cleanup EXIT

## Constanti
ATR_183E='3F FF 95 00 FF 91 81 71 FE 47 00 54 49 47 45 52 36 30 31 20 52 65 76 4D 38 37 14'
atr_string='aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1U0ZU02RGpW'
SECONDARY_ATR_STRING='aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L2FWaVJ3TjVy'
IP='127.0.0.1'
CAID='183E'

## Trova la directory di configurazione di OSCam
OSCAM_VERSION=$(find /tmp/ -name oscam.version | sed -n 1p)
if [ ! -f "$OSCAM_VERSION" ]; then
    echo "Errore: il file oscam.version non è stato trovato."
    exit 1
fi

OSCAM_CONFIG_DIR=$(grep -ir "ConfigDir" "$OSCAM_VERSION" | awk -F ":      " '{ print $2 }')
if [ ! -d "$OSCAM_CONFIG_DIR" ]; then
    echo "Errore: la directory di configurazione di OSCam non è stata trovata."
    exit 1
fi

OSCAM_CONF="${OSCAM_CONFIG_DIR}/oscam.conf"
LOCAL_EMM_FILE="${OSCAM_CONFIG_DIR}/emm"

## Estrai credenziali e porta HTTP di OSCam
OSCAM_USER=$(grep -ir "httpuser" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
OSCAM_PASSWD=$(grep -ir "httppwd" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
OSCAM_HTTPPORT=$(grep -ir "httpport" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
PROTOCOL=$([[ $OSCAM_HTTPPORT == *"+"* ]] && echo "https" || echo "http")
PORT=$(echo "$OSCAM_HTTPPORT" | sed 's/+//g' | sed 's/^[ \t]*//;s/[ \t]*$//')

## Verifica se curl è installato
if ! command -v curl &>/dev/null; then
    echo "curl non trovato. Tentativo di installazione..."
    if uname -m | grep -qE 'sh4|mips|armv7l'; then
        opkg install curl || { echo "Installazione di curl fallita. Uscita."; exit 1; }
    else
        apt update && apt install -y curl || { echo "Installazione di curl fallita. Uscita."; exit 1; }
    fi
fi

## Scarica l'EMM
emm_url=$(echo "$atr_string" | base64 -d)
REMOTE_EMM_CONTENT=$(curl -s "$emm_url")

if [ -z "$REMOTE_EMM_CONTENT" ]; then
    echo "URL primario fallito. Provo con URL alternativo..."
    emm_url=$(echo "$SECONDARY_ATR_STRING" | base64 -d)
    REMOTE_EMM_CONTENT=$(curl -s "$emm_url")
    if [ -z "$REMOTE_EMM_CONTENT" ]; then
        echo "Entrambi gli URL hanno fallito. Uscita."
        exit 1
    fi
fi

## Salva EMM locale se diverso da remoto
if [ ! -f "$LOCAL_EMM_FILE" ] || ! diff <(echo "$REMOTE_EMM_CONTENT") "$LOCAL_EMM_FILE" >/dev/null; then
    echo "$REMOTE_EMM_CONTENT" > "$LOCAL_EMM_FILE"
fi

## Ottieni i reader attivi
readers=$(curl -s --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth -k "${PROTOCOL}://${IP}:${PORT}/status.html" | grep "Restart Reader")
if [ -z "$readers" ]; then
    echo "Nessun reader attivo trovato."
    exit 1
fi

echo "$readers" | sed -e 's|<TD CLASS="statuscol1"><A HREF="status.html?action=restart&amp;label=||g' | 
    sed 's/^[ \t]*//' | 
    awk -F "\"" '{ print $1 }' > /tmp/active_readers.tmp

## Itera sui reader attivi
while IFS= read -r label; do
    entitlements=$(curl -s --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth -k "${PROTOCOL}://${IP}:${PORT}/entitlements.html?label=${label}")
    atr=$(echo "$entitlements" | sed -n 's/.*<TD COLSPAN="4">\(.*\)<\/TD>.*/\1/p' | sed 's/.$//g')

    atr_cleaned=$(echo "$atr" | tr -d '[:space:]')
    ATR_183E_cleaned=$(echo "$ATR_183E" | tr -d '[:space:]')

    if [ "$ATR_183E_cleaned" == "$atr_cleaned" ]; then
        echo "Invio EMM alla carta $label"
        
        while IFS= read -r EMM; do
            EMM=$(echo "$EMM" | tr -d '\r' | xargs)
            if [[ ${EMM:0:24} == "82708E0000000000D3875411" ]]; then
                curl -s --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth -k \
                    "${PROTOCOL}://${IP}:${PORT}/emm_running.html?label=${label}&emmcaid=${CAID}&ep=${EMM}&action=Launch" >/dev/null
                echo "EMM inviata: ${EMM:0:20}..."  # Mostra solo l'inizio per brevità
            fi
            sleep 1
        done < "$LOCAL_EMM_FILE"

        # Notifica su schermo OSCam
        curl -s "http://${IP}/web/message?text=EMM+inviate+a+${label}&type=2&timeout=5" >/dev/null
    fi
done < /tmp/active_readers.tmp

echo "Aggiornamento EMM completato."
exit 0