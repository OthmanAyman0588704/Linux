# 🤖 Bilingual Hybrid-AI Bot – Vollständige Dokumentation & DeepSeek-Coder Integration

Diese Dokumentation beschreibt den vorhandenen Python-Code (`chatbot_v2.py`) im Detail und liefert eine Schritt‑für‑Schritt‑Anleitung, wie Sie **DeepSeek-Coder** (z. B. `deepseek-coder:6.7b`) über Ollama integrieren, damit Ihr Bot Programmieraufgaben übernehmen kann.

---

## 📋 Inhaltsverzeichnis

1. [Überblick und Funktionsweise](#1-überblick-und-funktionsweise)
2. [Detaillierte Code‑Analyse](#2-detaillierte-codeanalyse)
   - [Aufbau und Bibliotheken](#aufbau-und-bibliotheken)
   - [Konfiguration (Config‑Klasse)](#konfiguration-configklasse)
   - [Slang‑Übersetzung & Spracherkennung](#slangübersetzung--spracherkennung)
   - [Systeminformations‑Funktionen](#systeminformationsfunktionen)
   - [Befehlsparser & Hilfefunktionen](#befehlsparser--hilfefunktionen)
   - [Ollama‑Integration](#ollamaintegration)
   - [Haupt‑Bot‑Klasse (HybridBot)](#hauptbotklasse-hybridbot)
3. [Voraussetzungen und Installation](#3-voraussetzungen-und-installation)
4. [DeepSeek‑Coder Integration – Schritt für Schritt](#4-deepseekcoder-integration--schritt-für-schritt)
   - [Schritt 1: Ollama Modell pullen](#schritt-1-ollama-modell-pullen)
   - [Schritt 2: Modell‑Routing einbauen](#schritt-2-modellrouting-einbauen)
   - [Schritt 3: Programmier‑spezifischen System‑Prompt definieren](#schritt-3-programmierspezifischen-systemprompt-definieren)
   - [Schritt 4: (Optional) Code‑Modus als Befehl](#schritt-4-optional-codemodus-als-befehl)
   - [Schritt 5: Code‑Blöcke sauber darstellen](#schritt-5-codeblöcke-sauber-darstellen)
   - [Schritt 6: Vollständig angepasster Code-Auszug](#schritt-6-vollständig-angepasster-code-auszug)
5. [Testen und Fehlerbehandlung](#5-testen-und-fehlerbehandlung)
6. [Fazit & Ausblick](#6-fazit--ausblick)

---

## 1. Überblick und Funktionsweise

Der Bot ist ein **bilingualer, hybrid arbeitender Linux‑Assistent**. Er versteht Deutsch und Englisch, übersetzt automatisch Slang‑Abkürzungen (z. B. `hw` → `how`), erkennt vordefinierte **Systembefehle** (z. B. `ip`, `wetter`, `prozesse`) und führt diese direkt aus. Falls keine Befehlserkennung greift, wird die Anfrage an ein **lokales LLM** (Ollama) weitergeleitet.

**Kernfähigkeiten:**
- Netzwerkinformationen (IP, MAC, DNS)
- Hardware‑Spezifikationen (CPU, RAM, GPU, Kernel)
- Live‑Systemauslastung (CPU‑%, RAM‑%, Festplatte, Netzwerk‑Traffic)
- Prozess‑ und Benutzerlisten
- Docker‑Container, Systemdienste, offene Ports
- Wetterabfrage (Open‑Meteo API)
- Zeit in beliebigen Städten
- Ping, Speedtest, Akkustatus
- Hilfe‑System mit allen Befehlen

Alles andere – von allgemeinen Fragen bis zu Programmierproblemen – wird an ein **Ollama‑Modell** (standardmässig `gemma2:2b`) geschickt.

---

## 2. Detaillierte Code‑Analyse

### Aufbau und Bibliotheken

```python
import sys, os, json, socket, uuid, urllib.request, urllib.parse, subprocess, re, time
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Externe Module (müssen installiert sein)
import psutil          # System‑Metriken
import cpuinfo         # detaillierte CPU‑Infos
import ollama          # Ollama‑Python‑Client
```

### Konfiguration (`Config`‑Klasse)

Zentrale Sammlung aller Einstellungen: Standard‑Ollama‑Modelle, API‑Endpunkte, Pfade, UI‑Texte.

```python
class Config:
    DEFAULT_MODEL: str = "gemma2:2b"
    FALLBACK_MODEL: str = "llama3.2:1b"
    MAX_HISTORY: int = 20
    WEATHER_API_BASE: str = "https://api.open-meteo.com/v1/forecast"
    ...
```

### Slang‑Übersetzung & Spracherkennung

- `translate_slang()` ersetzt bekannte Kurzformen (z. B. `temp` → `temperature`).  
- `detect_language()` zählt typische deutsche/englische Wörter und erkennt Umlaute.

### Systeminformations‑Funktionen

Jede Funktion liefert einen **formatieren String** und akzeptiert einen `lang`‑Parameter (`"de"` / `"en"`). Beispiele:

- `get_network_info()` – lokale IP, MAC, DNS‑Server
- `get_hardware_specs()` – CPU, RAM, Architektur, GPU (via `lspci`)
- `get_system_data()` – Live‑Auslastung (CPU‑%, RAM‑%, Disk‑%, Netzwerk‑Traffic, Temperatur)
- `get_disk_usage()` – alle Partitionen
- `get_battery_info()` – Akkustand und Restzeit
- `get_processes()` – Top‑Prozesse nach CPU
- `get_users()` – eingeloggte Benutzer
- `get_services()` – Status wichtiger Systemdienste (`systemctl`)
- `get_docker_info()` – laufende Container (`docker ps`)
- `get_environment()` – wichtige Umgebungsvariablen
- `get_ports()` – offene Ports (LISTEN)
- `get_ping()`, `get_speedtest()` – Netzwerktests
- `get_weather()` – aktuelle Temperatur/Wind/Luftfeuchte (Open‑Meteo)
- `get_city_time()` – aktuelle Ortszeit mit Zeitzonen‑Support (`ZoneInfo`)

### Befehlsparser & Hilfefunktionen

- `extract_time_city(raw_input)` – extrahiert Stadtnamen aus Sätzen wie `"uhrzeit in Tokio"`.
- `extract_host(raw_input, ...)` – holt Ziel‑Host für `ping`.
- `get_help()` – dynamische Hilfeseite.

### Ollama‑Integration

- `check_ollama_model()` – prüft, ob ein Modell lokal vorhanden ist.
- `get_available_model()` – wählt das beste verfügbare Modell (Haupt‑ → Fallback → erstes gelistetes).
- `ask_ollama(history, user_input, lang)` – baut den **System‑Prompt** (deutsch/englisch) auf, hängt die Historie an und ruft `ollama.chat()` auf.

### Haupt‑Bot‑Klasse (`HybridBot`)

- `__init__`: `self.history` (Chat‑Verlauf), `self.running`
- `print_banner()`: Startbildschirm
- `process_command()`:  
  - Wandelt `cleaned_input` in Kleinbuchstaben.  
  - Prüft auf Schlüsselwörter aus der Slang‑Übersetzung (z. B. `"network_info"`).  
  - Führt bei Treffer die entsprechende Systemfunktion aus und gibt `True` zurück.  
  - Sonst `False` → KI‑Modus.
- `run()`:  
  - Eingabeschleife, Slang‑Übersetzung, Spracherkennung.  
  - Bei Beendigungswörtern (`bye`, `exit`, …) wird abgebrochen.  
  - Wenn `process_command()` `False` liefert → `ask_ollama()` mit Historie.  
  - Antwort wird angezeigt und in Historie gespeichert (Begrenzung via `MAX_HISTORY`).

---

## 3. Voraussetzungen und Installation

**Benötigte Pakete (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

**Python‑Abhängigkeiten:**

```bash
pip install psutil py-cpuinfo ollama
```

**Ollama installieren und starten:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve   # (läuft normalerweise als Dienst)
```

**Ersten Test mit einem kleinen Modell:**

```bash
ollama pull gemma2:2b
```

Dann kann der Bot im aktuellen Zustand gestartet werden:

```bash
python3 chatbot_v2.py
```

---

## 4. DeepSeek‑Coder Integration – Schritt für Schritt

Ziel: Der Bot soll **programmierspezifische Fragen** (Code schreiben, debuggen, erklären) mit einem dafür optimierten Modell beantworten – z. B. **DeepSeek‑Coder** (`deepseek-coder:6.7b`). Alle anderen Anfragen bleiben beim bisherigen Standardmodell.

### Schritt 1: Ollama Modell pullen

DeepSeek‑Coder gibt es in verschiedenen Größen. Für eine gute Balance empfehle ich `deepseek-coder:6.7b` (ca. 3,8 GB) oder `deepseek-coder:1.3b` (ca. 0,8 GB).

```bash
ollama pull deepseek-coder:6.7b
```

Prüfen, ob das Modell verfügbar ist:

```bash
ollama list
```

### Schritt 2: Modell‑Routing einbauen

Wir ergänzen die `ask_ollama()` Funktion um eine **Entscheidung**, welches Modell verwendet wird. Dazu definieren wir eine neue Hilfsfunktion `is_programming_query()`.

**Erweiterung im Code (oberer Bereich, nach den Importen):**

```python
def is_programming_query(text: str) -> bool:
    """Erkennt, ob die Anfrage Programmierkenntnisse erfordert."""
    programming_keywords = [
        "code", "funktion", "klasse", "debug", "fehler", "bug", "programm",
        "skript", "algorithmus", "datenstruktur", "rekurs", "schleife",
        "import", "def ", "class ", "return", "print", "var ", "let ", "const",
        "compile", "runtime", "syntax", "exception", "traceback", "oop",
        "refactor", "test", "unittest", "api", "rest", "json", "xml",
        "html", "css", "javascript", "python", "java", "c++", "go", "rust"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in programming_keywords)
```

Dann innerhalb von `ask_ollama()`:

```python
def ask_ollama(history, user_input, lang="de"):
    # Modellauswahl
    if is_programming_query(user_input):
        model = "deepseek-coder:6.7b"
        # Optional: anderen System‑Prompt für Coder
        if lang == "de":
            system_content = (
                "Du bist ein erfahrener Programmier‑Assistent. "
                "Antworte auf Deutsch mit klaren Code‑Beispielen, "
                "erkläre Fehlerursachen und schlage Lösungen vor. "
                "Verwende ```code-blocks``` für Code."
            )
        else:
            system_content = (
                "You are an expert programming assistant. "
                "Answer in English with clear code examples, "
                "explain errors and suggest fixes. Use ```code blocks```."
            )
    else:
        model = get_available_model()   # bisherige Logik
        # Bisheriger System‑Prompt (wie original)
        if lang == "de":
            system_content = (
                "Du bist ein hilfreicher bilingualer Linux- und Programmier-Assistent. ..."
            )
        else:
            system_content = (
                "You are a helpful bilingual Linux assistant. ..."
            )

    messages = [{"role": "system", "content": system_content}]
    messages.extend(history[-Config.MAX_HISTORY:])
    messages.append({"role": "user", "content": user_input})

    try:
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content']
    except Exception as e:
        return f"❌ KI-Fehler / AI Error: {e}"
```

> **Hinweis:** Das `deepseek-coder:6.7b` Modell muss lokal vorhanden sein. Der Fallback auf `get_available_model()` bleibt für Nicht‑Programmierfragen erhalten.

### Schritt 3: Programmier‑spezifischen System‑Prompt definieren

Im obigen Code sehen Sie bereits, wie der Prompt je nach Modell variiert wird. Für DeepSeek‑Coder ist ein Prompt wichtig, der **Code‑Blöcke** und **detaillierte Erklärungen** fördert. Passen Sie die Texte nach Wunsch an.

### Schritt 4: (Optional) Code‑Modus als Befehl

Falls Sie den Programmiermodus explizit umschalten möchten (z. B. `/code`), erweitern Sie `process_command()`:

```python
# Innerhalb von process_command() – nach den anderen if‑Blöcken
if cleaned_input.lower().startswith("/code"):
    # Umschalten eines Flags self.code_mode = not self.code_mode
    # und eine Bestätigung ausgeben
    ...
```

Dann in `ask_ollama()` das Flag abfragen statt der automatischen Erkennung.

### Schritt 5: Code‑Blöcke sauber darstellen

Das DeepSeek‑Coder Modell liefert oft Antworten mit Markdown‑Code‑Blöcken (```` ```python ... ``` ````). Die Konsole zeigt diese normalerweise unformatiert an. Sie können die Ausgabe durch ein einfaches Reformat verbessern (z. B. Einrückung erkennen), ist aber nicht zwingend nötig.

### Schritt 6: Vollständig angepasster Code‑Auszug

Hier die wichtigsten geänderten Teile der `chatbot_v2.py` – fügen Sie sie ein und passen Sie ggf. die Modellnamen an.

```python
# ... (nach den Importen, vor Config)

def is_programming_query(text: str) -> bool:
    programming_keywords = [
        "code", "funktion", "klasse", "debug", "fehler", "bug", "programm",
        "skript", "algorithmus", "datenstruktur", "rekurs", "schleife",
        "import", "def ", "class ", "return", "print", "var ", "let ", "const",
        "compile", "runtime", "syntax", "exception", "traceback", "oop",
        "refactor", "test", "unittest", "api", "rest", "json", "xml",
        "html", "css", "javascript", "python", "java", "c++", "go", "rust"
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in programming_keywords)

# Dann die modifizierte ask_ollama() Funktion (siehe oben).
# Vergessen Sie nicht, den Parameter 'lang' korrekt zu übergeben.
```

**In der `ask_ollama()` Funktion** müssen Sie außerdem sicherstellen, dass `model` auch dann definiert ist, wenn `is_programming_query()` False ist. Das Original `get_available_model()` liefert ein Modell, das existiert.

**Tipp:** Ersetzen Sie das Standardmodell in `Config` durch ein kleineres allgemeines Modell (z. B. `llama3.2:1b`), damit Ressourcen für DeepSeek‑Coder frei bleiben.

---

## 5. Testen und Fehlerbehandlung

Nach den Änderungen starten Sie den Bot:

```bash
python3 chatbot_v2.py
```

**Testfälle:**

| Eingabe | Erwartung |
|---------|------------|
| `Wie viel RAM habe ich?` | Systembefehl (keine KI) |
| `Schreibe eine Python-Funktion, die Fibonacci berechnet` | Sollte mit DeepSeek‑Coder antworten (erkennbar an qualitativ hochwertigem Code) |
| `Was ist ein Docker-Container?` | Allgemeine Frage → geht ans Standardmodell |
| `Zeige mir einen Ping zu google.com` | Systembefehl |

**Fehlerbehandlung:**

- Modell nicht gefunden: Ollama gibt einen Exception – fangen Sie diese ab und geben Sie eine klare Meldung.
- Zu wenig RAM/VRAM: Wählen Sie ein kleineres Coder‑Modell (`deepseek-coder:1.3b`).
- Falls `ollama.chat()` hängt: Erhöhen Sie Timeout nicht, sondern starten Sie den Ollama‑Dienst neu (`systemctl restart ollama`).

---

## 6. Fazit & Ausblick

Durch die Integration von **DeepSeek‑Coder** wird Ihr Bot zu einem echten **Programmier‑Assistenten** – er kann Code generieren, debuggen und erklären, während er weiterhin alle Systemabfragen beherrscht. Die schrittweise Erweiterung ist dank des modularen Aufbaus einfach umsetzbar.

**Mögliche Erweiterungen:**
- Kontext‑Bewusstsein: Programmierzusammenhänge über mehrere Nachrichten speichern (separater Historie‑Puffer für Code‑Modus).
- Direkte Code‑Ausführung in einer Sandbox (z. B. mit `exec` oder Docker‑Container).
- Unterstützung weiterer Coder‑Modelle (z. B. `codellama`, `mixtral`).

**Viel Erfolg beim Programmieren mit Ihrem neuen Hybrid‑Bot!**
