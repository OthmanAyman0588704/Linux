# 📜 Bash-Skripting & Admin-Toolkit

In diesem Bereich lernen wir, wie man eigene kleine Programme (Skripte) schreibt, um Linux-Systeme automatisch zu verwalten.

---

## 🏗️ Grundlagen: Wie funktioniert ein Bash-Skript?

Jedes Bash-Skript auf einem Linux-System folgt immer diesen drei Schritten:

1. **Der Shebang (`#!/bin/bash`):** Dies muss immer in der **allerersten Zeile** ganz oben stehen. Es verrät Linux, dass es die Befehle mit der Bash-Shell ausführen soll.
2. **Ausführbar machen:** Linux verbietet das Starten neuer Skripte aus Sicherheitsgründen. Du musst im Terminal einmalig die Rechte freischalten:
   `chmod +x mein-skript.sh`
3. **Ausführen:** Gestartet wird das Skript im Terminal immer mit einem `./` vor dem Namen:
   `./mein-skript.sh`

---

## 🛠️ Unsere Admin-Skripte (Code-Sammlung)

Hier sind die fertigen Skripte aus unserer Toolkit-Sammlung. Erstelle jeweils eine neue Datei (z. B. `nano systeminfo.sh`), kopiere den Code hinein und teste ihn.

### 1. System-Informationen (`systeminfo.sh`)
Sammelt die wichtigsten Eckdaten des Linux-Systems auf einen Blick.
```bash
#!/bin/bash
echo "========================================="
echo "       🐧 LINUX SYSTEM-INFORMATIONEN     "
echo "========================================="
echo "Datum & Uhrzeit: \$(date)"
echo "Hostname:        \$(hostname)"
echo "Betriebssystem:  \$(uname -o)"
echo "Kernel-Version:  \$(uname -r)"
echo "-----------------------------------------"
echo "Systemlaufzeit und Auslastung:"
uptime
echo "========================================="
```

### 2. Benutzer-Prüfung (`usercheck.sh`)
Zeigt an, wer aktuell am System angemeldet ist und wie viele Benutzer existieren.
```bash
#!/bin/bash
echo "========================================="
echo "       👥 BENUTZER-ÜBERPRÜFUNG           "
echo "========================================="
echo "Aktuell angemeldete Benutzer:"
who
echo "-----------------------------------------"
echo "Anzahl aller registrierten User im System:"
wc -l /etc/passwd
echo "========================================="
```

### 3. Festplatten-Speicher (`diskspace.sh`)
Überwacht den freien Speicherplatz und listet die größten Ordner auf.
```bash
#!/bin/bash
echo "========================================="
echo "      💾 FESTPLATTEN-ÜBERWACHUNG         "
echo "========================================="
df -h | grep -E '^/dev/|Dateisystem'
echo "-----------------------------------------"
echo "Die 3 größten Ordner in deinem Home-Verzeichnis:"
du -h ~ --max-depth=1 2>/dev/null | sort -hr | head -n 3
echo "========================================="
```

### 4. Automatisches Backup (`backup.sh`)
Erstellt eine komprimierte Sicherung (.tar.gz) des aktuellen Arbeitsordners.
```bash
#!/bin/bash
QUELLE="\$HOME/Schreibtisch/mein-projekt/Linux-wiki"
ZIEL="\$HOME/Sicherungen"
ZEITSTEMPEL=\$(date +%F_%H-%M-%S)
DATEINAME="wiki_backup_\$ZEITSTEMPEL.tar.gz"

echo "========================================="
echo "      📦 AUTOMATISCHES SYSTEM-BACKUP     "
echo "========================================="
mkdir -p "\$ZIEL"
echo "Sichere Ordner: \$QUELLE"
tar -czf "\$ZIEL/\(DATEINAME" "\)QUELLE" 2>/dev/null

if [ \$? -eq 0 ]; then
    echo "✅ BACKUP ERFOLGREICH! Datei: \$DATEINAME"
else
    echo "❌ FEHLER: Backup fehlgeschlagen."
fi
echo "========================================="
```
