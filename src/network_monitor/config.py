"""
Configuration management for Network Monitor
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class NetworkConfig:
    """Network scanning configuration"""
    subnet: str
    scan_interval: int
    timeout: int = 3

    @classmethod
    def from_env(cls) -> "NetworkConfig":
        """Load network configuration from environment variables"""
        return cls(
            subnet=os.getenv("NETWORK_SUBNET", "192.168.1.0/24"),
            scan_interval=int(os.getenv("SCAN_INTERVAL", "60")),
            timeout=int(os.getenv("SCAN_TIMEOUT", "3")),
        )


@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    server: str
    database: str
    username: Optional[str]
    password: Optional[str]
    use_windows_auth: bool
    driver: str = "ODBC Driver 17 for SQL Server"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        """Load database configuration from environment variables"""
        use_windows_auth = os.getenv("SQL_WINDOWS_AUTH", "yes").lower() == "yes"
        
        return cls(
            server=os.getenv("SQL_SERVER", "localhost"),
            database=os.getenv("SQL_DATABASE", "NetworkMonitor"),
            username=os.getenv("SQL_USERNAME") if not use_windows_auth else None,
            password=os.getenv("SQL_PASSWORD") if not use_windows_auth else None,
            use_windows_auth=use_windows_auth,
            driver=os.getenv("SQL_DRIVER", "ODBC Driver 17 for SQL Server"),
        )

    def get_connection_string(self) -> str:
        """Generate SQL Server connection string"""
        base = f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};"
        
        if self.use_windows_auth:
            return base + "Trusted_Connection=yes;"
        else:
            return base + f"UID={self.username};PWD={self.password};"


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str
    file_path: str
    format: str

    @classmethod
    def from_env(cls) -> "LoggingConfig":
        """Load logging configuration from environment variables"""
        return cls(
            level=os.getenv("LOG_LEVEL", "INFO"),
            file_path=os.getenv("LOG_FILE", "network_monitor.log"),
            format=os.getenv(
                "LOG_FORMAT",
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
        )


class Config:
    """Main configuration class combining all configs"""
    
    def __init__(self):
        self.network = NetworkConfig.from_env()
        self.database = DatabaseConfig.from_env()
        self.logging = LoggingConfig.from_env()

    @classmethod
    def load(cls) -> "Config":
        """Load all configuration from environment"""
        return cls()
