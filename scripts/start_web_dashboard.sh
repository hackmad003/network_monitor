#!/bin/bash
# Start Network Monitor Web Dashboard
# This script must be run with sudo for network scanning

echo "========================================"
echo "Network Monitor Web Dashboard"
echo "========================================"
echo ""

# Check for root privileges
if [ "$EUID" -ne 0 ]; then 
    echo "ERROR: This script requires root privileges!"
    echo ""
    echo "Please run with sudo:"
    echo "  sudo ./scripts/start_web_dashboard.sh"
    echo ""
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Using system Python."
fi

echo ""
echo "Starting web dashboard..."
echo ""

# Start the web dashboard
python -m src.network_monitor.web_main

echo ""
echo "Dashboard stopped."
