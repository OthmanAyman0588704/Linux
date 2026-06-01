#!/bin/bash
# Hauptskript: Ruft alle Module zusammen auf

clear
echo "=========================================="
echo "      DEVOPS MONITORING DASHBOARD         "
echo "=========================================="
echo "Zeitstempel: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# Hier werden die einzelnen Module aufgerufen
bash ./cpu.sh
echo ""
bash ./ram.sh
echo ""
bash ./disk.sh
echo ""
bash ./network.sh

echo "=========================================="
read -p "Fertig! Drücke ENTER zum Schließen..."
