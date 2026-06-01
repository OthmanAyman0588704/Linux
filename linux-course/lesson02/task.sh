#!/bin/bash
# Lektion 2: Rechte-Prüfung
echo "=== LEKTION 2: DIE RECHTE-AUFGABE ==="
echo "Aufgabe: Erstelle im Ordner lesson02 eine Datei namens 'geheim.txt'"
echo "und mache sie für jeden lesbar."
echo "--------------------------------------------------"

if [ ! -f "geheim.txt" ]; then
    echo "Status: X - Datei 'geheim.txt' wurde noch nicht erstellt!"
else
    echo "Status: OK - Datei existiert."
    # Prüft, ob die Datei Leserechte hat
    if [ -r "geheim.txt" ]; then
        echo "Ergebnis: PERFEKT! Aufgabe erfolgreich gelöst."
    else
        echo "Ergebnis: Fast! Die Datei braucht noch Leserechte (chmod +r)."
    fi
fi

echo "--------------------------------------------------"
read -p "Drücke ENTER zum Schließen..."
