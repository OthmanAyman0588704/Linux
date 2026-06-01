#!/bin/bash
# Bereich: Benutzerverwaltung (users) - Auflistung
echo "=== AKTUELLE MITARBEITER ==="
echo -e "Name\tAbteilung\tErstellt am"
echo "--------------------------------------------------"

for user_file in users/*.txt; do
    [ -e "$user_file" ] || continue
    NAME=$(grep "Mitarbeiter:" "$user_file" | awk -F': ' '{print $2}')
    ABTEILUNG=$(grep "Abteilung:" "$user_file" | awk -F': ' '{print $2}')
    DATUM=$(grep "Erstellt am:" "$user_file" | awk -F': ' '{print $2}')
    echo -e "$NAME\t$ABTEILUNG\t$DATUM"
done

echo "--------------------------------------------------"
read -p "Fertig! Drücke ENTER zum Schließen..."
