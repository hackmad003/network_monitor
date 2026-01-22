# Installation Guide for Python 3.14 on Windows

## Your Situation
- ✅ Python 3.14.2 installed
- ❌ pyodbc won't install (needs compilation)
- ❌ scapy not installed yet (needs Npcap)
- ✅ You want to see the web dashboard

## Solution: Two Paths

---

## 🚀 PATH 1: Test the Dashboard NOW (Recommended to Start)

This lets you see the web interface immediately with mock data.

### Step 1: Install Flask
```powershell
pip install flask flask-cors
```

### Step 2: Run the Test Server
```powershell
python test_web_only.py
```

OR just double-click: **`START_WEB_TEST.bat`**

### Step 3: Open Browser
Go to: **http://localhost:5000**

You'll see the dashboard with sample devices - this shows you what it looks like!

---

## 🔧 PATH 2: Full Installation (For Real Network Monitoring)

This is the complete setup for actual network monitoring.

### Prerequisites

#### 1. Install Npcap (Required for Scapy)
1. Download from: https://npcap.com/#download
2. Run installer **as Administrator**
3. **IMPORTANT**: Check the box "Install Npcap in WinPcap API-compatible Mode"
4. Complete installation
5. **Restart your computer**

#### 2. Install Visual C++ Build Tools (Required for pyodbc)

**Option A: Install just the build tools**
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer
3. Select "Desktop development with C++"
4. Install (this takes a while)

**Option B: You already have Visual Studio 2022**
You have VS 2022, but pip might not find it. Try:
```powershell
# Use the Visual Studio command prompt
# Or set the environment variable
set DISTUTILS_USE_SDK=1
```

### Step-by-Step Installation

Run these commands in PowerShell **as Administrator**:

#### 1. Install Flask (Web Framework)
```powershell
pip install flask flask-cors python-dotenv
```

#### 2. Install pyodbc (Database)
```powershell
# Try the simple way first
pip install pyodbc

# If that fails, try forcing a rebuild
pip install --no-cache-dir --force-reinstall pyodbc

# If still fails, download pre-built wheel
# Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyodbc
# Download the .whl file for Python 3.14
# Then: pip install pyodbc-5.0.1-cp314-cp314-win_amd64.whl
```

#### 3. Install Scapy (Network Scanner)
After installing Npcap and restarting:
```powershell
pip install scapy
```

#### 4. Test Installation
```powershell
python -c "import flask; print('Flask: OK')"
python -c "import pyodbc; print('pyodbc: OK')"
python -c "import scapy; print('scapy: OK')"
```

### If pyodbc Still Fails

**Alternative 1: Use ODBC Driver Directly**
Windows has a built-in ODBC driver. You might not need pyodbc compilation if you:
- Download pre-built wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyodbc
- Or use conda: `conda install pyodbc`

**Alternative 2: Use SQLite Instead**
We could modify the code to use SQLite (built into Python) instead of SQL Server.

---

## 🎯 Recommended Approach

### For Testing (Right Now):
1. Run `pip install flask flask-cors`
2. Run `python test_web_only.py`
3. See the dashboard at http://localhost:5000

### For Production (When Ready):
1. Install Npcap first (requires restart)
2. Try `pip install pyodbc scapy python-dotenv`
3. If pyodbc fails, download pre-built wheel
4. Configure `.env` file with database settings
5. Run the full version

---

## Troubleshooting

### "pip is not recognized"
Make sure Python is in your PATH. Try:
```powershell
python -m pip install flask flask-cors
```

### "Access denied" when installing
Run PowerShell as Administrator:
- Right-click PowerShell
- Select "Run as administrator"

### pyodbc compile error persists
You have three options:
1. Download pre-built wheel from unofficial binaries
2. Use Anaconda: `conda install pyodbc`
3. Use Python 3.11 or 3.12 (more stable, more wheels available)

### Scapy "No module named 'scapy.libs'" 
Npcap is not installed or not installed correctly:
1. Uninstall Npcap
2. Reinstall with "WinPcap API-compatible Mode" checked
3. Restart computer
4. Reinstall scapy: `pip uninstall scapy && pip install scapy`

---

## Quick Commands Summary

### Test Mode (No Dependencies):
```powershell
pip install flask flask-cors
python test_web_only.py
```

### Full Installation:
```powershell
# 1. Install Npcap from https://npcap.com (restart after)
# 2. Then:
pip install flask flask-cors python-dotenv
pip install pyodbc
pip install scapy
```

### Verify:
```powershell
python -c "import flask, flask_cors, pyodbc, scapy; print('All OK!')"
```

---

## Alternative: Use Python 3.11 or 3.12

Python 3.14 is very new. If you keep having issues, consider:

1. Download Python 3.11 or 3.12 from python.org
2. Install alongside 3.14 (different directory)
3. Create virtual environment with specific version:
   ```powershell
   py -3.11 -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

Most packages have stable wheels for Python 3.11 and 3.12.

---

## What to Do Next

1. **Try the test version first** - see if you like the dashboard
2. **Install Npcap** (download and restart)
3. **Fix pyodbc** (try pre-built wheel or conda)
4. **Run full version** when all dependencies work

Need help? Check:
- `network_monitor.log` for error details
- This guide for specific error solutions
- Python package documentation for your versions
