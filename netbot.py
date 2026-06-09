#!/usr/bin/env python3
import socket
import uuid
from pathlib import Path

def get_network_info():
    # IP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    
    # MAC
    mac = ':'.join(format((uuid.getnode() >> i) & 0xff, '02x') for i in range(40, -1, -8))
    
    # DNS
    dns = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns.append(line.split()[1])
    except:
        pass
    
    return f"IP: {ip}\nMAC: {mac}\nDNS: {', '.join(dns) if dns else 'keine' }"

print(get_network_info())
