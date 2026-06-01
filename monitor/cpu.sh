#!/bin/bash
# Modul: CPU-Auslastung
echo "--- CPU Status ---"

# Liest die IDLE-Zeit sauber aus und ersetzt Kommas durch Punkte
CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F',' '{for(i=1;i<=NF;i++) if($i ~ /id/) print $i}' | awk '{print $1}' | sed 's/,/./')

# Falls das Auslesen fehlschlägt, nutzen wir eine alternative Methode
if [ -z "$CPU_IDLE" ]; then
    CPU_IDLE=$(vmstat 1 2 | tail -1 | awk '{print $15}')
fi

# Berechnet die echte Nutzung (100 - Idle)
CPU_USAGE=$(echo "100 - $CPU_IDLE" | bc)
echo "Aktuelle CPU-Auslastung: $CPU_USAGE%"
