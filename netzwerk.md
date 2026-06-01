# 🌐 Netzwerk-Konfiguration

Befehle zur Überprüfung der Internet- und Netzwerkverbindung.

## 🔍 IP-Adresse herausfinden
Um die eigene IP-Adresse im Netzwerk anzuzeigen:
```bash
ip a
```

## ⚡ Verbindung prüfen
Mit `ping` testen wir, ob ein anderer Server (z. B. Google) erreichbar ist:
```bash
ping google.com
```
# 🌐 Netzwerk-Konfiguration

Hier sammeln wir die wichtigsten Befehle, um Verbindungen zu prüfen und Netzwerkschnittstellen zu analysieren.

## 🔍 Befehle für die Netzwerkanalyse
* `ip a` — Zeigt alle Netzwerkgeräte und die dazugehörigen IP-Adressen deines Linux-PCs an.
* `ping <ziel>` — Sendet Testpakete an eine Website oder IP, um die Internetverbindung zu prüfen (z. B. `ping google.com`).
  * *Tipp: Drücke **Strg + C**, um den unendlichen Ping im Terminal zu stoppen!*
* `curl <URL>` — Ruft den rohen Textinhalt einer Webseite direkt im Terminal ab.
