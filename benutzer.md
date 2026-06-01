# 👥 Benutzerverwaltung und Rechte

Linux ist ein Mehrbenutzersystem. Hier dokumentieren wir, wie man Rechte verwaltet.

## 🔑 Administrator-Rechte
Wenn man Befehle als Systemadministrator (Root) ausführen muss, stellt man `sudo` voran:
```bash
sudo apt update
```

## 🛡️ Dateiberechtigungen ändern
Mit `chmod` (Change Mode) ändern wir die Rechte einer Datei:
* `chmod +x skript.sh` — Macht eine Datei ausführbar.
