# Network Monitor - Web Dashboard Guide

## Overview

The Network Monitor now includes a modern web dashboard that provides real-time monitoring and visualization of your network devices. The dashboard offers an intuitive interface to view connected devices, track connection history, and monitor network activity.

## Features

### 🎯 Key Features

- **Real-Time Monitoring**: Automatic updates every 5 seconds showing current network status
- **Device Management**: View all network devices with detailed information
- **Connection History**: Track device connections and disconnections over time
- **Statistics Dashboard**: View 24-hour connection statistics and trends
- **Manual Scanning**: Trigger immediate network scans on demand
- **Device Details**: Drill down into individual device connection history
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### 📊 Dashboard Components

1. **Status Bar**: Shows monitoring status, network subnet, and scan interval
2. **Statistics Cards**: Quick overview of connected devices, total devices, and 24h activity
3. **Device Table**: Comprehensive list of all network devices with filtering and search
4. **Recent Events**: Live feed of connection and disconnection events
5. **Device Details Modal**: Detailed information and connection history for each device

## Installation

### 1. Install Required Dependencies

The web dashboard requires Flask and Flask-CORS. Install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Web Settings (Optional)

Add these settings to your `.env` file to customize the web dashboard:

```env
# Web Dashboard Settings
WEB_HOST=0.0.0.0          # Host address (0.0.0.0 = all interfaces)
WEB_PORT=5000             # Port number
WEB_DEBUG=no              # Enable debug mode (yes/no)
AUTO_START_MONITORING=yes # Auto-start network monitoring (yes/no)
```

If not specified, the dashboard will use default values.

## Starting the Web Dashboard

### On Windows

**Option 1: Using the Startup Script (Recommended)**

1. Right-click `scripts/start_web_dashboard.bat`
2. Select "Run as administrator"

**Option 2: Manual Start**

Open Command Prompt as Administrator and run:

```cmd
python -m src.network_monitor.web_main
```

### On Linux/Mac

**Option 1: Using the Startup Script (Recommended)**

```bash
sudo ./scripts/start_web_dashboard.sh
```

**Option 2: Manual Start**

```bash
sudo python -m src.network_monitor.web_main
```

### Important Notes

- ⚠️ **Administrator/root privileges are required** for network scanning
- The dashboard will automatically start network monitoring by default
- The original command-line monitor can still be used independently

## Accessing the Dashboard

Once started, open your web browser and navigate to:

```
http://localhost:5000
```

Or from another device on the same network:

```
http://[your-server-ip]:5000
```

## Using the Dashboard

### Main Controls

**Scan Now Button**
- Triggers an immediate network scan
- Updates the dashboard with latest device information
- Useful for getting fresh data without waiting for the next scheduled scan

**Start/Stop Monitoring Button**
- Toggles automatic network monitoring on/off
- When active, scans run at the configured interval (default: 60 seconds)
- Green = Running, Gray = Stopped

### Device Table

**Features:**
- **Status Column**: Shows connected (green) or disconnected (red) status
- **Search Box**: Filter devices by name, IP, MAC, or hostname
- **Filter Dropdown**: Show all devices, connected only, or disconnected only
- **Info Button**: Click to view detailed device information

**Device Information:**
- Device name/hostname
- IP address (current or last known)
- MAC address
- Last seen timestamp
- Connection status

### Recent Events

Shows the latest 20 connection/disconnection events with:
- Event type (Connected/Disconnected)
- Device information
- Timestamp
- IP address

### Device Details Modal

Click the info button (ℹ️) on any device to view:
- Complete device information
- Device type and vendor (if available)
- First seen and last seen timestamps
- Full connection history (last 100 events)

## API Endpoints

The web dashboard provides a REST API for integration with other tools:

### Status & Control

- `GET /api/status` - Get current monitoring status
- `POST /api/control/start` - Start network monitoring
- `POST /api/control/stop` - Stop network monitoring
- `POST /api/control/scan` - Trigger immediate scan

### Device Information

- `GET /api/devices` - Get all devices
- `GET /api/devices/connected` - Get only connected devices
- `GET /api/device/<mac_address>` - Get specific device details

### Statistics & Events

- `GET /api/statistics` - Get network statistics
- `GET /api/events?limit=50` - Get recent events (default limit: 50)

### Example API Usage

```bash
# Get current status
curl http://localhost:5000/api/status

# Trigger a scan
curl -X POST http://localhost:5000/api/control/scan

# Get all connected devices
curl http://localhost:5000/api/devices/connected
```

## Running Both Monitor and Web Dashboard

You have several options for running the network monitor:

### Option 1: Web Dashboard Only (Recommended)
- Start the web dashboard with auto-monitoring enabled
- Manages everything through the web interface
- Best for most users

