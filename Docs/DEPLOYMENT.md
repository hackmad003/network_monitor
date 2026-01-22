# Deployment Guide

Complete guide for deploying Network Monitor in various environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Development Deployment](#development-deployment)
- [Production Deployment](#production-deployment)
- [Windows Service](#windows-service)
- [Linux Service (systemd)](#linux-service-systemd)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python**: 3.8 or higher
- **SQL Server**: SQL Server 2017+ or SQL Server Express
- **RAM**: Minimum 512 MB (1 GB recommended)
- **Network**: Access to local network for scanning

### Software Dependencies
- **Python packages**: See requirements.txt
- **ODBC Driver**: ODBC Driver 17 for SQL Server
- **Packet capture**: Npcap (Windows) or libpcap (Linux/Mac)
- **Administrator privileges**: Required for network scanning

---

## Development Deployment

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/network-monitor.git
cd network-monitor
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Configure Environment
```bash
# Copy example configuration
cp config/env.example config/.env

# Edit configuration
# Windows: notepad config/.env
# Linux/Mac: nano config/.env
```

Update the following in `config/.env`:
```bash
NETWORK_SUBNET=192.168.1.0/24  # Your network subnet
SCAN_INTERVAL=60               # Scan frequency in seconds
SQL_SERVER=localhost           # Your SQL Server instance
SQL_DATABASE=NetworkMonitor
SQL_WINDOWS_AUTH=yes           # or 'no' for SQL authentication
```

### 5. Setup Database
```bash
# Open SQL Server Management Studio (SSMS)
# Connect to your SQL Server instance
# Open: config/database_setup.sql
# Execute the script (F5)
```

Or via command line:
```bash
sqlcmd -S localhost -i config/database_setup.sql
```

### 6. Run Application
```bash
# Windows (as Administrator)
python -m network_monitor.main

# Linux/Mac (with sudo)
sudo python -m network_monitor.main
```

---

## Production Deployment

### Installation as Package

```bash
# Install in development mode (editable)
pip install -e .

# Or install normally
pip install .

# Run the installed command
network-monitor
```

### Configuration Management

For production, use environment-specific `.env` files:

```bash
config/
├── .env.development
├── .env.staging
├── .env.production
```

Load specific environment:
```bash
export ENV_FILE=config/.env.production
```

### Security Best Practices

1. **Use Windows Authentication** (when possible)
   ```bash
   SQL_WINDOWS_AUTH=yes
   ```

2. **Secure .env files**
   ```bash
   chmod 600 config/.env
   ```

3. **Use SQL Service Account** (for SQL Auth)
   - Create dedicated SQL user with minimal privileges
   - Grant only necessary permissions:
     ```sql
     GRANT SELECT, INSERT, UPDATE ON NetworkMonitor.* TO 'monitor_user';
     ```

4. **Restrict Network Access**
   - Limit scanning to specific subnet
   - Use firewall rules to restrict database access

---

## Windows Service

### Using NSSM (Non-Sucking Service Manager)

#### 1. Download NSSM
Download from: https://nssm.cc/download

#### 2. Install Service
```powershell
# Run PowerShell as Administrator
cd C:\path\to\nssm

.\nssm.exe install NetworkMonitor "C:\path\to\python.exe" "-m network_monitor.main"
```

#### 3. Configure Service
```powershell
# Set working directory
.\nssm.exe set NetworkMonitor AppDirectory "C:\path\to\network-monitor"

# Set environment file
.\nssm.exe set NetworkMonitor AppEnvironmentExtra "DOTENV_PATH=C:\path\to\network-monitor\config\.env"

# Set description
.\nssm.exe set NetworkMonitor Description "Network Device Monitor Service"

# Set startup type (automatic)
.\nssm.exe set NetworkMonitor Start SERVICE_AUTO_START

# Set log files
.\nssm.exe set NetworkMonitor AppStdout "C:\path\to\logs\service.log"
.\nssm.exe set NetworkMonitor AppStderr "C:\path\to\logs\service-error.log"
```

#### 4. Start Service
```powershell
.\nssm.exe start NetworkMonitor

# Check status
.\nssm.exe status NetworkMonitor

# Stop service
.\nssm.exe stop NetworkMonitor

# Remove service
.\nssm.exe remove NetworkMonitor confirm
```

### Using Task Scheduler

#### 1. Create Batch Script
Create `C:\NetworkMonitor\run_monitor.bat`:
```batch
@echo off
cd C:\path\to\network-monitor
call venv\Scripts\activate
python -m network_monitor.main
```

#### 2. Create Scheduled Task
```powershell
$action = New-ScheduledTaskAction -Execute "C:\NetworkMonitor\run_monitor.bat"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "NetworkMonitor" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Network Device Monitor"
```

---

## Linux Service (systemd)

### 1. Create Service File
Create `/etc/systemd/system/network-monitor.service`:

```ini
[Unit]
Description=Network Device Monitor
After=network.target mssql-server.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/network-monitor
Environment="PATH=/opt/network-monitor/venv/bin"
ExecStart=/opt/network-monitor/venv/bin/python -m network_monitor.main
Restart=always
RestartSec=10
StandardOutput=append:/var/log/network-monitor/service.log
StandardError=append:/var/log/network-monitor/service-error.log

[Install]
WantedBy=multi-user.target
```

### 2. Setup Log Directory
```bash
sudo mkdir -p /var/log/network-monitor
sudo chmod 755 /var/log/network-monitor
```

### 3. Enable and Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start at boot)
sudo systemctl enable network-monitor

# Start service
sudo systemctl start network-monitor

# Check status
sudo systemctl status network-monitor

# View logs
sudo journalctl -u network-monitor -f

# Stop service
sudo systemctl stop network-monitor

# Restart service
sudo systemctl restart network-monitor
```

### 4. Log Rotation
Create `/etc/logrotate.d/network-monitor`:

```
/var/log/network-monitor/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 root root
}
```

---

## Docker Deployment

### 1. Create Dockerfile
Create `Dockerfile` in project root:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Microsoft ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create volume for configuration
VOLUME ["/app/config"]

# Run as root (required for network scanning)
USER root

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "-m", "network_monitor.main"]
```

### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  network-monitor:
    build: .
    container_name: network-monitor
    network_mode: host
    privileged: true  # Required for network scanning
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - DOTENV_PATH=/app/config/.env
    restart: unless-stopped
    depends_on:
      - sqlserver

  sqlserver:
    image: mcr.microsoft.com/mssql/server:2019-latest
    container_name: sqlserver
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong!Passw0rd
    ports:
      - "1433:1433"
    volumes:
      - sqldata:/var/opt/mssql

volumes:
  sqldata:
```

### 3. Build and Run
```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f network-monitor

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## Troubleshooting

### Permission Errors

**Problem**: "Permission denied" when scanning network

**Solution**:
- Windows: Run as Administrator
- Linux/Mac: Run with sudo or set capabilities
  ```bash
  sudo setcap cap_net_raw+ep $(which python)
  ```

### Database Connection Errors

**Problem**: Cannot connect to SQL Server

**Solutions**:
1. Verify SQL Server is running:
   ```bash
   # Windows
   services.msc → SQL Server (SQLEXPRESS)
   
   # Linux
   sudo systemctl status mssql-server
   ```

2. Check connection string in `.env`
3. Test connection with sqlcmd:
   ```bash
   sqlcmd -S localhost -U sa -P YourPassword
   ```

4. Verify ODBC driver installation:
   ```bash
   # Windows
   odbcad32
   
   # Linux
   odbcinst -j
   ```

### No Devices Found

**Problem**: Scan completes but finds no devices

**Solutions**:
1. Verify correct subnet in `.env`
   ```bash
   # Find your subnet
   # Windows: ipconfig
   # Linux: ip addr show
   ```

2. Check firewall settings
3. Increase scan timeout:
   ```bash
   SCAN_TIMEOUT=5
   ```

4. Test manually:
   ```bash
   ping 192.168.1.1
   arp -a
   ```

### Service Won't Start

**Problem**: Service fails to start at boot

**Solutions**:
1. Check service logs
2. Verify paths in service configuration
3. Ensure database is available before starting
4. Check dependencies (SQL Server service)

### High CPU/Memory Usage

**Problem**: Application consuming too many resources

**Solutions**:
1. Increase scan interval:
   ```bash
   SCAN_INTERVAL=300  # 5 minutes
   ```

2. Reduce subnet size:
   ```bash
   NETWORK_SUBNET=192.168.1.0/25  # Smaller range
   ```

3. Check for database locks or slow queries
4. Monitor with:
   ```bash
   # Windows
   perfmon
   
   # Linux
   top -p $(pgrep -f network_monitor)
   ```

---

## Maintenance

### Database Maintenance

**Cleanup old logs**:
```sql
-- Delete logs older than 90 days
DELETE FROM ConnectionLog 
WHERE EventTime < DATEADD(day, -90, GETDATE());

-- Vacuum/shrink database
DBCC SHRINKDATABASE (NetworkMonitor);
```

**Backup database**:
```sql
BACKUP DATABASE NetworkMonitor 
TO DISK = 'C:\Backups\NetworkMonitor.bak';
```

### Log Management

**Rotate logs** (if not using logrotate):
```bash
mv network_monitor.log network_monitor.log.1
touch network_monitor.log
systemctl restart network-monitor
```

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart network-monitor
```

---

## Monitoring

### Health Checks

Create a simple health check script:
```python
# health_check.py
from network_monitor.database import DatabaseManager
from network_monitor.config import DatabaseConfig

try:
    config = DatabaseConfig.from_env()
    db = DatabaseManager(config)
    counts = db.get_device_count()
    print(f"OK: {counts['connected']} devices connected")
    exit(0)
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
```

### Nagios/Icinga Integration
```bash
# /usr/lib/nagios/plugins/check_network_monitor
#!/bin/bash
cd /opt/network-monitor
source venv/bin/activate
python health_check.py
```

### Prometheus Metrics

Future enhancement - expose metrics endpoint:
- `network_monitor_devices_connected`
- `network_monitor_scan_duration_seconds`
- `network_monitor_last_scan_timestamp`
