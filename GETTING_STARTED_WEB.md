# 🚀 Getting Started with the Web Dashboard

## What You Just Got

Your Network Monitor application now has a **beautiful web dashboard** that lets you monitor your network in real-time from any browser!

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
This installs Flask and Flask-CORS (the new web dependencies).

### Step 2: Start the Dashboard

**Windows:**
1. Right-click `scripts/start_web_dashboard.bat`
2. Click "Run as administrator"

**Linux/Mac:**
```bash
sudo ./scripts/start_web_dashboard.sh
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

That's it! 🎉

---

## What You'll See

### 📊 Real-Time Dashboard
- **Live device counts** - See how many devices are connected right now
- **Device table** - All your network devices with status, IP, MAC address
- **Recent events** - Watch devices connect and disconnect in real-time
- **24-hour statistics** - Connection activity from the last day

### 🎮 Control Panel
- **Scan Now** - Trigger an immediate network scan
- **Start/Stop Monitoring** - Control the network monitor from your browser
- **Search & Filter** - Find devices quickly by name, IP, or MAC
- **Device Details** - Click any device to see its complete history

---

## Key Features

✅ **Auto-refresh every 5 seconds** - Always up-to-date  
✅ **Mobile-friendly** - Works on phones and tablets  
✅ **No configuration needed** - Works out of the box  
✅ **REST API included** - Build your own integrations  
✅ **Multiple viewing options** - Filter by connected/disconnected  

---

## What Files Were Added?

### Backend (Python/Flask)
- `src/network_monitor/web.py` - Flask app with API
- `src/network_monitor/web_main.py` - Startup script

### Frontend (HTML/CSS/JS)
- `templates/index.html` - Dashboard page
- `static/css/style.css` - Styling
- `static/js/main.js` - JavaScript functionality

### Scripts
- `scripts/start_web_dashboard.bat` - Windows launcher
- `scripts/start_web_dashboard.sh` - Linux/Mac launcher

### Documentation
- `WEB_DASHBOARD_GUIDE.md` - Complete guide
- `QUICKSTART_WEB_DASHBOARD.md` - Quick reference
- `WEB_DASHBOARD_IMPLEMENTATION.md` - Technical details

---

## Configuration (Optional)

You can customize the web dashboard by adding these to your `.env` file:

```env
# Web Dashboard Settings
WEB_HOST=0.0.0.0          # Listen on all interfaces (or 127.0.0.1 for localhost only)
WEB_PORT=5000             # Change port if needed
WEB_DEBUG=no              # Set to 'yes' for development
AUTO_START_MONITORING=yes # Auto-start network scanning
```

---

## Access from Other Devices

Want to check your network from your phone or tablet?

1. Find your computer's IP address:
   - Windows: Open cmd and type `ipconfig`
   - Linux/Mac: Type `ifconfig` or `ip addr`

2. On your mobile device, open browser and go to:
   ```
   http://YOUR-COMPUTER-IP:5000
   ```
   Example: `http://192.168.1.100:5000`

3. Make sure your device is on the same network!

---

## Troubleshooting

### Dashboard won't start?
- **Check**: Are you running as Administrator (Windows) or with sudo (Linux/Mac)?
- **Check**: Is port 5000 already in use? Change it in `.env`
- **Check**: Is SQL Server running and database set up?

### No devices showing?
- Click **"Scan Now"** to trigger a scan
- Make sure monitoring is active (green button)
- Verify your network subnet in `.env` matches your network

### Can't access from phone?
- Set `WEB_HOST=0.0.0.0` in `.env`
- Check your firewall allows port 5000
- Use your computer's IP, not "localhost"

---

## Using the API

The dashboard includes a REST API for custom integrations:

```bash
# Get current status
curl http://localhost:5000/api/status

# Get all devices
curl http://localhost:5000/api/devices

# Trigger a scan
curl -X POST http://localhost:5000/api/control/scan
```

See `WEB_DASHBOARD_GUIDE.md` for complete API documentation.

---

## Command-Line Monitor Still Works!

Don't worry - the original command-line monitor still works exactly as before:

```bash
# Windows
scripts\start_monitor.bat

# Linux/Mac
sudo ./scripts/start_monitor.sh
```

You can use either one, or run them both at the same time!

---

## Next Steps

1. **✅ Start the dashboard** and explore the interface
2. **📱 Try mobile access** from your phone
3. **🔍 Test device search** and filtering
4. **📊 Check out the statistics** after a few hours
5. **🎨 Customize** the `.env` file if needed

---

## Need More Help?

📖 **Detailed Documentation:**
- `WEB_DASHBOARD_GUIDE.md` - Complete feature guide
- `QUICKSTART_WEB_DASHBOARD.md` - Quick reference
- `README.md` - General setup instructions

🐛 **Troubleshooting:**
- Check `network_monitor.log` for error details
- Review the troubleshooting sections in the guides
- Verify all prerequisites are met

---

## 🎉 Enjoy Your New Dashboard!

You now have a modern, real-time web interface for monitoring your network. No more command-line only - monitor your network from any device with a browser!

**Happy Monitoring! 🌐📊**
