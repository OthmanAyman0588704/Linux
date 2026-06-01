cat << 'EOF' > systeminfo.sh
#!/bin/bash
# Systeminformationen

echo "=== SYSTEM INFORMATIONEN ==="
echo "Hostname:   $(hostname)"
echo "Betriebssystem: $(uname -o)"
echo "Kernel:     $(uname -r)"
echo "Uptime:    $(uptime -p)"
echo "============================"

read -p "Fertig! Drücke ENTER zum Schließen..."
EOF

