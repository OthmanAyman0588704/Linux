
# ======================= SELBST-INSTALLATION =======================
def install_python_package(package_name):
    import subprocess, sys
    print(f"⚠️  Benötige Python-Paket '{package_name}'")
    if input("Darf ich es installieren? (y/n): ").lower() != 'y':
        return False
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        print(f"✅ {package_name} installiert.")
        return True
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False

def install_system_package(package_name):
    import subprocess
    print(f"📦 Systempaket '{package_name}' wird benötigt.")
    if input(f"Mit 'sudo apt install {package_name}' installieren? (y/n): ").lower() != 'y':
        return False
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
        print(f"✅ {package_name} installiert.")
        return True
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return False
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🤖 BILINGUAL HYBRID-AI & NET/HARDWARE BOT v2.0                              ║
║  Ein erweiterter, modularer Linux-Assistent mit Ollama-Integration           ║
║  Unterstützt Deutsch & Englisch, Slang-Übersetzung, Live-Monitoring          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# 1. STANDARD-BIBLIOTHEKEN (Python Built-ins)
# ══════════════════════════════════════════════════════════════════════════════
import sys          # System-spezifische Parameter und Funktionen (z.B. exit)
import os           # Betriebssystem-Interaktion (z.B. Dateien lesen, uname)
import json         # JSON-Parsing für API-Antworten (Wetter, Ollama)
import socket       # Netzwerk-Sockets für IP-Ermittlung
import uuid         # UUID-Generierung für MAC-Adresse aus Node-ID
import urllib.request   # HTTP-Anfragen ohne externe Abhängigkeiten
import urllib.parse     # URL-Encoding für Städtenamen mit Umlauten/Leerzeichen
import subprocess   # Ausführen von Shell-Befehlen (neu: erweiterte Systeminfos)
import re           # Reguläre Ausdrücke für Textverarbeitung
import time         # Zeitfunktionen für Delays und Messungen
from datetime import datetime  # Aktuelle Uhrzeit und Datum formatieren
from zoneinfo import ZoneInfo  #Akutelle Uhrzeit und Datum der Zeitzone
from pathlib import Path       # Moderner Dateipfad-Umgang (Python 3.4+)
from typing import Dict, List, Optional, Tuple, Any  # Type Hints für bessere Code-Klarheit

# ══════════════════════════════════════════════════════════════════════════════
# 2. EXTERNE ABHÄNGIGKEITEN (müssen via pip installiert werden)
# ══════════════════════════════════════════════════════════════════════════════

try:
    import psutil     # System- und Prozess-Utilitäten (CPU, RAM, Disk, Netzwerk)
except ImportError:
    print("❌ Fehler: 'psutil' nicht gefunden. Bitte installiere: pip install psutil")
    sys.exit(1)

try:
    import cpuinfo    # Detaillierte CPU-Informationen (Brand, Cores, Flags)
except ImportError:
    print("❌ Fehler: 'py-cpuinfo' nicht gefunden. Bitte installiere: pip install py-cpuinfo")
    sys.exit(1)

try:
    import ollama     # Python-Client für lokale Ollama-LLM-API
except ImportError:
    print("❌ Fehler: 'ollama' nicht gefunden. Bitte installiere: pip install ollama")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# 3. KONFIGURATION & KONSTANTEN
# ══════════════════════════════════════════════════════════════════════════════

class Config:
    """
    Zentrale Konfigurationsklasse.
    Alle einstellbaren Parameter an einem Ort – leicht anpassbar ohne
    im Code herumzuwühlen.
    """
    # --- LLM-Einstellungen ---
    DEFAULT_MODEL: str = "gemma2:2b"      # Standard-Ollama-Modell
    FALLBACK_MODEL: str = "llama3.2:1b"   # Fallback wenn Hauptmodell nicht verfügbar
    MAX_HISTORY: int = 20                  # Maximale Chat-Historie (RAM-Schutz)

    # --- Wetter-API ---
    WEATHER_API_BASE: str = "https://api.open-meteo.com/v1/forecast"
    GEO_API_BASE: str = "https://geocoding-api.open-meteo.com/v1/search"
    DEFAULT_CITY: str = "Berlin"

    # --- Netzwerk ---
    DNS_TEST_HOST: str = "8.8.8.8"         # Google DNS für IP-Ermittlung
    DNS_TEST_PORT: int = 80
    DNS_RESOLV_PATH: str = "/etc/resolv.conf"

    # --- Sprache ---
    DEFAULT_LANG: str = "de"

    # --- UI ---
    BOT_PREFIX: str = "🤖 Bot"
    THINKING_MSG: str = "🧠 Denke nach..."


