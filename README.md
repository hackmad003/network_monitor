# Network Device Monitor

> 🎯 **Professional-grade network monitoring solution** - Track device connections on your local network with SQL Server backend and Power BI reporting.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ New in v1.0.0

- **🏗️ Modular Architecture**: Refactored into clean, testable modules
- **📦 Proper Package Structure**: Installable Python package with `pip`
- **🧪 Unit Tests**: Comprehensive test suite included
- **📚 Complete Documentation**: Architecture, API reference, deployment guides
- **🐳 Docker Support**: Ready for containerized deployment
- **🔧 Professional Standards**: Type hints, logging, error handling
- **🌐 Web Dashboard**: Modern web interface for real-time monitoring (NEW!)

---

# Network Device Monitor

Monitor devices connecting to your home network and log them to SQL Server for Power BI dashboards.

## What This Does

- 🔍 **Scans** your home network every minute (configurable)
- 📝 **Logs** every device connection and disconnection
- 💾 **Stores** data in SQL Server database
- 📊 **Ready** for Power BI dashboards
- 🌐 **Web Dashboard** for real-time monitoring and visualization

---

## Prerequisites

You'll need to install these first:

### 1. Python 3.8 or higher
- Download from: https://www.python.org/downloads/
- **IMPORTANT**: During installation, check "Add Python to PATH"

### 2. SQL Server
You have two options:

**Option A: SQL Server Express (FREE)**
- Download: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
- Choose "Express" edition
- During setup, choose "Basic" installation

**Option B: SQL Server Developer Edition (FREE, more features)**
- Same download link, choose "Developer" edition

### 3. SQL Server Management Studio (SSMS)
- Download: https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms
- This is the tool to manage your database

### 4. ODBC Driver for SQL Server
- Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Download "ODBC Driver 17 for SQL Server"

### 5. Npcap (for network scanning on Windows)
- Download: https://npcap.com/#download
- Install with default settings

---

## Step-by-Step Setup

### Step 1: Install Python Packages

