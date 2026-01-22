# Network Monitor - Project Structure

Complete overview of the reorganized project structure.

## Directory Tree

```
network-monitor/
│
├── src/                          # Source code
│   └── network_monitor/          # Main package
│       ├── __init__.py           # Package initialization
│       ├── config.py             # Configuration management
│       ├── scanner.py            # Network scanning logic
│       ├── database.py           # Database operations
│       ├── monitor.py            # Main orchestration
│       └── main.py               # Application entry point
│
├── config/                       # Configuration files
│   ├── .env                      # Active configuration (not in git)
│   ├── env.example               # Configuration template
│   └── database_setup.sql        # Database schema
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # System architecture
│   ├── API_REFERENCE.md          # API documentation
│   ├── CODE_REVIEW.md            # Code review & improvements
│   ├── DEPLOYMENT.md             # Deployment guide
│   └── NetworkMonitor_Documentation.docx  # Original docs
│
├── scripts/                      # Utility scripts
│   ├── start_monitor.bat         # Windows startup script
│   └── start_monitor.sh          # Linux/Mac startup script
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_config.py            # Configuration tests
│   └── test_scanner.py           # Scanner tests
│
├── .gitignore                    # Git ignore rules
├── CHANGELOG.md                  # Version history
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                       # MIT License
├── PROJECT_STRUCTURE.md          # This file
├── QUICKSTART.md                 # Quick start guide
├── README.md                     # Main documentation
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
├── setup.py                      # Package setup
└── gitignore                     # Old gitignore (can be removed)
```

## File Descriptions

### Source Code (`src/network_monitor/`)

#### `__init__.py`
Package initialization and exports
- Version information
- Main exports: NetworkMonitor, DatabaseManager, NetworkScanner

#### `config.py`
Configuration management with dataclasses
- `NetworkConfig`: Network scanning settings
- `DatabaseConfig`: Database connection settings
- `LoggingConfig`: Logging configuration
- `Config`: Unified configuration loader

#### `scanner.py`
Network scanning functionality
- `Device`: Device data model
- `NetworkScanner`: ARP-based network scanner
- Hostname resolution
- Device discovery

#### `database.py`
Database operations and management
- `DatabaseManager`: SQL Server interface
- Connection management
- Device status tracking
- Event logging
- Statistics queries

#### `monitor.py`
Main monitoring orchestration
- `NetworkMonitor`: Main controller
- Scan loop management
- Component coordination
- Status reporting

#### `main.py`
Application entry point
- Logging setup
- Configuration loading
- Error handling
- User-friendly error messages

### Configuration (`config/`)

#### `.env`
Active configuration (not committed to git)
- Network subnet and scan interval
- Database connection details
- Logging settings

#### `env.example`
Configuration template for new installations
- Example values
- Documentation of each setting

#### `database_setup.sql`
Complete database schema
- Tables: DeviceConnections, ConnectionLog
- Views: vw_CurrentlyConnected, vw_ConnectionHistory, vw_DailyConnectionSummary
- Indexes for performance

### Documentation (`docs/`)

#### `ARCHITECTURE.md`
System architecture documentation
- Component overview
- Data flow diagrams
- Database schema
- Security considerations
- Performance analysis
- Extensibility guide

#### `API_REFERENCE.md`
Complete API documentation
- All classes and methods
- Parameters and return types
- Usage examples
- Code snippets

#### `CODE_REVIEW.md`
Code quality analysis
- Improvements from original code
- Best practices applied
- Design patterns used
- Testing strategy
- Future recommendations

#### `DEPLOYMENT.md`
Deployment guide for all platforms
- Development setup
- Production deployment
- Windows service setup
- Linux systemd service
- Docker deployment
- Troubleshooting

### Scripts (`scripts/`)

#### `start_monitor.bat`
Windows startup script
- Batch file for easy Windows execution
- Runs with virtual environment

#### `start_monitor.sh`
Linux/Mac startup script
- Bash script with sudo check
- Virtual environment activation

### Tests (`tests/`)

#### `conftest.py`
Pytest fixtures and configuration
- Mock configuration
- Mock database connections
- Shared test utilities

#### `test_config.py`
Configuration module tests
- Environment variable loading
- Default values
- Connection string generation

#### `test_scanner.py`
Scanner module tests
- Device class tests
- Network scanning with mocks
- Hostname resolution
- Error handling

## Old vs New Structure

### Before Reorganization
```
network-monitor/
├── network_monitor.py           # Everything in one file (260 lines)
├── database_setup.sql
├── .env
├── env.example
├── requirements.txt
├── start_monitor.bat
├── QUICKSTART.md
├── README.md
└── Docs/
    └── NetworkMonitor_Documentation.docx
```

### After Reorganization
```
network-monitor/
├── src/network_monitor/         # Modular package (6 files)
├── config/                      # Centralized configuration
├── docs/                        # Comprehensive documentation
├── scripts/                     # Platform-specific scripts
├── tests/                       # Test suite
└── [Project files]              # LICENSE, CHANGELOG, etc.
```

## Benefits of New Structure

### 1. **Separation of Concerns**
- Each module has a single responsibility
- Easy to locate specific functionality
- Reduced coupling between components

### 2. **Testability**
- Individual modules can be tested in isolation
- Mock dependencies easily
- Better test coverage

### 3. **Maintainability**
- Smaller files are easier to understand
- Clear organization helps navigation
- Changes are localized to specific modules

### 4. **Professional Standards**
- Follows Python packaging best practices
- Industry-standard directory structure
- Complete documentation set

### 5. **Scalability**
- Easy to add new features
- Can extend without modifying existing code
- Clear extension points

## Usage

### Import Structure

```python
# Import main classes
from network_monitor import NetworkMonitor, DatabaseManager, NetworkScanner

# Import specific modules
from network_monitor.config import Config
from network_monitor.scanner import Device

# Run the application
from network_monitor.main import main
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/network_monitor

# Run specific test file
pytest tests/test_scanner.py

# Run with verbose output
pytest tests/ -v
```

### Development Workflow

```bash
# 1. Install in development mode
pip install -e .

# 2. Make changes to src/network_monitor/

# 3. Run tests
pytest tests/

# 4. Check code quality
black src/
flake8 src/
mypy src/

# 5. Run application
python -m network_monitor.main
```

## Migration from Old Structure

If you have the old structure, here's how to migrate:

### 1. Backup Current Setup
```bash
cp network_monitor.py network_monitor.py.backup
cp .env config/.env
```

### 2. Update Imports
The old code still works at the root level. To use the new structure:

```bash
# Instead of:
python network_monitor.py

# Use:
python -m network_monitor.main
```

### 3. Update Configuration Path
The new structure looks for `.env` in `config/` directory:
```bash
mv .env config/.env
```

### 4. Update Scripts
Update any custom scripts to use the new import structure.

## Next Steps

After understanding the structure:

1. **For Users**: See QUICKSTART.md for setup instructions
2. **For Developers**: See CONTRIBUTING.md for development guidelines
3. **For Deployment**: See docs/DEPLOYMENT.md for production setup
4. **For API Usage**: See docs/API_REFERENCE.md for detailed API docs