# ══════════════════════════════════════════════════════════════════════════════
# 4. SLANG-ÜBERSETZUNG & SPRACHERKENNUNG
# ══════════════════════════════════════════════════════════════════════════════

SLANG_TRANSLATION: Dict[str, str] = {
    # Englischer Internet-Slang
    "hw": "how", "rn": "now", "pls": "please", "thx": "thanks",
    "idk": "i dont know", "brb": "be right back", "asap": "as soon as possible",
    "btw": "by the way", "imo": "in my opinion", "fyi": "for your information",
    "lol": "laughing out loud", "omg": "oh my god", "wtf": "what the fuck",
    "tbh": "to be honest", "np": "no problem", "gl": "good luck",

    # Deutscher Internet-Slang / Jugendsprache
    "wv": "wieviel", "vllt": "vielleicht", "kb": "keinen bock",
    "kA": "keine ahnung", "ngl": "nicht gelogen", "omg": "oh mein gott",
    "lol": "lache laut", "wtf": "was zum fick", "afaik": "soweit ich weiß",
    "imo": "meiner meinung nach", "btw": "übrigens",

    # Technische Abkürzungen → interne Befehlsschlüssel
    "ip": "network_info", "mac": "network_info", "dns": "network_info",
    "uhrzeit": "time_info", "uhr": "time_info", "zeit": "time_info",
    "clock": "time_info", "spät": "time_info", "spaet": "time_info",
    "temp": "temperature", "temperatur": "temperature",
    "traffic": "network_traffic", "netzwerk": "network_info",
    "internet": "network_info", "speicher": "system_data",
    "festplatte": "system_data", "disk": "system_data",
    "monitoring": "system_data", "auslastung": "system_data",
    "hardware": "hardware_specs", "specs": "hardware_specs",
    "komponenten": "hardware_specs", "teile": "hardware_specs",
    "geraete": "hardware_specs", "geräte": "hardware_specs",
    "systeminfo": "hardware_specs", "prozesse": "processes",
    "prozesse": "processes", "top": "processes", "tasks": "processes",
    "battery": "battery", "akku": "battery", "laufzeit": "battery",
    "users": "users", "benutzer": "users", "who": "users",
    "docker": "docker", "container": "docker",
    "services": "services", "dienste": "services", "systemctl": "services",
    "update": "update", "upgrade": "update", "aktualisieren": "update",
    "ping": "ping", "speedtest": "speedtest", "geschwindigkeit": "speedtest",
    "disk_usage": "disk_usage", "partitionen": "disk_usage",
    "ports": "ports", "offene ports": "ports", "listening": "ports",
    "env": "environment", "umgebung": "environment", "variablen": "environment",
    "help": "help", "hilfe": "help", "?": "help",
    "joke": "joke", "witz": "joke", "spaß": "joke",
    "fact": "fact", "fakt": "fact", "trivia": "fact",
}


def translate_slang(text: str) -> str:
    """
    Ersetzt bekannte Slang-Begriffe durch ihre vollständigen Entsprechungen.

    Args:
        text: Rohe Benutzereingabe

    Returns:
        Bereinigter Text mit expandierten Abkürzungen

    Beispiel:
        "hw ist die temp rn" → "how ist die temperature now"
    """
    words = text.split()
    translated = []
    for word in words:
        # Entferne Satzzeichen für Lookup, behalte sie aber im Output
        clean = word.lower().strip(".,;:!?")
        replacement = SLANG_TRANSLATION.get(clean, clean)
        # Falls das Wort ersetzt wurde und Großbuchstaben hatte, beibehalten
        if replacement != clean:
            translated.append(replacement)
        else:
            translated.append(word)
    return " ".join(translated)


