#!/usr/bin/env python3
"""
🤖 JARVIS CHATBOT v2_12 - KI erstellt automatisch Code-Dateien
"""

import socket
import uuid
import subprocess
import sys
import os
from datetime import datetime

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

try:
    import ollama
    OLLAMA_OK = True
except ImportError:
    OLLAMA_OK = False

# ========== NETZWERK ==========
def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def get_mac():
    mac_num = uuid.getnode()
    return ':'.join(f'{(mac_num >> i) & 0xff:02x}' for i in range(40, -1, -8))

def get_dns():
    dns_list = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_list.append(line.split()[1])
    except:
        pass
    return dns_list if dns_list else ["keine DNS"]

def get_time():
    now = datetime.now()
    return f"{now.strftime('%H:%M:%S')} - {now.strftime('%d.%m.%Y')}"

def get_cpu():
    if not PSUTIL_OK:
        return "psutil nicht installiert"
    return f"{psutil.cpu_percent(interval=0.5)}%"

def get_ram():
    if not PSUTIL_OK:
        return "psutil nicht installiert"
    ram = psutil.virtual_memory()
    return f"{ram.percent}% ({ram.used//(1024**3)} GB/{ram.total//(1024**3)} GB)"

def get_gpu():
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "VGA" in line or "3D" in line:
                return line.split(":")[-1].strip()[:50]
        return "nicht erkannt"
    except:
        return "nicht erkannt"

def get_netzlast():
    if not PSUTIL_OK:
        return "psutil nicht installiert"
    net = psutil.net_io_counters()
    return f"📤 {net.bytes_sent/(1024**2):.1f} MB | 📥 {net.bytes_recv/(1024**2):.1f} MB"

# ========== KI (QWEN) ==========
def ask_qwen(prompt):
    if not OLLAMA_OK:
        return "❌ ollama nicht installiert"
    try:
        r = ollama.chat(model="qwen2.5-coder:1.5b", messages=[
            {"role": "user", "content": prompt}
        ])
        return r['message']['content']
    except Exception as e:
        return f"❌ Fehler: {e}"

# ========== CODE GENERIEREN + SPEICHERN ==========
def generate_and_save_code(description):
    print("\n⏳ KI generiert Code...")
    
    # Code generieren
    code = ask_qwen(f"Schreibe NUR den Python-Code. Keine Erklärungen. Keine Einleitungen. KEINE Markdown-Codeblöcke. KEINE Backticks. NUR den reinen Code. Keine Markdown-Codeblöcke. Keine Backticks. {description}")
    
    if code.startswith("❌"):
        print(code)
        return
    
    # Code anzeigen
    print("\n" + "="*60)
    print("📝 GENERIERTER CODE:")
    print("="*60)
    print(code)
    print("="*60)
    
    # Nach Dateinamen fragen
    print("\n💾 In welche Datei soll der Code gespeichert werden?")
    print("   (z.B. uhr.py oder mein_programm.py)")
    filename = input("📁 Dateiname: ").strip()
    
    if not filename:
        print("❌ Kein Dateiname eingegeben. Code nicht gespeichert.")
        return
    
    # .py hinzufügen wenn fehlt
    if not filename.endswith(".py"):
        filename += ".py"
    
    # Speichern
    try:
        with open(filename, "w") as f:
            f.write(code)
        print(f"\n✅ Code gespeichert als: {filename}")
        
        # Fragen ob nano geöffnet werden soll
        print("\n📝 Mit nano bearbeiten? (j/n)")
        if input().lower() == "j":
            subprocess.run(["nano", filename])
        else:
            print(f"💡 Datei ist unter: {os.path.abspath(filename)}")
            
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")

# ========== INSTALLATION ==========
def pip_install(pkg):
    subprocess.run([sys.executable, "-m", "pip", "install", pkg])

def apt_install(pkg):
    subprocess.run(["sudo", "apt", "install", "-y", pkg])

# ========== HAUPT ==========
print("\n" + "="*60)
print("  🤖 JARVIS BOT v11.0 - Code wird automatisch gespeichert")
print("="*60)
print("  ip | mac | dns | uhrzeit | cpu | ram | gpu | netzlast")
print("  code <beschreibung> | beliebige Fragen | pip | apt | bye")
print("="*60)
print("  ✨ NEU: Bei 'code' fragt der Bot nach Dateinamen")
print("  ✨ und speichert den Code direkt in eine Datei!")
print("="*60 + "\n")

while True:
    try:
        cmd = input("💬 Du: ").strip().lower()
        if not cmd:
            continue
        
        if cmd in ["bye", "exit", "quit"]:
            print("\n👋 Tschüss!\n")
            break
        
        # Befehle
        if cmd == "ip":
            print(f"\n📡 IP: {get_ip()}\n")
        elif cmd == "mac":
            print(f"\n🔌 MAC: {get_mac()}\n")
        elif cmd == "dns":
            print(f"\n📋 DNS: {', '.join(get_dns())}\n")
        elif cmd == "uhrzeit":
            print(f"\n🕐 {get_time()}\n")
        elif cmd == "cpu":
            print(f"\n🖥️ CPU: {get_cpu()}\n")
        elif cmd == "ram":
            print(f"\n🧠 RAM: {get_ram()}\n")
        elif cmd == "gpu":
            print(f"\n🎮 GPU: {get_gpu()}\n")
        elif cmd == "netzlast":
            print(f"\n🌐 {get_netzlast()}\n")
        elif cmd.startswith("code "):
            description = cmd[5:]
            generate_and_save_code(description)
        elif cmd.startswith("pip "):
            pip_install(cmd[4:])
            print(f"✅ {cmd[4:]} installiert\n")
        elif cmd.startswith("apt "):
            apt_install(cmd[4:])
            print(f"✅ {cmd[4:]} installiert\n")
        else:
            print("\n⏳ KI denkt nach...\n")
            antwort = ask_qwen(cmd)
            print(f"🤖 {antwort}\n")
    
    except KeyboardInterrupt:
        print("\n\n👋 Tschüss!\n")
        break
    except Exception as e:
        print(f"\n❌ Fehler: {e}\n")
