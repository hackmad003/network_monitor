# 🚀 Start the Web Dashboard - Simple Instructions

## Step-by-Step Guide

### Step 1: Install Required Packages

Open your terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs Flask and other needed packages. You only need to do this once.

---

### Step 2: Start the Server

**IMPORTANT:** You need administrator/root privileges because the network scanner needs special permissions.

#### On Windows:

**Option A: Using the Script (Easiest)**
1. Find the file: `scripts/start_web_dashboard.bat`
2. **Right-click** on it
3. Select **"Run as administrator"**
4. A window will open showing the server starting

**Option B: Using Command Prompt**
1. Right-click on **Command Prompt** or **PowerShell**
2. Select **"Run as administrator"**
3. Navigate to your project folder:
   ```cmd
   cd C:\path\to\your\project
   ```
4. Run:
   ```cmd
   python -m src.network_monitor.web_main
   ```

#### On Linux/Mac:

**Option A: Using the Script (Easiest)**
```bash
sudo ./scripts/start_web_dashboard.sh
```

**Option B: Direct Python Command**
```bash
sudo python -m src.network_monitor.web_main
```

---

### Step 3: Open in Your Browser

Once the server starts, you'll see a message like:

```
========================================
🌐 Open your browser and navigate to: http://localhost:5000
========================================
```

Now open your web browser and go to:

```
http://localhost:5000
```

That's it! You should see the dashboard! 🎉

---

## Quick Troubleshooting

### "Permission Denied" Error
**Solution:** You forgot to run as administrator/sudo. Go back to Step 2 and make sure you're using admin rights.

### "Port 5000 is already in use"
**Solution:** Something else is using port 5000. Either:
1. Stop that other application, OR
2. Create a `.env` file (copy from `config/env.example`) and change the port:
   ```env
   WEB_PORT=5001
   ```
   Then use `http://localhost:5001` instead

### "Module not found" Error
**Solution:** Install dependencies again:
```bash
pip install flask flask-cors scapy pyodbc python-dotenv
```

### "Database connection error"
**Solution:** Make sure:
1. SQL Server is running
2. You've run the `config/database_setup.sql` script
3. Your `.env` file has correct database settings

### Server starts but browser shows "Can't connect"
**Solution:** 
1. Make sure you're using the correct URL: `http://localhost:5000`
2. Check that the server is actually running (terminal should show "Running on...")
3. Try `http://127.0.0.1:5000` instead

---

## What You Should See

When the server starts successfully, you'll see:
```
========================================
Network Device Monitor - Web Dashboard
========================================

✓ Configuration loaded
✓ Monitoring network: 192.168.1.0/24
✓ Scan interval: 60 seconds
✓ Web server starting on http://0.0.0.0:5000

========================================
🌐 Open your browser and navigate to: http://localhost:5000
========================================

✓ Network monitoring will start automatically

Press Ctrl+C to stop the server
```

In your browser, you'll see:
- Network Device Monitor header
- Statistics cards showing device counts
- A table of network devices
- Recent events panel
- Control buttons (Scan Now, Start/Stop)

---

## Testing Without Admin Rights (For Testing Only)

If you just want to see the web interface without actually scanning:

1. Create/edit `.env` file and add:
   ```env
   AUTO_START_MONITORING=no
   ```

2. Start normally (no admin needed):
   ```bash
   python -m src.network_monitor.web_main
   ```

3. Open browser to `http://localhost:5000`

This lets you see the interface, but scanning won't work until you run with admin privileges.

---

## Stopping the Server

To stop the server:
- Press **Ctrl+C** in the terminal/command prompt window

---

## Access from Your Phone/Tablet

1. Start the server on your computer (as described above)

2. Find your computer's IP address:
   - **Windows:** Open cmd and type `ipconfig` (look for IPv4 Address)
   - **Mac/Linux:** Type `ifconfig` or `ip addr`

3. On your phone/tablet, open browser and go to:
   ```
   http://YOUR-COMPUTER-IP:5000
   ```
   Example: `http://192.168.1.100:5000`

4. Make sure your phone is on the same WiFi network!

---

## Need More Help?

- Check `network_monitor.log` for error messages
- See `WEB_DASHBOARD_GUIDE.md` for detailed documentation
- See `QUICKSTART_WEB_DASHBOARD.md` for quick reference

---

**Happy Monitoring! 🌐📊**
