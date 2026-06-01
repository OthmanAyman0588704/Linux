#!/bin/bash
# Modul: CPU-Auslastung
echo "--- CPU Status ---"

# Liest die IDLE-Zeit sicher aus (sucht nach 'id')
CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | awk -F',' '{for(i=1;i<=NF;i++) if($i ~ /id/) print $i}' | awk '{print $1}' | sed 's/,/./')

# Falls leer, Standardwert setzen um Fehler zu vermeiden
if [ -z "$CPU_IDLE" ]; then CPU_IDLE=100; fi

# Berechnet die Nutzung
CPU_USAGE=$(echo "100 - $CPU_IDLE" | bc)
echo "Aktuelle CPU-Auslastung: $CPU_USAGE%"