def detect_language(text: str) -> str:
    """
    Erkennt die Sprache der Benutzereingabe (de oder en).

    Strategie:
    1. Prüfe auf typisch deutsche Wörter/Wortteile
    2. Prüfe auf typisch englische Wörter
    3. Fallback: Deutsch (da primärer Nutzerkreis)

    Args:
        text: Benutzereingabe

    Returns:
        "de" oder "en"
    """
    text_lower = text.lower()

    # Typisch deutsche Schlüsselwörter (stark gewichtet)
    german_markers = [
        "wetter", "uhrzeit", "uhr", "zeit", "spät", "spaet", "wie", "was",
        "wer", "wo", "wann", "warum", "wie viel", "wieviel", "und", "oder",
        "aber", "weil", "dass", "bitte", "danke", "tschüss", "ciao", "hallo",
        "guten", "morgen", "tag", "abend", "nacht", "netzwerk", "hardware",
        "komponenten", "geräte", "geraete", "speicher", "festplatte", "auslastung",
        "temperatur", "prozesse", "benutzer", "dienste", "aktualisieren",
        "hilfe", "witz", "fakt", "akku", "laufzeit", "partitionen", "geschwindigkeit"
    ]

    # Typisch englische Schlüsselwörter
    english_markers = [
        "weather", "time", "clock", "how", "what", "who", "where", "when",
        "why", "and", "or", "but", "because", "that", "please", "thanks",
        "bye", "exit", "quit", "hello", "hi", "good", "morning", "evening",
        "night", "network", "hardware", "specs", "ram", "cpu", "gpu", "disk",
        "space", "traffic", "temp", "temperature", "processes", "users",
        "services", "update", "upgrade", "help", "joke", "fact", "battery",
        "partitions", "speed", "environment", "variables"
    ]

    german_score = sum(1 for marker in german_markers if marker in text_lower)
    english_score = sum(1 for marker in english_markers if marker in text_lower)

    # Deutsche Umlaute sind ein starker Indikator
    if any(char in text_lower for char in "äöüß"):
        german_score += 3

    return "de" if german_score >= english_score else "en"


# ══════════════════════════════════════════════════════════════════════════════
# 5. SYSTEM-INFORMATIONS-FUNKTIONEN (Hardware, Netzwerk, etc.)
# ══════════════════════════════════════════════════════════════════════════════

def get_network_info(lang: str = "de") -> str:
    """
    Ermittelt Netzwerk-Informationen: Lokale IP, MAC, DNS-Server.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Netzwerkdaten
    """
    # Lokale IP über externen DNS-Server ermitteln (funktioniert auch ohne Internet)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            s.connect((Config.DNS_TEST_HOST, Config.DNS_TEST_PORT))
            local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1 (Fallback)"

    # MAC-Adresse aus der UUID-Node-ID extrahieren
    mac = ':'.join(
        ['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
         for ele in range(0, 8 * 6, 8)][::-1]
    )

    # DNS-Server aus /etc/resolv.conf auslesen
    dns_servers: List[str] = []
    try:
        resolv_path = Path(Config.DNS_RESOLV_PATH)
        if resolv_path.exists():
            with resolv_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("nameserver"):
                        parts = line.split()
                        if len(parts) > 1:
                            dns_servers.append(parts[1])
    except Exception:
        pass

    dns_str = ", ".join(dns_servers) if dns_servers else (
        "Standard-DNS / Default DNS"
    )

    # Wichtige Test-IPs für Netzwerkdiagnose
    test_ips = (
        "• Google Public DNS: 8.8.8.8 / 8.8.4.4\n"
        "• Cloudflare DNS: 1.1.1.1 / 1.0.0.1\n"
        "• Quad9 (Security): 9.9.9.9\n"
        "• OpenDNS: 208.67.222.222"
    )

    if lang == "de":
        return (
            f"🌐 **Netzwerk-Informationen:**\n"
            f"• Lokale IP-Adresse: `{local_ip}`\n"
            f"• MAC-Adresse: `{mac}`\n"
            f"• Aktuelle DNS-Server: `{dns_str}`\n\n"
            f"🎯 **Wichtige Test-IPs (für Ping / DNS):**\n" + test_ips
        )
    else:
        return (
            f"🌐 **Network Information:**\n"
            f"• Local IP Address: `{local_ip}`\n"
            f"• MAC Address: `{mac}`\n"
            f"• Current DNS Servers: `{dns_str}`\n\n"
            f"🎯 **Important Test IPs (for Ping / DNS):**\n" + test_ips
        )


