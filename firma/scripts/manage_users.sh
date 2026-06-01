#!/bin/bash
# Bereich: Benutzerverwaltung (users)
echo "=== FIRMEN-USER MANAGEMENT ==="
read -p "Name des neuen Mitarbeiters: " NEW_USER

if [ -z "$NEW_USER" ]; then
    echo "Fehler: Kein Name eingegeben."
    read -p "Drücke ENTER zum Schließen..."
    exit 1
fi

# Erstellt die Datei im korrekten Unterordner 'users'
echo "Mitarbeiter: $NEW_USER" > "users/$NEW_USER.txt"
echo "Abteilung: IT-Support" >> "users/$NEW_USER.txt"
echo "Erstellt am: $(date)" >> "users/$NEW_USER.txt"

echo "Mitarbeiter-Akte für '$NEW_USER' wurde erfolgreich angelegt."
read -p "Fertig! Drücke ENTER zum Schließen..."
