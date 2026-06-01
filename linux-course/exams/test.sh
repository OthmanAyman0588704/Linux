#!/bin/bash
# Linux-Prüfung: Kleines Quiz
clear
echo "=========================================="
echo "         LINUX-PRÜFUNG: QUIZ              "
echo "=========================================="
echo "Frage 1: Welcher Befehl ändert Dateirechte?"
echo "1) chown"
echo "2) chmod"
echo "3) chmod+x"
echo ""
read -p "Deine Antwort (1, 2 oder 3): " ANTWORT

if [ "$ANTWORT" == "2" ]; then
    echo "RICHTIG! 'chmod' ändert den Modus/Rechte."
else
    echo "FALSCH! Die richtige Antwort wäre 2 (chmod) gewesen."
fi

echo "=========================================="
read -p "Prüfung beendet. Drücke ENTER..."
