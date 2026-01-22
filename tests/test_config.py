"""
Unit tests for configuration module
"""
import os
import pytest
from unittest.mock import patch
from network_monitor.config import NetworkConfig, DatabaseConfig, LoggingConfig, Config


class TestNetworkConfig:
    """Test cases for NetworkConfig"""
    
    @patch.dict(os.environ, {
        "NETWORK_SUBNET": "10.0.0.0/24",
        "SCAN_INTERVAL": "30",
        "SCAN_TIMEOUT": "5"
    })
    def test_from_env(self):
        """Test loading from environment variables"""
        config = NetworkConfig.from_env()
        assert config.subnet == "10.0.0.0/24"
        assert config.scan_interval == 30
        assert config.timeout == 5
    
    @patch.dict(os.environ, {}, clear=True)
    def test_from_env_defaults(self):
        """Test default values when env vars not set"""
        config = NetworkConfig.from_env()
        assert config.subnet == "192.168.1.0/24"
        assert config.scan_interval == 60
        assert config.timeout == 3


class TestDatabaseConfig:
    """Test cases for DatabaseConfig"""
    
    @patch.dict(os.environ, {
        "SQL_SERVER": "testserver",
        "SQL_DATABASE": "testdb",
        "SQL_WINDOWS_AUTH": "yes"
    })
    def test_windows_auth(self):
        """Test Windows authentication configuration"""
        config = DatabaseConfig.from_env()
        assert config.server == "testserver"
        assert config.database == "testdb"
        assert config.use_windows_auth is True
        assert config.username is None
        assert config.password is None
    
    @patch.dict(os.environ, {
        "SQL_SERVER": "testserver",
        "SQL_DATABASE": "testdb",
        "SQL_USERNAME": "testuser",
        "SQL_PASSWORD": "testpass",
        "SQL_WINDOWS_AUTH": "no"
    })
    def test_sql_auth(self):
        """Test SQL authentication configuration"""
        config = DatabaseConfig.from_env()
        assert config.use_windows_auth is False
        assert config.username == "testuser"
        assert config.password == "testpass"
    
    def test_connection_string_windows(self):
        """Test connection string generation for Windows auth"""
        config = DatabaseConfig(
            server="localhost",
            database="TestDB",
            username=None,
            password=None,
            use_windows_auth=True
        )
        conn_str = config.get_connection_string()
        assert "Trusted_Connection=yes" in conn_str
        assert "UID=" not in conn_str
    
    def test_connection_string_sql(self):
        """Test connection string generation for SQL auth"""
        config = DatabaseConfig(
            server="localhost",
            database="TestDB",
            username="user",
            password="pass",
            use_windows_auth=False
        )
        conn_str = config.get_connection_string()
        assert "UID=user" in conn_str
        assert "PWD=pass" in conn_str
        assert "Trusted_Connection" not in conn_str


class TestLoggingConfig:
    """Test cases for LoggingConfig"""
    
    @patch.dict(os.environ, {
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "test.log"
    })
    def test_from_env(self):
        """Test loading logging config from environment"""
        config = LoggingConfig.from_env()
        assert config.level == "DEBUG"
        assert config.file_path == "test.log"
