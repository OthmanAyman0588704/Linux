import sys
import os
import json
import socket
import uuid
import urllib.request
import urllib.parse
from datetime import datetime
import psutil

try:
    import cpuinfo
except ImportError:
    print("Error: Please run 'pip install py-cpuinfo' inside your activated .venv!")
    sys.exit(1)

try:
    import ollama
except ImportError:
    print("Error: Please run 'pip install ollama' inside your activated .venv!")
    sys.exit(1)

print("================================================================")
print("     🚀 BILINGUAL HYBRID-AI & NET/HARDWARE BOT STARTED...      ")
print("          (Combos like 'wien zeit und wetter' now work!)       ")
print("================================================================")

# Erweitertes Wörterbuch für Slang
SLANG_TRANSLATION = {
    "hw": "how", "wv": "wieviel", "rn": "now", "jz": "jetzt",
    "pls": "please", "thx": "thanks", "idk": "i dont know",
    "brb": "be right back", "vllt": "vielleicht", "kb": "keinen bock",
    "ip": "network_info", "mac": "network_info", "dns": "network_info",
    "uhrzeit": "time_info", "uhr": "time_info", "zeit": "time_info", "clock": "time_info"
}

def translate_slang(text):
    words = text.split()
    return " ".join([SLANG_TRANSLATION.get(word, word) for word in words])

def detektiere_sprache(text):
    englische_wörter = ["weather", "ram", "cpu", "gpu", "space", "network", "traffic", "temp", "how", "what", "bye", "exit", "hi", "hardware", "dns", "mac", "specs", "time", "clock"]
    text_lower = text.lower()
    for wort in englische_wörter:
        if wort in text_lower:
            return "en"
    return "de"

def hole_netzwerk_und_ips(lang="de"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lokale_ip = s.getsockname()[0]
        s.close()
    except Exception:
        lokale_ip = "127.0.0.1"

    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])

    dns_servers = []
    if os.path.exists("/etc/resolv.conf"):
        with open("/etc/resolv.conf", "r") as f:
            for zeile in f:
                if zeile.startswith("nameserver"):
                    teile = zeile.split()
                    if len(teile) > 1:
                        dns_servers.append(teile[1])
    dns_str = ", ".join(dns_servers) if dns_servers else "Standard-DNS"

    test_ips = (
        "• Google Public DNS: 8.8.8.8 / 8.8.4.4\n"
        "• Cloudflare DNS: 1.1.1.1 / 1.0.0.1\n"
        "• Quad9 (Security): 9.9.9.9\n"
        "• OpenDNS: 208.67.222.222"
    )

    if lang == "de":
        return f"🌐 **Netzwerk-Informationen:**\n• Lokale IP-Adresse: {lokale_ip}\n• MAC-Adresse: {mac}\n• Aktuelle DNS-Server: {dns_str}\n\n🎯 **Wichtige Test-IPs (für Ping / DNS):**\n" + test_ips
    else:
        return f"🌐 **Network Information:**\n• Local IP Address: {lokale_ip}\n• MAC Address: {mac}\n• Current DNS Servers: {dns_str}\n\n🎯 **Important Test IPs (for Ping / DNS):**\n" + test_ips

def hole_hardware_komponenten(lang="de"):
    try:
        cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    except Exception:
        cpu_name = "Unbekannte CPU"

    ram_gesamt = psutil.virtual_memory().total // (1024**3)
    os_info = os.uname()
    kernel = os_info.release
    arch = os_info.machine

    if lang == "de":
        return f"🔌 **Erkannte Hardware-Teile & OS-Specs:**\n• Prozessor (CPU): {cpu_name}\n• Architektur: {arch}\n• Arbeitsspeicher (RAM): {ram_gesamt} GB Gesamt\n• Linux-Kernel: {kernel}\n• Plattform: {os_info.sysname} ({os_info.nodename})"
    else:
        return f"🔌 **Detected Hardware & OS Specs:**\n• Processor (CPU): {cpu_name}\n• Architecture: {arch}\n• Total RAM: {ram_gesamt} GB\n• Linux Kernel: {kernel}\n• Platform: {os_info.sysname} ({os_info.nodename})"

def get_system_data(lang="de"):
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    mb_sent = network.bytes_sent / (1024 * 1024)
    mb_recv = network.bytes_recv / (1024 * 1024)
    
    if lang == "de":
        return f"🖥️ **Live-System-Auslastung:**\n• CPU: {cpu_usage}%\n• RAM: {ram.percent}% ({ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB)\n• Festplatte: {disk.percent}% belegt\n• Netzwerktraffic: Gesendet: {mb_sent:.2f} MB | Empfangen: {mb_recv:.2f} MB"
    else:
        return f"🖥️ **Live System Metrics:**\n• CPU: {cpu_usage}%\n• RAM: {ram.percent}% ({ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB)\n• Disk Space: {disk.percent}% used\n• Network Traffic: Sent: {mb_sent:.2f} MB | Received: {mb_recv:.2f} MB"

