# Web Dashboard Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
Make sure you've completed the basic setup from the main README.md:
- ✅ Python 3.8+ installed
- ✅ SQL Server running and accessible
- ✅ Database created using `database_setup.sql`
- ✅ `.env` file configured

### Step 1: Install Web Dashboard Dependencies

If you haven't already installed all dependencies:

```bash
pip install -r requirements.txt
```

This will install Flask and Flask-CORS in addition to the existing dependencies.

### Step 2: Configure Web Settings (Optional)

The web dashboard works with default settings, but you can customize by adding these to your `.env` file:

```env
# Web Dashboard Settings (optional)
WEB_HOST=0.0.0.0          # Listen on all network interfaces
WEB_PORT=5000             # Port number
WEB_DEBUG=no              # Enable debug mode (yes/no)
AUTO_START_MONITORING=yes # Auto-start network monitoring
```

### Step 3: Start the Web Dashboard

**Windows:**
1. Right-click `scripts/start_web_dashboard.bat`
2. Select "Run as administrator"
3. Wait for message: "Open your browser and navigate to: http://localhost:5000"

**Linux/Mac:**
```bash
sudo ./scripts/start_web_dashboard.sh
```

### Step 4: Open the Dashboard

Open your web browser and go to:
```
http://localhost:5000
```

That's it! You should see the Network Monitor Dashboard.

---

## 🎯 What You'll See

### Dashboard Overview

**Status Bar** (top of page)
- Shows monitoring status (active/stopped)
- Network subnet being monitored
- Scan interval
- Last update timestamp

**Statistics Cards** (4 cards)
- Connected Devices (currently online)
- Total Known Devices (all time)
- Connections in last 24 hours
- Disconnections in last 24 hours

**Devices Table** (main area)
- All network devices with their status
- Search and filter capabilities
- Click info button (ℹ️) to see device details

**Recent Events** (right side)
- Live feed of connections/disconnections
- Shows device names, IPs, and timestamps

### Dashboard Controls

**Scan Now Button** (top right)
- Triggers immediate network scan
- Updates the dashboard with fresh data

**Start/Stop Monitoring** (top right)
- Green = Monitoring active
- Gray = Monitoring stopped
- Click to toggle

---

## 🔧 Quick Troubleshooting

### Dashboard won't start?

**"Permission Denied" error**
- Make sure you're running as Administrator (Windows) or with sudo (Linux/Mac)

**"Port already in use" error**
- Change port in `.env`: `WEB_PORT=5001`
- Or stop other applications using port 5000

**"Database connection error"**
- Verify SQL Server is running
- Check `.env` database settings
- Ensure database was created with `database_setup.sql`

### Dashboard shows no devices?

1. Click "Scan Now" to trigger a manual scan
2. Check monitoring is active (green Start/Stop button)
3. Verify network subnet in `.env` matches your network
4. Ensure you have administrator privileges

### Can't access from another device?

1. Check `WEB_HOST=0.0.0.0` in `.env`
2. Verify firewall allows connections on port 5000
3. Use server's IP address: `http://192.168.1.x:5000`

---

## 📱 Access from Mobile/Tablet

The dashboard is fully responsive and works on mobile devices:

1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Linux/Mac: `ifconfig` or `ip addr`

2. On your mobile device, open browser:
   ```
   http://[your-computer-ip]:5000
   ```
   Example: `http://192.168.1.100:5000`

3. Make sure your mobile device is on the same network

---

## 🌟 Key Features

### Real-Time Updates
- Dashboard refreshes every 5 seconds automatically
- See devices connect/disconnect in real-time

### Device Search & Filter
- Search by device name, IP, MAC, or hostname
- Filter to show only connected or disconnected devices

### Device Details
- Click info button (ℹ️) on any device
- View complete connection history
- See all device information

### Manual Controls
- Start/stop monitoring without restarting
- Trigger scans on demand
- Perfect for testing

---

## 🔄 Running Both Interfaces

You can run the web dashboard alongside or instead of the command-line monitor:

**Web Dashboard Only** (Recommended)
```bash
# Set AUTO_START_MONITORING=yes in .env
scripts/start_web_dashboard.bat  # Windows
sudo ./scripts/start_web_dashboard.sh  # Linux/Mac
```

**Command-Line Only** (Traditional)
```bash
scripts/start_monitor.bat  # Windows
sudo ./scripts/start_monitor.sh  # Linux/Mac
```

**Both Separately**
```bash
# Set AUTO_START_MONITORING=no in .env
# Terminal 1: Web dashboard
python -m src.network_monitor.web_main

# Terminal 2: Command-line monitor
python -m src.network_monitor.main
```

---

## 🔗 REST API

The dashboard includes a REST API for custom integrations:

```bash
# Get status
curl http://localhost:5000/api/status

# Get all devices
curl http://localhost:5000/api/devices

# Get connected devices only
curl http://localhost:5000/api/devices/connected

# Get recent events
curl http://localhost:5000/api/events?limit=20

# Trigger a scan
curl -X POST http://localhost:5000/api/control/scan

# Start monitoring
curl -X POST http://localhost:5000/api/control/start

# Stop monitoring
curl -X POST http://localhost:5000/api/control/stop
```

---

## 📚 More Information

- **Full Documentation**: See `WEB_DASHBOARD_GUIDE.md`
- **General Setup**: See `README.md`
- **API Reference**: See `Docs/API_REFERENCE.md`

---

## 🎉 Enjoy Your Network Dashboard!

Your network monitor now has a beautiful web interface. Monitor devices in real-time, track connections, and analyze network activity—all from your browser!

**Need Help?**
- Check `network_monitor.log` for detailed error messages
- Review `WEB_DASHBOARD_GUIDE.md` for advanced features
- Ensure all prerequisites are met
