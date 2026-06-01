#!/bin/bash
# Modul: Festplattenbelegung
echo "--- Festplatten Status ---"
# Zeigt die Belegung der Hauptpartition an
df -h / | awk 'NR==2 {print "Belegt: " $5 " | Frei erhältlich: " $4}'