def get_hardware_specs(lang: str = "de") -> str:
    """
    Ermittelt detaillierte Hardware-Spezifikationen.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit CPU, RAM, Architektur, Kernel
    """
    try:
        cpu_info = cpuinfo.get_cpu_info()
        cpu_name = cpu_info.get('brand_raw', 'Unbekannt / Unknown')
        cpu_cores = cpu_info.get('count', psutil.cpu_count())
        cpu_freq = cpu_info.get('hz_advertised_friendly', 'N/A')
    except Exception:
        cpu_name = "Unbekannte CPU / Unknown CPU"
        cpu_cores = psutil.cpu_count()
        cpu_freq = "N/A"

    ram_total_gb = psutil.virtual_memory().total // (1024 ** 3)

    try:
        os_info = os.uname()
        kernel = os_info.release
        arch = os_info.machine
        platform_name = os_info.sysname
        hostname = os_info.nodename
    except Exception:
        kernel = "Unbekannt"
        arch = "Unbekannt"
        platform_name = "Linux"
        hostname = "localhost"

    # GPU-Info via lspci (falls verfügbar)
    gpu_info = "Nicht erkannt / Not detected"
    try:
        result = subprocess.run(
            ["lspci"], capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split("\n"):
            if "VGA" in line or "3D" in line or "Display" in line:
                gpu_info = line.split(":", 2)[-1].strip()
                break
    except Exception:
        pass

    if lang == "de":
        return (
            f"🔌 **Hardware-Komponenten & OS:**\n"
            f"• Prozessor (CPU): `{cpu_name}`\n"
            f"• CPU-Kerne: `{cpu_cores}`\n"
            f"• CPU-Takt: `{cpu_freq}`\n"
            f"• Architektur: `{arch}`\n"
            f"• Arbeitsspeicher (RAM): `{ram_total_gb} GB` Gesamt\n"
            f"• Grafikkarte (GPU): `{gpu_info}`\n"
            f"• Linux-Kernel: `{kernel}`\n"
            f"• Plattform: `{platform_name}`\n"
            f"• Hostname: `{hostname}`"
        )
    else:
        return (
            f"🔌 **Hardware Components & OS:**\n"
            f"• Processor (CPU): `{cpu_name}`\n"
            f"• CPU Cores: `{cpu_cores}`\n"
            f"• CPU Frequency: `{cpu_freq}`\n"
            f"• Architecture: `{arch}`\n"
            f"• Total RAM: `{ram_total_gb} GB`\n"
            f"• Graphics Card (GPU): `{gpu_info}`\n"
            f"• Linux Kernel: `{kernel}`\n"
            f"• Platform: `{platform_name}`\n"
            f"• Hostname: `{hostname}`"
        )


def get_system_data(lang: str = "de") -> str:
    """
    Ermittelt Live-System-Metriken: CPU, RAM, Disk, Netzwerk-Traffic.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit aktuellen Auslastungsdaten
    """
    cpu_usage = psutil.cpu_percent(interval=0.5)
    cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)

    ram = psutil.virtual_memory()
    ram_used_mb = ram.used // (1024 ** 2)
    ram_total_mb = ram.total // (1024 ** 2)
    ram_free_mb = ram.free // (1024 ** 2)

    disk = psutil.disk_usage('/')
    disk_total_gb = disk.total // (1024 ** 3)
    disk_used_gb = disk.used // (1024 ** 3)
    disk_free_gb = disk.free // (1024 ** 3)

    network = psutil.net_io_counters()
    mb_sent = network.bytes_sent / (1024 ** 2)
    mb_recv = network.bytes_recv / (1024 ** 2)

    # CPU-Temperatur (falls verfügbar via psutil)
    temps = "N/A"
    try:
        temp_data = psutil.sensors_temperatures()
        if temp_data:
            for name, entries in temp_data.items():
                if entries:
                    temps = f"{entries[0].current}°C ({name})"
                    break
    except Exception:
        pass

    if lang == "de":
        return (
            f"🖥️ **Live-System-Auslastung:**\n"
            f"• CPU Gesamt: `{cpu_usage}%`\n"
            f"• Pro Kern: `{', '.join(f'{c}%' for c in cpu_per_core)}`\n"
            f"• CPU-Temperatur: `{temps}`\n"
            f"• RAM: `{ram.percent}%` belegt\n"
            f"  └─ Genutzt: `{ram_used_mb} MB` / `{ram_total_mb} MB`\n"
            f"  └─ Frei: `{ram_free_mb} MB`\n"
            f"• Festplatte (/): `{disk.percent}%` belegt\n"
            f"  └─ Genutzt: `{disk_used_gb} GB` / `{disk_total_gb} GB`\n"
            f"  └─ Frei: `{disk_free_gb} GB`\n"
            f"• Netzwerktraffic:\n"
            f"  └─ Gesendet: `{mb_sent:.2f} MB`\n"
            f"  └─ Empfangen: `{mb_recv:.2f} MB`"
        )
    else:
        return (
            f"🖥️ **Live System Metrics:**\n"
            f"• CPU Total: `{cpu_usage}%`\n"
            f"• Per Core: `{', '.join(f'{c}%' for c in cpu_per_core)}`\n"
            f"• CPU Temperature: `{temps}`\n"
            f"• RAM: `{ram.percent}%` used\n"
            f"  └─ Used: `{ram_used_mb} MB` / `{ram_total_mb} MB`\n"
            f"  └─ Free: `{ram_free_mb} MB`\n"
            f"• Disk (/): `{disk.percent}%` used\n"
            f"  └─ Used: `{disk_used_gb} GB` / `{disk_total_gb} GB`\n"
            f"  └─ Free: `{disk_free_gb} GB`\n"
            f"• Network Traffic:\n"
            f"  └─ Sent: `{mb_sent:.2f} MB`\n"
            f"  └─ Received: `{mb_recv:.2f} MB`"
        )


