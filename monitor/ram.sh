#!/bin/bash
# Modul: RAM-Auslastung
echo "--- RAM Status ---"
# Zeigt den belegten und freien RAM an
free -h | awk 'NR==2{printf "Genutzt: %s / Gesamt: %s (%.2f%%)\n", $3, $2, $3/$2*100}'