1. Open VS Code
2. Open Terminal in VS Code (View → Terminal, or Ctrl+`)
3. Navigate to the project folder:
   ```bash
   cd path\to\network_monitor
   ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

   If you get an error, try:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Step 2: Set Up the Database

1. Open **SQL Server Management Studio (SSMS)**
2. Connect to your local SQL Server:
   - Server name: `localhost` or `.\SQLEXPRESS`
   - Authentication: Windows Authentication
   - Click "Connect"

3. Open the `database_setup.sql` file in SSMS:
   - File → Open → File → Select `database_setup.sql`

4. Click "Execute" (or press F5)
   - You should see "Database setup complete!" message

### Step 3: Configure the Application

1. In your project folder, find `.env.example`
2. Copy it and rename to `.env`
3. Open `.env` in VS Code
4. Edit these settings:

```env
# Your home network (most common is 192.168.1.0/24)
# To find yours:
# - Open Command Prompt (cmd)
# - Type: ipconfig
# - Look for "IPv4 Address" (e.g., 192.168.1.100)
# - Your subnet is likely: 192.168.1.0/24
NETWORK_SUBNET=192.168.1.0/24

# How often to scan (in seconds)
SCAN_INTERVAL=60

# SQL Server settings
SQL_SERVER=localhost
SQL_DATABASE=NetworkMonitor

# If you're using Windows Authentication (recommended)
SQL_WINDOWS_AUTH=yes

# If you want to use SQL authentication instead:
# SQL_WINDOWS_AUTH=no
# SQL_USERNAME=your_username
# SQL_PASSWORD=your_password
```

### Step 4: Run the Application

**IMPORTANT**: You need administrator privileges to scan the network.

You have two options:

#### Option A: Web Dashboard (Recommended) 🌐

The web dashboard provides a modern interface to monitor your network in real-time.

**On Windows:**
1. Right-click `scripts/start_web_dashboard.bat`
2. Select "Run as administrator"
3. Open your browser and go to: `http://localhost:5000`

**On Linux/Mac:**
```bash
sudo ./scripts/start_web_dashboard.sh
```

**Features:**
- Real-time device monitoring
- Connection history and events
- Manual scan trigger
- Device details and statistics
- Auto-refresh every 5 seconds

📖 **For complete web dashboard documentation, see [WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md)**  
🚀 **For quick start guide, see [QUICKSTART_WEB_DASHBOARD.md](QUICKSTART_WEB_DASHBOARD.md)**

#### Option B: Command-Line Monitor

For traditional command-line interface:

**On Windows:**
1. Close VS Code
2. Right-click VS Code icon → "Run as administrator"
3. Open your project folder again
4. Open Terminal (Ctrl+`)
5. Run:
   ```bash
   python network_monitor.py
   ```

**On Linux/Mac:**
```bash
sudo python network_monitor.py
```

You should see:
```
Network Device Monitor
Monitoring network: 192.168.1.0/24
Scan interval: 60 seconds
Scanning network...
Found X devices on network
```

To stop: Press `Ctrl+C`

---

## Verify It's Working

### Check Database in SSMS

1. Open SSMS
2. Connect to your server
3. Expand: Databases → NetworkMonitor → Tables
4. Right-click `DeviceConnections` → "Select Top 1000 Rows"
5. You should see devices listed!

### View the Log File

- Check `network_monitor.log` in your project folder
- It shows all scan activity and any errors

---

## Connect to Power BI

### Step 1: Get Power BI Desktop (FREE)
- Download: https://powerbi.microsoft.com/desktop/

### Step 2: Connect to Your Database

1. Open Power BI Desktop
2. Click "Get Data" → "SQL Server"
3. Enter:
   - Server: `localhost`
   - Database: `NetworkMonitor`
   - Data Connectivity mode: Import
4. Click "OK"
5. Select tables to import:
   - ✅ DeviceConnections
   - ✅ ConnectionLog
   - ✅ vw_CurrentlyConnected
   - ✅ vw_ConnectionHistory
   - ✅ vw_DailyConnectionSummary
6. Click "Load"

### Step 3: Create Visualizations

**Suggested Visuals:**

1. **Card Visual**: Total Devices Currently Connected
   - Use: `vw_CurrentlyConnected` table
   - Count of MACAddress

2. **Table**: Active Devices
   - Use: `vw_CurrentlyConnected`
   - Columns: DisplayName, IPAddress, LastSeen

3. **Line Chart**: Connections Over Time
   - Use: `vw_DailyConnectionSummary`
   - X-axis: Date
   - Y-axis: TotalConnections

4. **Bar Chart**: Connection Events
   - Use: `vw_ConnectionHistory`
   - X-axis: DisplayName
   - Y-axis: Count of EventType

---

## Troubleshooting

### "Failed to connect to database"
- Check SQL Server is running (Services → SQL Server)
- Verify server name in `.env` (try `.\SQLEXPRESS` if `localhost` doesn't work)

### "Permission denied" when scanning
- Run VS Code as administrator (Windows)
- Use `sudo` before the command (Linux/Mac)

### "No devices found"
- Check your `NETWORK_SUBNET` setting
- Make sure you're on the same network
- Try running: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

### "Module not found" errors
- Make sure you installed requirements: `pip install -r requirements.txt`
- Check Python is in PATH: `python --version`

### Npcap not working
- Reinstall Npcap with "WinPcap compatibility" option checked

---

## Running Automatically (Optional)

### Run on Startup (Windows)

1. Create a batch file `start_monitor.bat`:
```batch
@echo off
cd C:\path\to\network_monitor
python network_monitor.py
pause
```

2. Press `Win + R`, type `shell:startup`
3. Create shortcut to your batch file here
4. Right-click shortcut → Properties → Advanced → "Run as administrator"

---

## Customization

### Add Friendly Names to Devices

In SSMS:
```sql
UPDATE DeviceConnections 
SET DeviceName = 'Johns iPhone'
WHERE MACAddress = 'AA:BB:CC:DD:EE:FF';
```

### Change Scan Frequency

Edit `.env`:
```env
SCAN_INTERVAL=30  # Scan every 30 seconds
```

---

## Files in This Project

### Main Files
- `network_monitor.py` - Legacy command-line application
- `requirements.txt` - Python packages needed
- `.env.example` - Template configuration file
- `.env` - Your actual configuration (you create this)
- `database_setup.sql` - Database creation script
- `network_monitor.log` - Application log file (created automatically)
- `README.md` - This file!
- `WEB_DASHBOARD_GUIDE.md` - Web dashboard documentation

### Source Code (`src/network_monitor/`)
- `main.py` - Command-line monitor entry point
- `web.py` - Web dashboard Flask application
- `web_main.py` - Web dashboard entry point
- `monitor.py` - Network monitoring orchestration
- `scanner.py` - Network scanning functionality
- `database.py` - Database operations
- `config.py` - Configuration management

### Scripts
- `scripts/start_monitor.bat/sh` - Start command-line monitor
- `scripts/start_web_dashboard.bat/sh` - Start web dashboard

### Web Dashboard Files
- `templates/index.html` - Dashboard HTML
- `static/css/style.css` - Dashboard styles
- `static/js/main.js` - Dashboard JavaScript

---

## Need Help?

Common issues and solutions are in the Troubleshooting section above.

## Web Dashboard

The web dashboard provides a modern, user-friendly interface for monitoring your network:

- **Real-time monitoring** with auto-refresh every 5 seconds
- **Device management** with search and filtering
- **Connection history** and event tracking
- **Statistics dashboard** with 24-hour activity
- **Manual scan trigger** for immediate updates
- **REST API** for custom integrations

📖 **See [WEB_DASHBOARD_GUIDE.md](WEB_DASHBOARD_GUIDE.md) for complete documentation**

Quick Start:
```bash
# Windows (as Administrator)
scripts\start_web_dashboard.bat

# Linux/Mac (with sudo)
sudo ./scripts/start_web_dashboard.sh

# Then open: http://localhost:5000
```

## Next Steps

- **🌐 Use the Web Dashboard**: Monitor your network in real-time with the modern web interface
- **Customize device names**: Edit `DeviceName` field in `DeviceConnections` table
- **Set up Power BI**: Connect to your database for visualizations
- **Schedule reports**: Use Power BI scheduled refresh
- **Add more devices**: They'll be detected automatically
- **Access remotely**: Configure firewall to access the web dashboard from other devices

Enjoy monitoring your network! 🎉
