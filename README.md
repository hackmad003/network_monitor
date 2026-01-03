# Network Device Monitor

Monitor devices connecting to your home network and log them to SQL Server for Power BI dashboards.

## What This Does

- 🔍 **Scans** your home network every minute (configurable)
- 📝 **Logs** every device connection and disconnection
- 💾 **Stores** data in SQL Server database
- 📊 **Ready** for Power BI dashboards

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

### Step 4: Run the Monitor

**IMPORTANT**: You need administrator privileges to scan the network.

#### On Windows:
1. Close VS Code
2. Right-click VS Code icon → "Run as administrator"
3. Open your project folder again
4. Open Terminal (Ctrl+`)
5. Run:
   ```bash
   python network_monitor.py
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

- `network_monitor.py` - Main application
- `requirements.txt` - Python packages needed
- `.env.example` - Template configuration file
- `.env` - Your actual configuration (you create this)
- `database_setup.sql` - Database creation script
- `network_monitor.log` - Application log file (created automatically)
- `README.md` - This file!

---

## Need Help?

Common issues and solutions are in the Troubleshooting section above.

## Next Steps

1. Let the monitor run for a few days to collect data
2. Create Power BI dashboards to visualize:
   - Peak usage times
   - Most connected devices
   - Connection patterns
3. Set up automatic refresh in Power BI (File → Options → Data Load)

Enjoy monitoring your network! 🎉
