cat << 'EOF' > lesson01/info.md
# Lektion 1: Fortgeschrittene Navigation und Dateimanipulation

In dieser Lektion lernst du Profi-Werkzeuge für die Shell kennen, um Verzeichnisse effizient zu analysieren und zu filtern.

## 1. Erweiterte Navigation & Pfade
- `cd -`: Springt sofort zurück in das vorherige Verzeichnis (perfekt zum schnellen Hin- und Herwechseln).
- `cd ~`: Wechselt direkt in das Home-Verzeichnis des aktuellen Nutzers.

## 2. Detaillierte Listenansichten (`ls`)
- `ls -la`: Zeigt alle Dateien an, inklusive versteckter Dateien (die mit einem `.` beginnen) und Rechten.
- `ls -lhS`: Listet Dateien sortiert nach Dateigröße auf, lesbar formatiert (z.B. in MB oder GB).
- `ls -lt`: Sortiert die Dateien nach der letzten Änderungszeit (neueste zuerst).

## 3. Suchen und Filtern (Pipes & Wildcards)
- `*`: Ein Wildcard-Platzhalter für beliebig viele Zeichen (z.B. `ls *.sh` zeigt nur Shell-Skripte).
- `?`: Ein Platzhalter für exakt ein einzelnes Zeichen (z.B. `ls lesson0?`).
- `|` (Pipe): Übergibt die Ausgabe eines Befehls als Eingabe an den nächsten Befehl.
- `grep`: Filtert Texte nach Mustern.
  * *Beispiel:* `ls -la | grep "root"` (Zeigt nur Dateien an, die dem Root-Nutzer gehören).

## 4. Echtzeit-Überwachung
- `tail -f /var/log/syslog`: Überwacht System-Logdateien live während des Betriebs.
EOF

