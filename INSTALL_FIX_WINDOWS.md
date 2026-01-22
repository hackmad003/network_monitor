# Fix Installation Issues on Windows

## Problem
You're getting errors installing `pyodbc` and `scapy`, and module import errors.

## Solution - Step by Step

### Step 1: Install pyodbc (Pre-built Wheel)

The issue is that `pyodbc` needs to be compiled, but it's failing. Use the pre-built wheel instead:

```powershell
pip install pyodbc --only-binary :all:
```

If that doesn't work, try:
```powershell
pip install pyodbc --prefer-binary
```

Or download the wheel directly from: https://pypi.org/project/pyodbc/#files
And install with: `pip install pyodbc-5.0.1-cp312-cp312-win_amd64.whl` (adjust version to match your Python)

### Step 2: Install Scapy

Scapy on Windows needs Npcap (WinPcap replacement):

1. **Download and Install Npcap:**
   - Go to: https://npcap.com/#download
   - Download Npcap installer
   - Run installer with **"WinPcap API-compatible Mode"** checked
   - Restart your computer after installation

2. **Install Scapy:**
   ```powershell
   pip install scapy
   ```

### Step 3: Install Other Dependencies

```powershell
pip install flask flask-cors python-dotenv
```

### Step 4: Verify Installation

```powershell
python -c "import pyodbc; print('pyodbc OK')"
python -c "import scapy; print('scapy OK')"
python -c "import flask; print('flask OK')"
```

All three should print "OK".

## Alternative: Install All at Once

Try this command which forces binary wheels where possible:

```powershell
pip install --prefer-binary -r requirements.txt
```

## If Still Having Issues

### Option 1: Use Conda (Recommended for Windows)

```powershell
conda install -c conda-forge pyodbc scapy flask flask-cors python-dotenv
```

### Option 2: Install Only What You Need

If you just want to test the web dashboard without actual scanning:

```powershell
pip install flask flask-cors python-dotenv
```

Then run the web server in "demo mode" (we'll create this).

## Check Your Python Version

```powershell
python --version
```

Make sure you're using Python 3.8 - 3.12 (3.14 might be too new for some packages).
