# API Reference

Complete API documentation for Network Monitor modules.

## Table of Contents
- [scanner Module](#scanner-module)
- [database Module](#database-module)
- [monitor Module](#monitor-module)
- [config Module](#config-module)
- [main Module](#main-module)

---

## scanner Module

### Device Class

Represents a network device.

```python
class Device:
    def __init__(self, mac_address: str, ip_address: str, hostname: Optional[str] = None)
```

**Parameters**:
- `mac_address` (str): MAC address of the device (converted to uppercase)
- `ip_address` (str): IP address of the device
- `hostname` (Optional[str]): Hostname of the device if resolved

**Attributes**:
- `mac_address` (str): MAC address in uppercase format
- `ip_address` (str): IP address
- `hostname` (Optional[str]): Resolved hostname or None

**Methods**:
- `__repr__() -> str`: String representation
- `__eq__(other) -> bool`: Equality based on MAC address
- `__hash__() -> int`: Hash based on MAC address

**Example**:
```python
from network_monitor.scanner import Device

device = Device("aa:bb:cc:dd:ee:ff", "192.168.1.100", "laptop")
print(device.mac_address)  # "AA:BB:CC:DD:EE:FF"
```

---

### NetworkScanner Class

Performs network scanning operations.

```python
class NetworkScanner:
    def __init__(self, subnet: str, timeout: int = 3)
```

**Parameters**:
- `subnet` (str): Network subnet in CIDR notation (e.g., "192.168.1.0/24")
- `timeout` (int): Timeout in seconds for ARP requests (default: 3)

**Methods**:

#### scan()
```python
def scan(self) -> Dict[str, Device]
```
Scan the network for connected devices using ARP protocol.

**Returns**: Dictionary mapping MAC addresses to Device objects

**Raises**:
- `PermissionError`: If insufficient privileges for network scanning

**Example**:
```python
scanner = NetworkScanner("192.168.1.0/24", timeout=5)
devices = scanner.scan()

for mac, device in devices.items():
    print(f"{mac}: {device.ip_address} - {device.hostname}")
```

#### _resolve_hostname() [static]
```python
@staticmethod
def _resolve_hostname(ip_address: str) -> Optional[str]
```
Attempt to resolve hostname from IP address.

**Parameters**:
- `ip_address` (str): IP address to resolve

**Returns**: Hostname string or None if resolution fails

---

## database Module

### DatabaseManager Class

Manages database connections and operations.

```python
class DatabaseManager:
    def __init__(self, config: DatabaseConfig)
```

**Parameters**:
- `config` (DatabaseConfig): Database configuration object

**Methods**:

#### close()
```python
def close(self) -> None
```
Close the database connection.

**Example**:
```python
from network_monitor.config import DatabaseConfig
from network_monitor.database import DatabaseManager

config = DatabaseConfig.from_env()
db = DatabaseManager(config)
# ... perform operations ...
db.close()
```

#### get_connected_devices()
```python
def get_connected_devices(self) -> Set[str]
```
Get MAC addresses of currently connected devices.

**Returns**: Set of MAC address strings

#### update_device_status()
```python
def update_device_status(self, devices: Dict[str, Device]) -> None
```
Update database with current device status.

**Parameters**:
- `devices` (Dict[str, Device]): Dictionary of currently detected devices

**Raises**:
- `pyodbc.Error`: On database operation failures

**Example**:
```python
scanner = NetworkScanner("192.168.1.0/24")
devices = scanner.scan()
db.update_device_status(devices)
```

#### get_device_count()
```python
def get_device_count(self) -> Dict[str, int]
```
Get count of connected and total devices.

**Returns**: Dictionary with keys "connected" and "total"

**Example**:
```python
counts = db.get_device_count()
print(f"Connected: {counts['connected']}, Total: {counts['total']}")
```

---

## monitor Module

### NetworkMonitor Class

Main monitoring orchestration class.

```python
class NetworkMonitor:
    def __init__(self, config: Optional[Config] = None)
```

**Parameters**:
- `config` (Optional[Config]): Configuration object (loads from env if None)

**Attributes**:
- `config` (Config): Application configuration
- `scanner` (NetworkScanner): Network scanner instance
- `database` (DatabaseManager): Database manager instance

**Methods**:

#### scan_once()
```python
def scan_once(self) -> bool
```
Perform a single network scan and update database.

**Returns**: True if scan was successful, False otherwise

**Example**:
```python
monitor = NetworkMonitor()
success = monitor.scan_once()
if success:
    print("Scan completed successfully")
```

#### run()
```python
def run(self) -> None
```
Main monitoring loop - runs continuously until interrupted.

**Raises**:
- `KeyboardInterrupt`: On user interrupt (Ctrl+C)
- `Exception`: On critical errors

**Example**:
```python
monitor = NetworkMonitor()
try:
    monitor.run()  # Runs until Ctrl+C
except KeyboardInterrupt:
    print("Stopped by user")
```

#### cleanup()
```python
def cleanup(self) -> None
```
Clean up resources (close database connections).

#### get_status()
```python
def get_status(self) -> dict
```
Get current monitoring status.

**Returns**: Dictionary with status information

**Example**:
```python
status = monitor.get_status()
print(f"Status: {status['status']}")
print(f"Network: {status['network']}")
print(f"Connected Devices: {status['connected_devices']}")
```

---

## config Module

### NetworkConfig Class

Network scanning configuration.

```python
@dataclass
class NetworkConfig:
    subnet: str
    scan_interval: int
    timeout: int = 3
```

**Class Methods**:

#### from_env()
```python
@classmethod
def from_env(cls) -> NetworkConfig
```
Load configuration from environment variables.

**Environment Variables**:
- `NETWORK_SUBNET` (default: "192.168.1.0/24")
- `SCAN_INTERVAL` (default: "60")
- `SCAN_TIMEOUT` (default: "3")

**Example**:
```python
config = NetworkConfig.from_env()
print(f"Scanning {config.subnet} every {config.scan_interval}s")
```

---

### DatabaseConfig Class

Database connection configuration.

```python
@dataclass
class DatabaseConfig:
    server: str
    database: str
    username: Optional[str]
    password: Optional[str]
    use_windows_auth: bool
    driver: str = "ODBC Driver 17 for SQL Server"
```

**Class Methods**:

#### from_env()
```python
@classmethod
def from_env(cls) -> DatabaseConfig
```
Load configuration from environment variables.

**Environment Variables**:
- `SQL_SERVER` (default: "localhost")
- `SQL_DATABASE` (default: "NetworkMonitor")
- `SQL_USERNAME` (required if not using Windows auth)
- `SQL_PASSWORD` (required if not using Windows auth)
- `SQL_WINDOWS_AUTH` (default: "yes")
- `SQL_DRIVER` (default: "ODBC Driver 17 for SQL Server")

#### get_connection_string()
```python
def get_connection_string(self) -> str
```
Generate SQL Server connection string.

**Returns**: ODBC connection string

**Example**:
```python
config = DatabaseConfig.from_env()
conn_str = config.get_connection_string()
```

---

### LoggingConfig Class

Logging configuration.

```python
@dataclass
class LoggingConfig:
    level: str
    file_path: str
    format: str
```

**Class Methods**:

#### from_env()
```python
@classmethod
def from_env(cls) -> LoggingConfig
```
Load configuration from environment variables.

**Environment Variables**:
- `LOG_LEVEL` (default: "INFO")
- `LOG_FILE` (default: "network_monitor.log")
- `LOG_FORMAT` (default: "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

---

### Config Class

Unified configuration container.

```python
class Config:
    def __init__(self)
```

**Attributes**:
- `network` (NetworkConfig): Network configuration
- `database` (DatabaseConfig): Database configuration
- `logging` (LoggingConfig): Logging configuration

**Class Methods**:

#### load()
```python
@classmethod
def load(cls) -> Config
```
Load all configuration from environment.

**Example**:
```python
config = Config.load()
print(f"Network: {config.network.subnet}")
print(f"Database: {config.database.server}")
print(f"Log Level: {config.logging.level}")
```

---

## main Module

### Functions

#### setup_logging()
```python
def setup_logging(config: Config) -> None
```
Configure logging based on configuration.

**Parameters**:
- `config` (Config): Application configuration

#### main()
```python
def main() -> None
```
Main entry point for the application.

**Raises**:
- `PermissionError`: If insufficient privileges
- `Exception`: On startup failures

**Example**:
```python
from network_monitor.main import main

if __name__ == "__main__":
    main()
```

---

## Usage Examples

### Basic Usage
```python
from network_monitor import NetworkMonitor

# Using environment configuration
monitor = NetworkMonitor()
monitor.run()
```

### Custom Configuration
```python
from network_monitor.config import Config, NetworkConfig, DatabaseConfig, LoggingConfig
from network_monitor import NetworkMonitor

# Create custom configuration
config = Config()
config.network = NetworkConfig(
    subnet="10.0.0.0/24",
    scan_interval=30,
    timeout=5
)

monitor = NetworkMonitor(config)
monitor.run()
```

### Single Scan
```python
from network_monitor import NetworkMonitor

monitor = NetworkMonitor()
if monitor.scan_once():
    status = monitor.get_status()
    print(f"Found {status['connected_devices']} devices")
monitor.cleanup()
```

### Custom Scanner
```python
from network_monitor.scanner import NetworkScanner

scanner = NetworkScanner("192.168.1.0/24", timeout=5)
devices = scanner.scan()

for mac, device in devices.items():
    print(f"Device: {device.hostname or 'Unknown'}")
    print(f"  MAC: {mac}")
    print(f"  IP: {device.ip_address}")
```

### Database Operations
```python
from network_monitor.config import DatabaseConfig
from network_monitor.database import DatabaseManager

config = DatabaseConfig.from_env()
db = DatabaseManager(config)

# Get statistics
counts = db.get_device_count()
print(f"Total devices: {counts['total']}")
print(f"Currently connected: {counts['connected']}")

# Get connected MAC addresses
connected = db.get_connected_devices()
print(f"Connected MACs: {connected}")

db.close()
```
