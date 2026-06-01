#!/bin/bash
# Backup-Skript

SOURCE="./skripte_quelle"
TARGET="./backup_archiv"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

if [ ! -d "$SOURCE" ]; then
    echo "Fehler: Quellordner $SOURCE existiert nicht."
    exit 1
fi

mkdir -p "$TARGET"
tar -czf "$TARGET/$BACKUP_NAME" "$SOURCE"
echo "Backup erfolgreich erstellt: $TARGET/$BACKUP_NAME"

