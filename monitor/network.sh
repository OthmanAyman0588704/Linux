#!/bin/bash
# Modul: Netzwerk-Überprüfung
echo "--- Netzwerk Status ---"
# Prüft, ob google.com erreichbar ist
if ping -c 1 google.com &>/dev/null; then
    echo "Internetverbindung: OK"
else
    echo "Internetverbindung: FEHLER (Offline)"
fi
