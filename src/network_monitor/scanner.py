"""
Network scanning functionality using ARP protocol
"""
import logging
import socket
from typing import Dict, Optional
from scapy.all import ARP, Ether, srp

logger = logging.getLogger(__name__)


class Device:
    """Represents a network device"""
    
    def __init__(self, mac_address: str, ip_address: str, hostname: Optional[str] = None):
        self.mac_address = mac_address.upper()
        self.ip_address = ip_address
        self.hostname = hostname

    def __repr__(self) -> str:
        return f"Device(mac={self.mac_address}, ip={self.ip_address}, hostname={self.hostname})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Device):
            return False
        return self.mac_address == other.mac_address

    def __hash__(self) -> int:
        return hash(self.mac_address)


class NetworkScanner:
    """Handles network scanning operations"""

    def __init__(self, subnet: str, timeout: int = 3):
        """
        Initialize network scanner
        
        Args:
            subnet: Network subnet to scan (e.g., '192.168.1.0/24')
            timeout: Timeout in seconds for ARP requests
        """
        self.subnet = subnet
        self.timeout = timeout
        logger.info(f"NetworkScanner initialized for subnet: {subnet}")

    def scan(self) -> Dict[str, Device]:
        """
        Scan the network for connected devices using ARP
        
        Returns:
            Dictionary mapping MAC addresses to Device objects
        """
        try:
            logger.info(f"Scanning network {self.subnet}...")
            
            # Create ARP packet
            arp = ARP(pdst=self.subnet)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether / arp
            
            # Send packet and get response
            result = srp(packet, timeout=self.timeout, verbose=0)[0]
            
            devices = {}
            for sent, received in result:
                mac_address = received.hwsrc.upper()
                ip_address = received.psrc
                hostname = self._resolve_hostname(ip_address)
                
                device = Device(mac_address, ip_address, hostname)
                devices[mac_address] = device
            
            logger.info(f"Found {len(devices)} devices on network")
            return devices
            
        except PermissionError:
            logger.error("Permission denied. Network scanning requires administrator/root privileges.")
            raise
        except Exception as e:
            logger.error(f"Error scanning network: {e}", exc_info=True)
            return {}

    @staticmethod
    def _resolve_hostname(ip_address: str) -> Optional[str]:
        """
        Try to resolve hostname from IP address
        
        Args:
            ip_address: IP address to resolve
            
        Returns:
            Hostname if resolved, None otherwise
        """
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except (socket.herror, socket.gaierror):
            return None
        except Exception as e:
            logger.debug(f"Could not resolve hostname for {ip_address}: {e}")
            return None
