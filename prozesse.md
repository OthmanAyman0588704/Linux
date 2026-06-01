# ⚙️ Prozessverwaltung

Hier lernen wir, wie man laufende Programme überwacht und beendet.

## 📊 Live-Überwachung
Der Befehl `top` (oder das modernere `htop`) zeigt eine Live-Übersicht von CPU und RAM:
```bash
htop
```
*Tipp: Zum Beenden der Ansicht einfach die Taste `Q` drücken.*

## 🛑 Prozesse beenden
Wenn ein Programm hängt, nutzen wir die Prozess-ID (PID) zum Schließen:
```bash
kill <PID>
```
# ⚙️ Prozessverwaltung (Der Linux Task-Manager)

Hier lernen wir, wie man laufende Programme im Hintergrund überwacht und abgestürzte Anwendungen gezielt schließt.

## 📊 Prozesse überwachen
* `top` — Öffnet die Live-Übersicht im Terminal. Sie zeigt an, wie viel CPU und RAM deine Programme gerade verbrauchen.
  * *Tipp: Beende diese Live-Ansicht jederzeit mit der Taste **Q**.*
* `ps aux` — Gibt eine einmalige, riesige Tabelle aller laufenden Programme inklusive ihrer Prozess-ID (PID) aus.

## 🛑 Programme beenden
* `kill <PID>` — Beendet ein abgestürztes Programm mithilfe seiner eindeutigen Prozess-Nummer (PID).
* `pkill <name>` — Schließt eine Anwendung direkt über ihren Programmnamen (z. B. `pkill firefox`).