```bash
# Windows (as Administrator)
scripts\start_web_dashboard.bat

# Linux/Mac (with sudo)
sudo ./scripts/start_web_dashboard.sh
```

### Option 2: Command-Line Monitor Only
- Traditional command-line interface
- No web dashboard
- Best for servers without web access

```bash
# Windows (as Administrator)
scripts\start_monitor.bat

# Linux/Mac (with sudo)
sudo ./scripts/start_monitor.sh
```

### Option 3: Both Running Separately
- Run web dashboard with auto-monitoring disabled
- Run command-line monitor separately
- Both access the same database

```bash
# In .env file
AUTO_START_MONITORING=no

# Terminal 1 - Start web dashboard
python -m src.network_monitor.web_main

# Terminal 2 - Start monitor
python -m src.network_monitor.main
```

## Troubleshooting

### Dashboard Won't Start

**Problem**: "Permission Denied" error
- **Solution**: Make sure you're running as Administrator (Windows) or with sudo (Linux/Mac)

**Problem**: "Port already in use" error
- **Solution**: Change the port in your `.env` file: `WEB_PORT=5001`

**Problem**: "Database connection error"
- **Solution**: Verify SQL Server is running and database is set up (see main README.md)

### Dashboard Shows No Data

**Problem**: No devices displayed
- **Solution**: 
  1. Check that monitoring is active (green Start/Stop button)
  2. Trigger a manual scan using "Scan Now" button
  3. Verify your network subnet is correct in `.env` file

**Problem**: "Failed to load devices" error
- **Solution**: Check that the database is accessible and contains the required tables

### Scanning Issues

**Problem**: Scan fails or returns no devices
- **Solution**:
  1. Verify you have administrator/root privileges
  2. Check firewall settings aren't blocking ARP packets
  3. Ensure the subnet setting matches your network

### Browser Issues

**Problem**: Dashboard doesn't update
- **Solution**: 
  1. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
  2. Clear browser cache
  3. Check browser console for JavaScript errors

**Problem**: Can't access from another device
- **Solution**:
  1. Verify `WEB_HOST=0.0.0.0` in `.env` file
  2. Check firewall allows connections on port 5000
  3. Use the server's IP address, not localhost

## Security Considerations

### Network Access

- By default, the dashboard is accessible from any network interface
- To restrict to localhost only, set `WEB_HOST=127.0.0.1`
- Consider using a reverse proxy (nginx/Apache) with authentication for production

### Database Security

- The dashboard uses the same database credentials as the monitor
- Ensure your SQL Server credentials are secure
- Use Windows Authentication when possible

### Firewall Rules

- The web dashboard listens on port 5000 by default
- Configure firewall rules based on your security requirements
- Only open the port to trusted networks

## Performance Tips

1. **Adjust Refresh Interval**: The dashboard auto-refreshes every 5 seconds. This is configurable in `static/js/main.js`

2. **Scan Interval**: For large networks, increase the scan interval in `.env`:
   ```env
   SCAN_INTERVAL=300  # 5 minutes
   ```

3. **Event History**: The dashboard loads the last 20 events. Increase the limit if needed via the API

4. **Browser Performance**: For best performance, use modern browsers (Chrome, Firefox, Edge)

## Advanced Configuration

### Custom Styling

Modify `static/css/style.css` to customize colors and appearance:

```css
:root {
    --primary-color: #2563eb;  /* Change to your brand color */
    --success-color: #10b981;
    --danger-color: #ef4444;
}
```

### Dashboard Refresh Rate

Edit `static/js/main.js` to change auto-refresh interval:

```javascript
const REFRESH_INTERVAL = 10000; // 10 seconds (default: 5000)
```

### Event History Limit

Change the number of events displayed:

```javascript
// In static/js/main.js
async function loadEvents() {
    const response = await fetch('/api/events?limit=50'); // Default: 20
    // ...
}
```

## Integration Examples

### Power BI Integration

Use the API endpoints to create custom Power BI dashboards:

1. Use "Get Data" → "Web"
2. Enter API endpoint: `http://localhost:5000/api/devices`
3. Schedule automatic refresh

### Custom Monitoring Scripts

```python
import requests

# Get current device count
response = requests.get('http://localhost:5000/api/status')
data = response.json()
print(f"Connected devices: {data['connected_devices']}")

# Trigger a scan
requests.post('http://localhost:5000/api/control/scan')
```

### Webhook Notifications (Future Enhancement)

The API can be extended to support webhook notifications for device events.

## Support

For issues or questions:
1. Check the main `README.md` for general setup issues
2. Review the `network_monitor.log` file for detailed error messages
3. Verify all prerequisites are installed and configured

## Version Information

- Web Dashboard Version: 1.0.0
- Flask Version: 3.0.0
- Compatible with Network Monitor v1.0+

---

**Happy Monitoring! 🌐📊**