def get_disk_usage(lang: str = "de") -> str:
    """
    Zeigt detaillierte Festplatten-Nutzung aller Partitionen.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit allen Partitionen
    """
    partitions = psutil.disk_partitions()
    lines = []

    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = usage.total // (1024 ** 3)
            used_gb = usage.used // (1024 ** 3)
            free_gb = usage.free // (1024 ** 3)
            percent = usage.percent
            lines.append(
                f"  📁 `{part.mountpoint}` ({part.fstype})\n"
                f"     └─ `{used_gb} GB` / `{total_gb} GB` (`{percent}%` belegt)"
            )
        except PermissionError:
            lines.append(f"  📁 `{part.mountpoint}` ─ Zugriff verweigert / Permission denied")

    header = "💾 **Festplatten-Nutzung:**" if lang == "de" else "💾 **Disk Usage:**"
    return header + "\n" + "\n".join(lines) if lines else (
        header + "\n  Keine Partitionen gefunden / No partitions found"
    )


def get_battery_info(lang: str = "de") -> str:
    """
    Ermittelt Akku-Status (nur bei Laptops / Tablets).

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Akku-Informationen
    """
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return (
                "🔋 Kein Akku erkannt (Desktop-PC?).\n"
                "🔋 No battery detected (Desktop PC?)."
            )

        percent = battery.percent
        plugged = "⚡ Am Strom" if battery.power_plugged else "🔋 Akkubetrieb"

        if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left = "Unbegrenzt / Unlimited"
        elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            time_left = "Unbekannt / Unknown"
        else:
            hours = battery.secsleft // 3600
            mins = (battery.secsleft % 3600) // 60
            time_left = f"{hours}h {mins}m"

        if lang == "de":
            return (
                f"🔋 **Akku-Status:**\n"
                f"• Ladestand: `{percent}%`\n"
                f"• Status: `{plugged}`\n"
                f"• Verbleibende Zeit: `{time_left}`"
            )
        else:
            return (
                f"🔋 **Battery Status:**\n"
                f"• Charge Level: `{percent}%`\n"
                f"• Status: `{plugged}`\n"
                f"• Time Remaining: `{time_left}`"
            )
    except Exception as e:
        return f"🔋 Fehler / Error: {e}"


