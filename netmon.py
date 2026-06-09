#!/usr/bin/env python3
"""
Netzwerk-Monitor für Heimnetzwerke
ARP-Scan + Nmap + Logging
"""

import time
import logging
import subprocess
import sys
import os  # ← DAS WAR DER FEHLER (os wurde vergessen)
from datetime import datetime
from scapy.all import ARP, Ether, srp
import nmap

# ==================== KONFIGURATION ====================
NETWORK = "192.168.1.0/24"  # Dein Netzwerk anpassen!
SCAN_INTERVAL = 300  # 5 Minuten in Sekunden
LOG_FILE = "/var/log/netmon.log"
KNOWN_MACS = {
    "aa:bb:cc:dd:ee:ff": "Mein iPhone",
    "11:22:33:44:55:66": "Mein Laptop",
    # Weitere MACs hier hinzufügen
}

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Terminal-Farben
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# ==================== FUNKTIONEN ====================

def arp_scan(network):
    """Führt ARP-Scan durch und gibt Liste der Geräte zurück"""
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    devices = []
    
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def port_scan(ip):
    """Führt schnellen Port-Scan auf wichtige Ports durch"""
    nm = nmap.PortScanner()
    ports = "22,80,443,8080"
    
    try:
        nm.scan(ip, ports, arguments='-T4 --host-timeout 30s')
        open_ports = []
        
        for port in ports.split(','):
            port = int(port)
            if ip in nm.all_hosts() and 'tcp' in nm[ip]:
                state = nm[ip]['tcp'][port]['state']
                if state == 'open':
                    service = nm[ip]['tcp'][port].get('name', 'unknown')
                    open_ports.append(f"{port}/{service}")
        
        return open_ports
    except Exception as e:
        logging.error(f"Port-Scan Fehler für {ip}: {e}")
        return []

def log_event(message, level="INFO", terminal=True):
    """Schreibt in Log-Datei und optional auf Terminal"""
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    
    if terminal:
        if "UNBEKANNT" in message:
            print(f"{RED}{message}{RESET}")
        elif "NEU" in message:
            print(f"{YELLOW}{message}{RESET}")
        else:
            print(f"{GREEN}{message}{RESET}")

def check_known_device(mac, ip):
    """Prüft ob MAC bekannt ist und gibt Name zurück"""
    if mac in KNOWN_MACS:
        return KNOWN_MACS[mac]
    else:
        log_event(f"⚠️ UNBEKANNTES GERÄT erkannt! IP: {ip}, MAC: {mac}", "WARNING")
        return None

# ==================== HAUPT-SCHLEIFE ====================

def main():
    print(f"{GREEN}🚀 Netzwerk-Monitor gestartet{RESET}")
    print(f"📡 Überwache Netzwerk: {NETWORK}")
    print(f"⏱️  Scan-Intervall: {SCAN_INTERVAL} Sekunden")
    print(f"📝 Log-Datei: {LOG_FILE}\n")
    
    known_devices = {}
    
    while True:
        try:
            print(f"\n🔍 {datetime.now().strftime('%H:%M:%S')} - Führe ARP-Scan durch...")
            devices = arp_scan(NETWORK)
            
            current_macs = []
            
            for device in devices:
                ip = device['ip']
                mac = device['mac']
                current_macs.append(mac)
                
                # Neues Gerät entdeckt?
                if mac not in known_devices:
                    known_devices[mac] = {'ip': ip, 'first_seen': datetime.now()}
                    name = check_known_device(mac, ip)
                    
                    if name is None:
                        log_event(f"🚨 NEUES UNBEKANNTES GERÄT: {ip} ({mac})", "WARNING")
                        
                        # Automatischer Port-Scan
                        print(f"🔎 Führe Port-Scan für {ip} durch...")
                        open_ports = port_scan(ip)
                        
                        if open_ports:
                            ports_str = ", ".join(open_ports)
                            log_event(f"📌 Offene Ports auf {ip}: {ports_str}", "INFO")
                        else:
                            log_event(f"📌 Keine offenen Standard-Ports auf {ip}", "INFO")
                    else:
                        log_event(f"✅ Bekanntes Gerät verbunden: {name} ({ip})", "INFO")
                else:
                    # Bekanntes Gerät
                    name = KNOWN_MACS.get(mac, "Unbekannt")
                    print(f"  • {name} - {ip} ({mac})")
            
            # Gerät nicht mehr im Netzwerk?
            for mac in list(known_devices.keys()):
                if mac not in current_macs:
                    name = KNOWN_MACS.get(mac, "Unbekannt")
                    log_event(f"📴 Gerät getrennt: {name} ({known_devices[mac]['ip']})", "INFO")
                    del known_devices[mac]
            
            print(f"💤 Warte {SCAN_INTERVAL} Sekunden bis zum nächsten Scan...")
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            print(f"\n{RED}👋 Monitor gestoppt{RESET}")
            break
        except Exception as e:
            log_event(f"❌ Fehler: {e}", "ERROR")
            time.sleep(60)

if __name__ == "__main__":
    # Prüfe auf Root-Rechte
    if not sys.platform.startswith('linux'):
        print("❌ Dieses Skript benötigt Linux!")
        sys.exit(1)
    
    if os.geteuid() != 0:
        print("❌ Bitte mit sudo ausführen: sudo python3 netmon.py")
        sys.exit(1)
    
    main()
