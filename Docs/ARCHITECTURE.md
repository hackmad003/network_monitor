# Network Monitor Architecture

## Overview

Network Monitor is a Python-based application that continuously scans a local network, tracks connected devices, and stores historical connection data in SQL Server. The system is designed to be modular, maintainable, and extensible.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Network Monitor                          │
│                                                               │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Scanner     │  │   Monitor    │  │    Database     │  │
│  │   Module      │→ │   Module     │→ │    Manager      │  │
│  └───────────────┘  └──────────────┘  └─────────────────┘  │
│         ↓                  ↓                     ↓           │
│    Network Scan      Orchestration         SQL Server       │
│    (ARP/Scapy)       (Main Loop)          (DeviceData)      │
└─────────────────────────────────────────────────────────────┘
         ↓                                          ↓
   Local Network                            Database Views
   (Devices)                                (Power BI)
```

## Components

### 1. Scanner Module (`scanner.py`)

**Purpose**: Network scanning and device discovery

**Key Classes**:
- `Device`: Represents a network device with MAC, IP, and hostname
- `NetworkScanner`: Performs ARP scans to discover devices

**Responsibilities**:
- Send ARP requests to network subnet
- Parse ARP responses to identify devices
- Resolve hostnames from IP addresses
- Return discovered devices as Device objects

**Technology**: Uses Scapy for packet manipulation

### 2. Database Manager (`database.py`)

**Purpose**: Database operations and data persistence

**Key Classes**:
- `DatabaseManager`: Handles all database interactions

**Responsibilities**:
- Manage SQL Server connections
- Track device connection/disconnection events
- Update device status and last-seen timestamps
- Log events to ConnectionLog table
- Provide device statistics

**Technology**: Uses pyodbc for SQL Server connectivity

### 3. Monitor Module (`monitor.py`)

**Purpose**: Main orchestration and control flow

**Key Classes**:
- `NetworkMonitor`: Coordinates scanning and database updates

**Responsibilities**:
- Initialize scanner and database components
- Run continuous monitoring loop
- Handle errors and interruptions
- Provide status information
- Manage cleanup on shutdown

### 4. Configuration Module (`config.py`)

**Purpose**: Configuration management

**Key Classes**:
- `NetworkConfig`: Network scanning parameters
- `DatabaseConfig`: Database connection settings
- `LoggingConfig`: Logging configuration
- `Config`: Unified configuration object

**Responsibilities**:
- Load settings from environment variables
- Provide default values
- Generate connection strings
- Validate configuration

**Technology**: Uses python-dotenv for environment variables

### 5. Main Module (`main.py`)

**Purpose**: Application entry point

**Responsibilities**:
- Setup logging
- Load configuration
- Initialize and start monitor
- Handle startup errors
- Provide user feedback

## Data Flow

```
1. Network Scan
   ├─ Scanner creates ARP packet
   ├─ Broadcasts to subnet
   ├─ Collects responses
   └─ Returns Device objects

2. Device Processing
   ├─ Monitor receives devices
   ├─ Compares with previous scan
   ├─ Identifies new/disconnected devices
   └─ Calls database manager

3. Database Update
   ├─ New devices → INSERT or UPDATE
   ├─ Log connection event
   ├─ Disconnected devices → UPDATE status
   ├─ Log disconnection event
   └─ Update last-seen timestamps

4. Wait & Repeat
   └─ Sleep for scan_interval seconds