def get_processes(lang: str = "de", limit: int = 10) -> str:
    """
    Zeigt die Top-Prozesse nach CPU-Auslastung.

    Args:
        lang: "de" oder "en"
        limit: Anzahl der angezeigten Prozesse

    Returns:
        Formatierter String mit Prozessliste
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sortiere nach CPU-Auslastung (absteigend)
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        top = processes[:limit]

        lines = []
        for i, p in enumerate(top, 1):
            lines.append(
                f"  {i}. `{p['name']}` (PID: {p['pid']}) ─ "
                f"CPU: {p['cpu_percent'] or 0:.1f}%, RAM: {p['memory_percent'] or 0:.1f}%"
            )

        header = f"⚙️ **Top {limit} Prozesse (nach CPU):**" if lang == "de" else f"⚙️ **Top {limit} Processes (by CPU):**"
        return header + "\n" + "\n".join(lines)
    except Exception as e:
        return f"⚙️ Fehler / Error: {e}"


def get_users(lang: str = "de") -> str:
    """
    Zeigt aktuell eingeloggte Benutzer.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Benutzerliste
    """
    try:
        users = psutil.users()
        if not users:
            return "👤 Keine Benutzer eingeloggt / No users logged in"

        lines = []
        for u in users:
            lines.append(
                f"  • `{u.name}` ─ Terminal: `{u.terminal}` ─ "
                f"Seit: {datetime.fromtimestamp(u.started).strftime('%H:%M:%S')}"
            )

        header = "👤 **Eingeloggte Benutzer:**" if lang == "de" else "👤 **Logged-in Users:**"
        return header + "\n" + "\n".join(lines)
    except Exception as e:
        return f"👤 Fehler / Error: {e}"


def get_services(lang: str = "de") -> str:
    """
    Zeigt den Status wichtiger Systemdienste.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Dienst-Status
    """
    important_services = [
        "ssh", "cron", "docker", "nginx", "apache2", "mysql", "postgresql",
        " NetworkManager", "systemd-resolved", "bluetooth", "cups"
    ]

    lines = []
    for service in important_services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True, text=True, timeout=3
            )
            status = result.stdout.strip()
            icon = "🟢" if status == "active" else "🔴"
            lines.append(f"  {icon} `{service}` ─ `{status}`")
        except Exception:
            lines.append(f"  ⚪ `{service}` ─ `unbekannt / unknown`")

    header = "🔧 **Wichtige Dienste:**" if lang == "de" else "🔧 **Important Services:**"
    return header + "\n" + "\n".join(lines)


def get_docker_info(lang: str = "de") -> str:
    """
    Zeigt laufende Docker-Container (falls Docker installiert).

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Container-Infos
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}|{{.Image}}|{{.Status}}"],
            capture_output=True, text=True, timeout=5
        )

        if result.returncode != 0:
            return (
                "🐳 Docker nicht verfügbar oder nicht installiert.\n"
                "🐳 Docker not available or not installed."
            )

        containers = result.stdout.strip().split("\n")
        if not containers or containers == ['']:
            return (
                "🐳 Keine laufenden Docker-Container.\n"
                "🐳 No running Docker containers."
            )

        lines = []
        for container in containers:
            parts = container.split("|")
            if len(parts) >= 3:
                lines.append(f"  • `{parts[0]}` ─ Image: `{parts[1]}` ─ Status: `{parts[2]}`")

        header = "🐳 **Docker-Container:**" if lang == "de" else "🐳 **Docker Containers:**"
        return header + "\n" + "\n".join(lines)
    except FileNotFoundError:
        return (
            "🐳 Docker ist nicht installiert.\n"
            "🐳 Docker is not installed."
        )
    except Exception as e:
        return f"🐳 Fehler / Error: {e}"


