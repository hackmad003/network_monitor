# Migration Guide

Guide for migrating from the original single-file version to the new modular structure.

## Overview

The Network Monitor has been refactored from a single `network_monitor.py` file into a professional, modular package structure. This guide helps you transition smoothly.

## What Changed?

### File Structure

**Before**:
```
network-monitor/
├── network_monitor.py          # Single 260-line file
├── database_setup.sql
├── .env
├── env.example
└── requirements.txt
```

**After**:
```
network-monitor/
├── src/network_monitor/        # Modular package
│   ├── config.py               # Configuration
│   ├── scanner.py              # Network scanning
│   ├── database.py             # Database operations
│   ├── monitor.py              # Orchestration
│   └── main.py                 # Entry point
├── config/                     # Configuration files
│   ├── .env
│   ├── env.example
│   └── database_setup.sql
├── docs/                       # Documentation
├── scripts/                    # Helper scripts
└── tests/                      # Test suite
```

## Migration Steps

### Step 1: Backup Current Setup

```bash
# Backup your configuration
cp .env .env.backup

# Backup your log file (if you want to keep history)
cp network_monitor.log network_monitor.log.backup

# Backup the old script
cp network_monitor.py network_monitor.py.backup
```

### Step 2: Pull New Code

```bash
# If using git
git pull origin main

# Or download the new version
```

### Step 3: Move Configuration

The new structure keeps configuration files in the `config/` directory:

```bash
# Move your .env file
mv .env config/.env

# Verify it's correct
cat config/.env
```

Your `.env` file doesn't need any changes - all settings remain the same!

### Step 4: Update Python Environment

```bash
# Activate your virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Optional: Install as a package
pip install -e .
```

### Step 5: Update How You Run It

**Old way**:
```bash
python network_monitor.py
```

**New way** (choose one):
```bash
# Option 1: Run as module
python -m network_monitor.main

# Option 2: Use the helper scripts
# Windows:
scripts\start_monitor.bat
# Linux/Mac:
sudo scripts/start_monitor.sh

# Option 3: If installed as package
network-monitor
```

### Step 6: Update Custom Scripts (If Any)

If you have custom scripts that import the old code:

**Old code**:
```python
from network_monitor import NetworkMonitor

monitor = NetworkMonitor()
monitor.run()
```

**New code** (same, but imports from package):
```python
from network_monitor import NetworkMonitor

monitor = NetworkMonitor()
monitor.run()
```

The API is backward compatible! Your code should work without changes.

### Step 7: Update Services (If Running as Service)

#### Windows Service (NSSM)

Update the executable path:

```powershell
# Stop service
nssm stop NetworkMonitor

# Update path
nssm set NetworkMonitor Application "C:\path\to\python.exe"
nssm set NetworkMonitor AppParameters "-m network_monitor.main"
nssm set NetworkMonitor AppDirectory "C:\path\to\network-monitor"

# Restart service
nssm start NetworkMonitor
```

#### Linux Systemd Service

Update `/etc/systemd/system/network-monitor.service`:

```ini
[Service]
# Old:
# ExecStart=/opt/network-monitor/venv/bin/python network_monitor.py

# New:
ExecStart=/opt/network-monitor/venv/bin/python -m network_monitor.main
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart network-monitor
```

## Compatibility

### ✅ Backward Compatible

- **Configuration**: `.env` file format unchanged
- **Database**: Same schema, no migrations needed
- **API**: Main classes have same interface
- **Logging**: Same log format and location

### ⚠️ Breaking Changes

Only one breaking change:

**Import path for advanced usage**:
```python
# Old (won't work):
from network_monitor import NetworkMonitor

# New:
from network_monitor import NetworkMonitor  # Actually the same!
# Or more specific:
from network_monitor.monitor import NetworkMonitor
```

Actually, there are **NO breaking changes** for normal usage! 🎉

## Verification

After migration, verify everything works:

### 1. Check Configuration
```bash
cat config/.env
# Ensure all your settings are correct
```

### 2. Test Database Connection
```bash
# Try a single scan
python -m network_monitor.main
# Press Ctrl+C after one scan completes
```

### 3. Check Logs
```bash
# View the log
tail -f network_monitor.log

# Or on Windows:
type network_monitor.log
```

### 4. Verify Database
```sql
-- In SQL Server Management Studio
SELECT COUNT(*) FROM NetworkMonitor.dbo.DeviceConnections;
SELECT TOP 10 * FROM NetworkMonitor.dbo.ConnectionLog ORDER BY EventTime DESC;
```

## Troubleshooting

### Issue: "Module not found"

**Problem**: 
```
ModuleNotFoundError: No module named 'network_monitor'
```

**Solution**:
```bash
# Make sure you're in the right directory
cd /path/to/network-monitor

# Reinstall dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Issue: "Can't find .env file"

**Problem**: Configuration not loading

**Solution**:
```bash
# Ensure .env is in config/ directory
ls config/.env

# If not, move it
mv .env config/.env

# Or copy from example
cp config/env.example config/.env
```

### Issue: Old network_monitor.py still exists

**Problem**: Confusion about which file to use

**Solution**:
```bash
# Rename the old file (don't delete yet)
mv network_monitor.py network_monitor.py.old

# Use the new structure
python -m network_monitor.main
```

After confirming everything works, you can delete `network_monitor.py.old`.

### Issue: Import errors in custom scripts

**Problem**:
```python
ImportError: cannot import name 'NetworkMonitor'
```

**Solution**:
```python
# Make sure you're importing correctly
from network_monitor import NetworkMonitor  # Correct

# Not from the old file
# from network_monitor import NetworkMonitor  # Old way
```

The package structure handles the imports automatically.

## Rollback Plan

If you need to rollback:

### 1. Restore Old Files
```bash
# Restore old script
cp network_monitor.py.backup network_monitor.py

# Restore old .env location
cp config/.env .env
```

### 2. Run Old Version
```bash
python network_monitor.py
```

### 3. Report Issues
Please report any migration issues on GitHub so we can help!

## Benefits of New Structure

### For Users
- ✅ Same functionality, better organized
- ✅ Easier to understand and maintain
- ✅ Better error messages
- ✅ Comprehensive documentation

### For Developers
- ✅ Testable components
- ✅ Type hints for IDE support
- ✅ Modular architecture
- ✅ Easy to extend

### For Operations
- ✅ Better logging
- ✅ Health check support
- ✅ Docker deployment option
- ✅ Service deployment guides

## Need Help?

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Documentation**: See [docs/](docs/) directory
- **Issues**: Create a GitHub issue
- **Questions**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Summary

The migration is simple:
1. ✅ Move `.env` to `config/.env`
2. ✅ Run with `python -m network_monitor.main`
3. ✅ Everything else works the same!

No database changes, no configuration format changes, no breaking changes to core functionality.

Happy monitoring! 🎉
