#!/bin/bash
# Bereich: Datensicherung (backups)
echo "=== FIRMEN-BACKUP DIENST ==="
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="../backups/firma_backup_$TIMESTAMP.tar.gz"

# Sichert docs und inventory Ordner
tar -czf "$BACKUP_FILE" ../docs ../inventory 2>/dev/null

echo "Firmendaten erfolgreich gesichert in: $BACKUP_FILE"
read -p "Fertig! Drücke ENTER zum Schließen..."