def get_environment(lang: str = "de") -> str:
    """
    Zeigt wichtige Umgebungsvariablen.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Umgebungsvariablen
    """
    important_vars = [
        "PATH", "HOME", "USER", "SHELL", "LANG", "TERM",
        "DISPLAY", "XDG_SESSION_TYPE", "EDITOR", "PYTHONPATH"
    ]

    lines = []
    for var in important_vars:
        value = os.environ.get(var, "nicht gesetzt / not set")
        lines.append(f"  • `{var}` = `{value}`")

    header = "🌍 **Umgebungsvariablen:**" if lang == "de" else "🌍 **Environment Variables:**"
    return header + "\n" + "\n".join(lines)


def get_ports(lang: str = "de") -> str:
    """
    Zeigt alle offenen Ports und lauschende Prozesse.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Port-Informationen
    """
    try:
        connections = psutil.net_connections(kind='inet')
        listening = [c for c in connections if c.status == 'LISTEN']

        if not listening:
            return (
                "🔌 Keine lauschenden Ports gefunden.\n"
                "🔌 No listening ports found."
            )

        lines = []
        seen = set()
        for conn in listening:
            if conn.laddr:
                key = (conn.laddr.port, conn.pid)
                if key not in seen:
                    seen.add(key)
                    proc_name = "unknown"
                    try:
                        proc = psutil.Process(conn.pid)
                        proc_name = proc.name()
                    except Exception:
                        pass
                    lines.append(
                        f"  • Port `{conn.laddr.port}` ─ Prozess: `{proc_name}` (PID: {conn.pid})"
                    )

        header = "🔌 **Offene Ports (LISTEN):**" if lang == "de" else "🔌 **Open Ports (LISTEN):**"
        return header + "\n" + "\n".join(lines[:20])  # Max 20 Einträge
    except Exception as e:
        return f"🔌 Fehler / Error: {e}"


