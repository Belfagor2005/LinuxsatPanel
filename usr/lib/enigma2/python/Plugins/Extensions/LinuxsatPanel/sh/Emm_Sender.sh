#!/bin/bash
#DESCRIPTION=send emm
# mod by lululla 24/08/2023
# Aggiornato il $(date +"%d/%m/%Y")

set -e

## Funzione di cleanup
cleanup() {
    rm -f /tmp/*.tmp /tmp/*.html /tmp/emm.txt
}

trap cleanup EXIT

## Constanti
ATR_183E='3F FF 95 00 FF 91 81 71 FE 47 00 54 49 47 45 52 36 30 31 20 52 65 76 4D 38 37 14'
atr_string='aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L0I5N0hDOGll'

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

OSCAM_CONF="${OSCAM_CONFIG_DIR}oscam.conf"
emm_file=$(echo "$atr_string" | base64 -d)

## Estrai credenziali e porta HTTP di OSCam
OSCAM_USER=$(grep -ir "httpuser" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
OSCAM_PASSWD=$(grep -ir "httppwd" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
OSCAM_HTTPPORT=$(grep -ir "httpport" "$OSCAM_CONF" | awk -F "=" '{ print $2 }' | sed 's/^[ \t]*//')
OSCAM_PORT=$(echo "$OSCAM_HTTPPORT" | sed -e 's|+||g')

## Ottieni i reader attivi
readers=$(curl -s --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth -k "http://127.0.0.1:${OSCAM_PORT}/status.html" | grep "Restart Reader")
if [ -z "$readers" ]; then
    echo "Nessun reader attivo trovato."
    exit 1
fi

echo "$readers" | sed -e 's|<TD CLASS="statuscol1"><A HREF="status.html?action=restart&amp;label=||g' | 
    sed 's/^[ \t]*//' | 
    awk -F "\"" '{ print $1 }' > /tmp/active_readers.tmp

## Scarica l'EMM
if ! curl -s -o /tmp/emm.txt "$emm_file"; then
    echo "Errore nel download del file EMM. Uscita."
    exit 1
fi

if [ ! -s /tmp/emm.txt ]; then
    echo "Errore: il file EMM è vuoto o non è stato scaricato correttamente."
    exit 1
fi

## Itera sui reader attivi
while IFS= read -r label; do
    curl -s --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth -k "http://127.0.0.1:${OSCAM_PORT}/entitlements.html?label=${label}" > "/tmp/${label}_entitlements.html"
    atr=$(sed -n 's/.*<TD COLSPAN="4">\(.*\)<\/TD>.*/\1/p' "/tmp/${label}_entitlements.html" | sed 's/.$//g')

    atr_cleaned=$(echo "$atr" | tr -d '[:space:]')
    ATR_183E_cleaned=$(echo "$ATR_183E" | tr -d '[:space:]')

    if [ "$ATR_183E_cleaned" == "$atr_cleaned" ]; then
        echo "Invio nuovi EMM alla carta $label"
        emm=$(cat /tmp/emm.txt)
        response=$(curl -s -k --user "${OSCAM_USER}:${OSCAM_PASSWD}" --anyauth \
            -d "label=${label}" \
            -d "emmcaid=183E" \
            -d "ep=$(< /tmp/emm.txt)" \
            -d "action=Launch" \
            "http://127.0.0.1:${OSCAM_PORT}/emm_running.html")
																																													   
        echo "Risposta del server: $response"
        if [[ $response == *"success"* ]]; then
            echo "EMM inviata con successo alla carta $label."
        else
            echo "Errore nell'invio dell'EMM alla carta $label."
        fi
    fi

    rm -f "/tmp/${label}_entitlements.html"  # Pulizia del file temporaneo
done < /tmp/active_readers.tmp

## Pulizia finale
cleanup

echo "Aggiornamento EMM completato."
exit 0