# QUICK START CHECKLIST

Follow these steps in order. Check off each one as you complete it!

## Before You Start
- [ ] Install Python 3.8+ (https://www.python.org/downloads/)
     - ⚠️ Check "Add Python to PATH" during installation!
- [ ] Install SQL Server Express (https://www.microsoft.com/en-us/sql-server/sql-server-downloads)
- [ ] Install SSMS (https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)
- [ ] Install ODBC Driver 17 (https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [ ] Install Npcap (https://npcap.com/#download)

## Setup Steps (15 minutes)

### 1. Install Python Packages
- [ ] Open VS Code
- [ ] Open Terminal (Ctrl + `)
- [ ] Run: `pip install -r requirements.txt`

### 2. Create Database
- [ ] Open SSMS
- [ ] Connect to `localhost` or `.\SQLEXPRESS`
- [ ] Open `database_setup.sql`
- [ ] Click "Execute" (F5)
- [ ] Wait for "Database setup complete!" message

### 3. Configure Settings
- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` in VS Code
- [ ] Set your `NETWORK_SUBNET` (probably 192.168.1.0/24)
  - To find: Open cmd, type `ipconfig`, look at your IP address
- [ ] Save the file

### 4. Run the Monitor
- [ ] Close VS Code
- [ ] Right-click VS Code → "Run as administrator"
- [ ] Open Terminal
- [ ] Run: `python network_monitor.py`
- [ ] You should see devices being detected!

### 5. Verify It's Working
- [ ] Open SSMS
- [ ] Navigate to: NetworkMonitor → Tables → DeviceConnections
- [ ] Right-click → "Select Top 1000 Rows"
- [ ] See your devices listed? ✅ You're done!

## Connect Power BI (Optional)
- [ ] Download Power BI Desktop (https://powerbi.microsoft.com/desktop/)
- [ ] Open Power BI
- [ ] Get Data → SQL Server
- [ ] Server: `localhost`, Database: `NetworkMonitor`
- [ ] Select all tables/views
- [ ] Create your visualizations!

---

## 🆘 Need Help?

**Can't connect to database?**
→ Check SQL Server is running in Services

**Permission denied?**
→ Run VS Code as administrator

**No devices found?**
→ Check your NETWORK_SUBNET setting

**More help?**
→ See the full README.md file

---

## Quick Commands

```bash
# Install packages
pip install -r requirements.txt

# Run monitor
python network_monitor.py

# Check Python version
python --version

# Check if packages installed
pip list
```

---

Good luck! 🚀
