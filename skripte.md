# 📜 Bash-Skripte schreiben

Mit Skripten automatisieren wir Befehlsketten in Linux.

## 🏗️ Aufbau eines Skripts
Jedes Bash-Skript muss in der allerersten Zeile den **Shebang** enthalten:
```bash
#!/bin/bash
echo "Hallo Welt!"
```

## 🏃‍♂️ Ausführen
1. Datei ausführbar machen: `chmod +x mein-skript.sh`
2. Starten mit: `./mein-skript.sh`

# 📜 Bash-Skripte schreiben

Hier dokumentieren wir, wie man Linux-Befehle in einer Datei sammelt und sie automatisch nacheinander ausführen lässt.

## 🏗️ Aufbau eines Skripts
Jedes funktionierende Bash-Skript muss immer dieser Struktur folgen:

1. **Der Shebang in Zeile 1:** `#!/bin/bash` (Sagt Linux, womit das Skript gelesen werden soll).
2. **Der Befehl:** Der eigentliche Code (z. B. `echo "Hallo Welt"`).

## 🏃‍♂️ Wie man ein Skript startet
Damit ein Skript läuft, musst du im Terminal zwei Schritte ausführen:
```bash
chmod +x mein-skript.sh   # 1. Ausführungsrechte freischalten
./mein-skript.sh          # 2. Skript im aktuellen Ordner starten
```
