#!/bin/bash
# Network Monitor Startup Script for Linux/Mac

echo "===================================="
echo "Network Device Monitor"
echo "===================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run with sudo privileges"
    echo "Please run: sudo ./start_monitor.sh"
    exit 1
fi

echo "Starting network monitor..."
echo "Press Ctrl+C to stop"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python -m network_monitor.main
