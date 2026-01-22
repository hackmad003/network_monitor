"""
Pytest configuration and fixtures
"""
import pytest
from unittest.mock import MagicMock
from network_monitor.config import Config, NetworkConfig, DatabaseConfig, LoggingConfig


@pytest.fixture
def mock_config():
    """Fixture providing a mock configuration"""
    config = Config()
    config.network = NetworkConfig(
        subnet="192.168.1.0/24",
        scan_interval=60,
        timeout=3
    )
    config.database = DatabaseConfig(
        server="localhost",
        database="TestDB",
        username=None,
        password=None,
        use_windows_auth=True
    )
    config.logging = LoggingConfig(
        level="INFO",
        file_path="test.log",
        format="%(message)s"
    )
    return config


@pytest.fixture
def mock_database_connection():
    """Fixture providing a mock database connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor
