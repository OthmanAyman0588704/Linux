cat << 'EOF' > usercheck.sh
#!/bin/bash
# Benutzer-Prüfung

if [ -z "$1" ]; then
    echo "Nutzername fehlt! Nutzen Sie: $0 <benutzername>"
    read -p "Drücke ENTER zum Schließen..."
    exit 1
fi

USERNAME=$1

if id "$USERNAME" &>/dev/null; then
    echo "Benutzer '$USERNAME' existiert im System."
else
    echo "Benutzer '$USERNAME' existiert NICHT."
fi

read -p "Fertig! Drücke ENTER zum Schließen..."
EOF