def get_ping(host: str = "google.com", lang: str = "de") -> str:
    """
    Führt einen Ping-Test zu einem Host durch.

    Args:
        host: Ziel-Host für den Ping
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Ping-Ergebnis
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "3", "-W", "2", host],
            capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            # Extrahiere durchschnittliche Latenz
            avg_match = re.search(r'avg.*?=.*?([\d.]+)', result.stdout)
            avg = avg_match.group(1) + " ms" if avg_match else "N/A"

            if lang == "de":
                return f"🏓 **Ping zu `{host}`:**\n  ✅ Erreichbar! Ø Latenz: `{avg}`"
            else:
                return f"🏓 **Ping to `{host}`:**\n  ✅ Reachable! Avg latency: `{avg}`"
        else:
            if lang == "de":
                return f"🏓 **Ping zu `{host}`:**\n  ❌ Nicht erreichbar / Host unreachable"
            else:
                return f"🏓 **Ping to `{host}`:**\n  ❌ Host unreachable"
    except Exception as e:
        return f"🏓 Fehler / Error: {e}"


def get_speedtest(lang: str = "de") -> str:
    """
    Führt einen einfachen Download-Speedtest durch.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Geschwindigkeitsergebnis
    """
    test_url = "https://speed.hetzner.de/10MB.bin"

    try:
        start = time.time()
        req = urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
        elapsed = time.time() - start

        size_mb = len(data) / (1024 * 1024)
        speed_mbps = (size_mb * 8) / elapsed

        if lang == "de":
            return (
                f"🚀 **Speedtest:**\n"
                f"  • Heruntergeladen: `{size_mb:.1f} MB`\n"
                f"  • Dauer: `{elapsed:.1f}s`\n"
                f"  • Geschwindigkeit: `{speed_mbps:.1f} Mbps`"
            )
        else:
            return (
                f"🚀 **Speedtest:**\n"
                f"  • Downloaded: `{size_mb:.1f} MB`\n"
                f"  • Duration: `{elapsed:.1f}s`\n"
                f"  • Speed: `{speed_mbps:.1f} Mbps`"
            )
    except Exception as e:
        return f"🚀 Fehler / Error: {e}"


def get_weather(city: str = "Berlin", lang: str = "de") -> str:
    """
    Ruft aktuelle Wetterdaten von Open-Meteo API ab.

    Args:
        city: Stadtname (wird URL-kodiert)
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Temperatur und Wind
    """
    try:
        # Schritt 1: Geocoding (Stadt → Koordinaten)
        city_encoded = urllib.parse.quote(city)
        geo_url = (
            f"{Config.GEO_API_BASE}?"
            f"name={city_encoded}&count=1&language={lang}"
        )

        req = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            geo_data = json.loads(response.read().decode())

        if not geo_data or "results" not in geo_data or not geo_data["results"]:
            msg = f"Stadt '{city}' nicht gefunden." if lang == "de" else f"City '{city}' not found."
            return msg

        target = geo_data["results"][0]
        lat = target["latitude"]
        lon = target["longitude"]

        target = geo_data["results"][0]

        lat = target["latitude"]
        lon = target["longitude"]
        timezone = target["timezone"]
        found_city = f"{target['name']} ({target.get('country', '')})"

        # Schritt 2: Wetterdaten abrufen
        weather_url = (
            f"{Config.WEATHER_API_BASE}?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,wind_speed_10m,relative_humidity_2m"
        )

        with urllib.request.urlopen(weather_url, timeout=10) as response:
            weather_data = json.loads(response.read().decode())

        current = weather_data["current"]
        temp = current["temperature_2m"]
        wind = current["wind_speed_10m"]
        humidity = current.get("relative_humidity_2m", "N/A")

        if lang == "de":
            return (
                f"🌤️ **Wetter in {found_city}:**\n"
                f"  • Temperatur: `{temp}°C`\n"
                f"  • Wind: `{wind} km/h`\n"
                f"  • Luftfeuchtigkeit: `{humidity}%`"
            )
        else:
            return (
                f"🌤️ **Weather in {found_city}:**\n"
                f"  • Temperature: `{temp}°C`\n"
                f"  • Wind: `{wind} km/h`\n"
                f"  • Humidity: `{humidity}%`"
            )

    except urllib.error.URLError:
        return (
            "🌤️ Keine Internetverbindung. Wetterdaten nicht verfügbar.\n"
            "🌤️ No internet connection. Weather data unavailable."
        )
    except Exception as e:
        return f"🌤️ Fehler / Error: {e}"


def get_time_info(lang: str = "de") -> str:
    """
    Gibt aktuelle Uhrzeit und Datum zurück.

    Args:
        lang: "de" oder "en"

    Returns:
        Formatierter String mit Zeit und Datum
    """
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str_de = now.strftime("%d.%m.%Y")
    date_str_en = now.strftime("%Y-%m-%d")
    weekday_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", 
                  "Freitag", "Samstag", "Sonntag"][now.weekday()]
    weekday_en = ["Monday", "Tuesday", "Wednesday", "Thursday",
                  "Friday", "Saturday", "Sunday"][now.weekday()]

    if lang == "de":
        return (
            f"🕐 **Aktuelle Zeit:**\n"
            f"  • Uhrzeit: `{time_str}`\n"
            f"  • Datum: `{date_str_de}`\n"
            f"  • Wochentag: `{weekday_de}`"
        )
    else:
        return (
            f"🕐 **Current Time:**\n"
            f"  • Time: `{time_str}`\n"
            f"  • Date: `{date_str_en}`\n"
            f"  • Weekday: `{weekday_en}`"
        )


    try:
        city_encoded = urllib.parse.quote(city)

        geo_url = (
            f"{Config.GEO_API_BASE}?"
            f"name={city_encoded}&count=1&language={lang}"
        )

        with urllib.request.urlopen(geo_url, timeout=10) as response:
            geo_data = json.loads(response.read().decode())

        if not geo_data.get("results"):
            return f"Stadt '{city}' nicht gefunden."

        target = geo_data["results"][0]

        city_name = target["name"]
        country = target.get("country", "")
        timezone = target["timezone"]

        now = datetime.now(ZoneInfo(timezone))

        return (
            f"🕐 Uhrzeit in {city_name} ({country})\n"
            f"• Zeit: {now.strftime('%H:%M:%S')}\n"
            f"• Datum: {now.strftime('%d.%m.%Y')}\n"
            f"• Zeitzone: {timezone}"
        )

    except Exception as e:
        return f"Fehler: {e}"


