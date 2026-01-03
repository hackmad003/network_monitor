"""
Network Device Monitor
Scans local network for connected devices and logs to SQL Server database
"""

#############
## IMPORTS ##
#############
import os
import time
import logging
from datetime import datetime
from typing import Dict, Set, Optional
import pyodbc
from scapy.all import ARP, Ether, srp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('network_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NetworkMonitor:
    def __init__(self):
        """Initialize the network monitor with database connection"""
        self.network_subnet = os.getenv('NETWORK_SUBNET', '192.168.1.0/24')
        self.scan_interval = int(os.getenv('SCAN_INTERVAL', 60))
        self.known_devices: Set[str] = set()
        self.connection = self._get_db_connection()
        logger.info("Network Monitor initialized")
        logger.info(f"Monitoring network: {self.network_subnet}")
        logger.info(f"Scan interval: {self.scan_interval} seconds")
        
    def _get_db_connection(self):
        """Create connection to SQL Server database"""
        try:
            server = os.getenv('SQL_SERVER')
            database = os.getenv('SQL_DATABASE')
            use_windows_auth = os.getenv('SQL_WINDOWS_AUTH', 'yes').lower() == 'yes'
            
            if use_windows_auth:
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={server};'
                    f'DATABASE={database};'
                    f'Trusted_Connection=yes;'
                )
            else:
                username = os.getenv('SQL_USERNAME')
                password = os.getenv('SQL_PASSWORD')
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={server};'
                    f'DATABASE={database};'
                    f'UID={username};'
                    f'PWD={password};'
                )
            
            conn = pyodbc.connect(connection_string)
            logger.info("Successfully connected to SQL Server database")
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    def scan_network(self) -> Dict[str, dict]:
        """
        Scan the network for connected devices using ARP
        Returns dictionary of MAC addresses and their details
        """
        try:
            logger.info(f"Scanning network {self.network_subnet}...")
            
            # Create ARP packet
            arp = ARP(pdst=self.network_subnet)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Send packet and get response
            result = srp(packet, timeout=3, verbose=0)[0]
            
            devices = {}
            for sent, received in result:
                mac_address = received.hwsrc.upper()
                ip_address = received.psrc
                
                devices[mac_address] = {
                    'ip': ip_address,
                    'mac': mac_address,
                    'hostname': self._get_hostname(ip_address)
                }
            
            logger.info(f"Found {len(devices)} devices on network")
            return devices
            
        except Exception as e:
            logger.error(f"Error scanning network: {e}")
            return {}
    
    def _get_hostname(self, ip_address: str) -> Optional[str]:
        """Try to resolve hostname from IP address"""
        try:
            import socket
            hostname = socket.gethostbyaddr(ip_address)[0]
            return hostname
        except:
            return None
    
    def update_database(self, current_devices: Dict[str, dict]):
        """Update database with current device information"""
        try:
            cursor = self.connection.cursor()
            current_time = datetime.now()
            current_macs = set(current_devices.keys())
            
            # Get previously known connected devices
            cursor.execute("""
                SELECT MACAddress FROM DeviceConnections 
                WHERE IsConnected = 1
            """)
            previous_macs = {row[0] for row in cursor.fetchall()}
            
            # Find newly connected devices
            new_devices = current_macs - previous_macs
            # Find disconnected devices
            disconnected_devices = previous_macs - current_macs
            
            # Process newly connected devices
            for mac in new_devices:
                device = current_devices[mac]
                logger.info(f"New device connected: {mac} ({device.get('ip')})")
                
                # Check if device exists in database
                cursor.execute("""
                    SELECT ConnectionID FROM DeviceConnections 
                    WHERE MACAddress = ?
                """, mac)
                
                if cursor.fetchone():
                    # Update existing device
                    cursor.execute("""
                        UPDATE DeviceConnections 
                        SET IPAddress = ?, 
                            Hostname = ?,
                            LastSeen = ?, 
                            IsConnected = 1
                        WHERE MACAddress = ?
                    """, device['ip'], device['hostname'], current_time, mac)
                else:
                    # Insert new device
                    cursor.execute("""
                        INSERT INTO DeviceConnections 
                        (MACAddress, IPAddress, Hostname, FirstSeen, LastSeen, IsConnected)
                        VALUES (?, ?, ?, ?, ?, 1)
                    """, mac, device['ip'], device['hostname'], current_time, current_time)
                
                # Log connection event
                cursor.execute("""
                    INSERT INTO ConnectionLog 
                    (MACAddress, IPAddress, EventType, EventTime)
                    VALUES (?, ?, 'CONNECTED', ?)
                """, mac, device['ip'], current_time)
            
            # Process disconnected devices
            for mac in disconnected_devices:
                logger.info(f"Device disconnected: {mac}")
                
                # Update device status
                cursor.execute("""
                    UPDATE DeviceConnections 
                    SET IsConnected = 0
                    WHERE MACAddress = ?
                """, mac)
                
                # Log disconnection event
                cursor.execute("""
                    INSERT INTO ConnectionLog 
                    (MACAddress, IPAddress, EventType, EventTime)
                    VALUES (?, NULL, 'DISCONNECTED', ?)
                """, mac, current_time)
            
            # Update LastSeen for all currently connected devices
            for mac in current_macs:
                device = current_devices[mac]
                cursor.execute("""
                    UPDATE DeviceConnections 
                    SET LastSeen = ?,
                        IPAddress = ?,
                        Hostname = ?
                    WHERE MACAddress = ?
                """, current_time, device['ip'], device['hostname'], mac)
            
            self.connection.commit()
            
            if new_devices or disconnected_devices:
                logger.info(f"Database updated: {len(new_devices)} connected, {len(disconnected_devices)} disconnected")
                
        except Exception as e:
            logger.error(f"Error updating database: {e}")
            self.connection.rollback()
    
    def run(self):
        """Main monitoring loop"""
        logger.info("Starting network monitoring...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                # Scan network
                devices = self.scan_network()
                
                # Update database
                if devices:
                    self.update_database(devices)
                
                # Wait for next scan
                logger.info(f"Waiting {self.scan_interval} seconds until next scan...")
                time.sleep(self.scan_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        finally:
            self.connection.close()
            logger.info("Database connection closed")


def main():
    """Entry point for the application"""
    print("=" * 60)
    print("Network Device Monitor")
    print("=" * 60)
    print()
    
    try:
        monitor = NetworkMonitor()
        monitor.run()
    except Exception as e:
        logger.error(f"Failed to start monitor: {e}")
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. Your .env file is configured correctly")
        print("2. SQL Server is running and accessible")
        print("3. Database has been set up (run database_setup.sql)")
        print("4. You have administrator/root privileges (required for network scanning)")


if __name__ == "__main__":
    main()
