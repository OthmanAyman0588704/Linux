cat << 'EOF' > diskspace.sh
#!/bin/bash
# Festplatten-Überwachung

LIMIT=80
USAGE=$(df / | grep / | awk '{ print $5 }' | sed 's/%//')

echo "Aktuelle Festplattenbelegung: $USAGE%"

if [ "$USAGE" -gt "$LIMIT" ]; then
    echo "WARNUNG: Speicherplatz kritisch! Über $LIMIT% belegt."
else
    echo "Speicherplatz ist im grünen Bereich."
fi

read -p "Fertig! Drücke ENTER zum Schließen..."
EOF

