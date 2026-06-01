cat << 'EOF' > backup.sh
#!/bin/bash
# Sicheres Backup-Skript im admin-toolkit
SOURCE="$HOME/Linux/admin-toolkit"
TARGET="$HOME/backup_archiv"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

if [ ! -d "$SOURCE" ]; then
    echo "Fehler: Quellordner $SOURCE existiert nicht."
    read -p "Drücke ENTER zum Schließen..."
    exit 1
fi

mkdir -p "$TARGET"
tar -czf "$TARGET/$BACKUP_NAME" -C "$(dirname "$SOURCE")" "$(basename "$SOURCE")"
echo "Backup erfolgreich erstellt: $TARGET/$BACKUP_NAME"
read -p "Fertig! Drücke ENTER zum Schließen..."
EOF
