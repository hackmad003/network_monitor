"""
Unit tests for NetworkScanner
"""
import pytest
from unittest.mock import patch, MagicMock
from network_monitor.scanner import NetworkScanner, Device


class TestDevice:
    """Test cases for Device class"""
    
    def test_device_creation(self):
        """Test device object creation"""
        device = Device("AA:BB:CC:DD:EE:FF", "192.168.1.100", "test-device")
        assert device.mac_address == "AA:BB:CC:DD:EE:FF"
        assert device.ip_address == "192.168.1.100"
        assert device.hostname == "test-device"
    
    def test_device_mac_uppercase(self):
        """Test that MAC address is converted to uppercase"""
        device = Device("aa:bb:cc:dd:ee:ff", "192.168.1.100")
        assert device.mac_address == "AA:BB:CC:DD:EE:FF"
    
    def test_device_equality(self):
        """Test device equality based on MAC address"""
        device1 = Device("AA:BB:CC:DD:EE:FF", "192.168.1.100")
        device2 = Device("AA:BB:CC:DD:EE:FF", "192.168.1.101")
        device3 = Device("11:22:33:44:55:66", "192.168.1.100")
        
        assert device1 == device2
        assert device1 != device3


class TestNetworkScanner:
    """Test cases for NetworkScanner class"""
    
    def test_scanner_initialization(self):
        """Test scanner initialization"""
        scanner = NetworkScanner("192.168.1.0/24", timeout=5)
        assert scanner.subnet == "192.168.1.0/24"
        assert scanner.timeout == 5
    
    @patch('network_monitor.scanner.socket.gethostbyaddr')
    def test_resolve_hostname_success(self, mock_gethostbyaddr):
        """Test successful hostname resolution"""
        mock_gethostbyaddr.return_value = ("test-host", [], [])
        
        hostname = NetworkScanner._resolve_hostname("192.168.1.100")
        assert hostname == "test-host"
    
    @patch('network_monitor.scanner.socket.gethostbyaddr')
    def test_resolve_hostname_failure(self, mock_gethostbyaddr):
        """Test failed hostname resolution"""
        mock_gethostbyaddr.side_effect = Exception("Cannot resolve")
        
        hostname = NetworkScanner._resolve_hostname("192.168.1.100")
        assert hostname is None
    
    @patch('network_monitor.scanner.srp')
    def test_scan_success(self, mock_srp):
        """Test successful network scan"""
        # Mock scapy response
        mock_received = MagicMock()
        mock_received.hwsrc = "aa:bb:cc:dd:ee:ff"
        mock_received.psrc = "192.168.1.100"
        
        mock_srp.return_value = ([((None, mock_received),)], None)
        
        scanner = NetworkScanner("192.168.1.0/24")
        devices = scanner.scan()
        
        assert len(devices) == 1
        assert "AA:BB:CC:DD:EE:FF" in devices
        assert devices["AA:BB:CC:DD:EE:FF"].ip_address == "192.168.1.100"
    
    @patch('network_monitor.scanner.srp')
    def test_scan_permission_error(self, mock_srp):
        """Test scan with permission error"""
        mock_srp.side_effect = PermissionError("Admin required")
        
        scanner = NetworkScanner("192.168.1.0/24")
        
        with pytest.raises(PermissionError):
            scanner.scan()