```

## Database Schema

### DeviceConnections Table
Stores current state of all known devices

| Column | Type | Description |
|--------|------|-------------|
| ConnectionID | INT (PK) | Unique identifier |
| MACAddress | VARCHAR(17) | Device MAC address (unique) |
| IPAddress | VARCHAR(15) | Current IP address |
| Hostname | VARCHAR(255) | Resolved hostname |
| FirstSeen | DATETIME | First detection time |
| LastSeen | DATETIME | Most recent detection |
| IsConnected | BIT | Current connection status |
| DeviceName | VARCHAR(255) | User-assigned friendly name |
| DeviceType | VARCHAR(50) | Device type (future) |
| Vendor | VARCHAR(255) | MAC vendor (future) |

### ConnectionLog Table
Historical event log

| Column | Type | Description |
|--------|------|-------------|
| LogID | INT (PK) | Unique identifier |
| MACAddress | VARCHAR(17) | Device MAC address (FK) |
| IPAddress | VARCHAR(15) | IP at event time |
| EventType | VARCHAR(20) | CONNECTED/DISCONNECTED |
| EventTime | DATETIME | Event timestamp |

### Views
- `vw_CurrentlyConnected`: Active devices with display names
- `vw_ConnectionHistory`: Full event history with device info
- `vw_DailyConnectionSummary`: Daily statistics

## Security Considerations

### Permissions Required
- **Network Scanning**: Requires administrator/root privileges
  - Windows: Run as Administrator
  - Linux/Mac: Use sudo

### Database Security
- Supports Windows Authentication (recommended)
- Supports SQL Authentication with credentials
- Connection string stored in .env (not committed)

### Network Security
- Passive monitoring (read-only ARP scanning)
- No device manipulation or attacks
- Local network only (no internet traffic)

## Error Handling

### Network Errors
- Permission denied → Clear user message, exit gracefully
- Scan timeout → Log warning, continue monitoring
- No devices found → Log warning, continue monitoring

### Database Errors
- Connection failure → Retry with exponential backoff
- Transaction errors → Rollback and log error
- Data integrity errors → Log and continue

### Application Errors
- Configuration errors → Validate on startup, fail fast
- Runtime errors → Log with traceback, attempt recovery
- Keyboard interrupt → Clean shutdown

## Performance Considerations

### Scanning Performance
- **Timeout**: 3 seconds (configurable)
- **Subnet size**: /24 network = 254 IPs
- **Scan time**: ~3-5 seconds for typical network
- **Interval**: 60 seconds default (configurable)

### Database Performance
- **Indexes**: On MAC, LastSeen, EventTime, EventType
- **Batch operations**: Single transaction per scan
- **Connection pooling**: Single persistent connection

### Resource Usage
- **Memory**: ~50-100 MB
- **CPU**: Low (mostly idle during scan_interval)
- **Network**: Minimal (broadcast ARP only)
- **Disk**: Log file grows ~1-2 MB/day

## Extensibility

### Adding Features

1. **MAC Vendor Lookup**
   - Add vendor API client in scanner module
   - Update Device class with vendor field
   - Populate during scan

2. **Email Notifications**
   - Add notification module
   - Subscribe to connection/disconnection events
   - Send emails via SMTP

3. **Web Dashboard**
   - Add Flask/FastAPI web server
   - Create REST API endpoints
   - Serve real-time device status

4. **Device Profiling**
   - Add port scanning (nmap integration)
   - Identify device types
   - Store device fingerprints

5. **Multiple Networks**
   - Extend Config for multiple subnets
   - Create scanner pool
   - Parallel scanning

## Testing Strategy

### Unit Tests
- Scanner: Mock scapy responses
- Database: Mock pyodbc connections
- Config: Mock environment variables
- Monitor: Mock scanner and database

### Integration Tests
- End-to-end scan and database update
- Configuration loading
- Error handling paths

### Performance Tests
- Large network scanning (254 devices)
- Database load testing
- Long-running stability

## Deployment

### Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m network_monitor.main
```

### Production
```bash
# Install as package
pip install -e .

# Run as service (systemd on Linux)
systemctl start network-monitor

# Run as Windows service
nssm install NetworkMonitor
```

## Monitoring & Operations

### Logs
- **Location**: `network_monitor.log`
- **Rotation**: Implement logrotate or Python logging handlers
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics
- Devices discovered per scan
- Connection/disconnection events per hour
- Scan duration
- Database query times

### Alerts
- Scanner permission errors
- Database connection failures
- Unusual device activity
- Service downtime

## Future Roadmap

### Phase 1 (Current)
- ✅ Basic network scanning
- ✅ SQL Server integration
- ✅ Event logging
- ✅ Power BI views

### Phase 2 (Planned)
- 🔄 MAC vendor lookup
- 🔄 Web dashboard
- 🔄 Email notifications
- 🔄 Enhanced device profiling

### Phase 3 (Future)
- ⏳ Multi-network support
- ⏳ Cloud deployment
- ⏳ Mobile app
- ⏳ Machine learning anomaly detection