def get_weather(city="Berlin", lang="de"):
    try:
        city_encoded = urllib.parse.quote(city)
        geo_url = f"https://open-meteo.com{city_encoded}&count=1&language={lang}"
        req = urllib.request.Request(geo_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req) as response:
            geo_daten = json.loads(response.read().decode())
            if not geo_daten or "results" not in geo_daten:
                return f"City '{city}' not found." if lang == "en" else f"Stadt '{city}' nicht gefunden."
            
            ziel = geo_daten["results"][0]
            lat = ziel["latitude"]
            lon = ziel["longitude"]
            found_city = f"{ziel['name']} ({ziel.get('country', '')})"

        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
        with urllib.request.urlopen(weather_url) as response:
            weather_data = json.loads(response.read().decode())
            current = weather_data["current"]
            temp = current["temperature_2m"]
            wind = current["wind_speed_10m"]
            
            return f"🌤️ **Weather in {found_city}:** {temp}°C (Wind: {wind} km/h)." if lang == "en" else f"🌤️ **Wetter in {found_city}:** {temp}°C (Wind: {wind} km/h)."
    except Exception as e:
        return f"Error fetching weather: {e}" if lang == "en" else f"Fehler beim Abrufen des Wetters: {e}"

history = [
    {
        "role": "system", 
        "content": "You are a bilingual Linux assistant. Reply in German if the user speaks German, and in English if the user speaks English. Keep it casual and use emojis."
    }
]

while True:
    try:
        raw_input = input("\nYou: ").strip()
        if not raw_input:
            continue
            
        input_lower = raw_input.lower()
        if input_lower in ["bye", "exit", "quit", "tschüss", "ciao"]:
            print("Bot: Bye! / Tschüss!")
            break
            
        cleaned_input = translate_slang(input_lower)
        sprache = detektiere_sprache(cleaned_input)
        befehl_ausgefuehrt = False
        
        # --- 1. UHRZEIT / TIME ---
        if any(word in cleaned_input for word in ["time_info", "time", "clock", "spät", "spaet"]):
            jetzt = datetime.now().strftime("%H:%M:%S")
            datum = datetime.now().strftime("%d.%m.%Y")
            if sprache == "de":
                print(f"Bot: Es ist aktuell {jetzt} Uhr am {datum}.")
            else:
                print(f"Bot: The current time is {jetzt} on {datum}.")
            befehl_ausgefuehrt = True

        # --- 2. NETZWERK, IP, MAC, DNS ---
        if any(word in cleaned_input for word in ["network_info", "ip", "mac", "dns", "netzwerk", "internet"]):
            print("Bot is gathering network data...")
            print(f"Bot:\n{hole_netzwerk_und_ips(sprache)}")
            befehl_ausgefuehrt = True

        # --- 3. HARDWARE SPECS / GERÄTE ---
        if any(word in cleaned_input for word in ["hardware", "specs", "teile", "komponenten", "geraete", "geräte", "systeminfo"]):
            print("Bot is scanning hardware...")
            print(f"Bot:\n{hole_hardware_komponenten(sprache)}")
            befehl_ausgefuehrt = True
        
        # --- 4. LIVE AUSLASTUNG (RAM, CPU) ---
        if any(word in cleaned_input for word in ["space", "ram", "cpu", "gpu", "monitoring", "traffic", "temp", "speicher", "festplatte"]):
            print("Bot is reading sensors / Bot liest Sensoren...")
            print(f"Bot:\n{get_system_data(sprache)}")
            befehl_ausgefuehrt = True
            
        # --- 5. WETTER ---
        if any(word in cleaned_input for word in ["weather", "wetter"]):
            city = "Berlin"
            words = raw_input.split()
            for trenner in ["in ", "für ", "for "]:
                if trenner in input_lower:
                    city = raw_input.split(trenner)[-1].strip("? .")
                    break
            if city == "Berlin" and len(words) > 1:
                cleaned_words = [w.strip("? .") for w in words if w.lower() not in ["weather", "wetter", "und", "and", "zeit", "time", "uhr", "wie", "ist", "das"]]
                if cleaned_words:
                    city = " ".join(cleaned_words)
            print(f"Bot is fetching data / Bot lädt Daten...")
            print(f"Bot: {get_weather(city, sprache)}")
            befehl_ausgefuehrt = True

        if befehl_ausgefuehrt:
            continue

        # --- 6. KI ANFRAGE ---
        history.append({"role": "user", "content": raw_input})
        print("Bot is thinking / Bot denkt nach...")
        
        response = ollama.chat(model='gemma2:2b', messages=history)
        bot_text = response['message']['content']
        print(f"\nBot:\n{bot_text}")
        history.append({"role": "assistant", "content": bot_text})
        
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Bye!")
        sys.exit()
    except Exception as e:
        print(f"\nBot: Error / Fehler: ({e})")
        sys.exit()
