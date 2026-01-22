"""
Database management and operations
"""
import logging
from datetime import datetime
from typing import Set, Dict
import pyodbc
from .scanner import Device
from .config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations"""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize database manager
        
        Args:
            config: Database configuration
        """
        self.config = config
        self.connection = None
        self._connect()

    def _connect(self):
        """Establish connection to SQL Server database"""
        try:
            connection_string = self.config.get_connection_string()
            self.connection = pyodbc.connect(connection_string)
            logger.info("Successfully connected to SQL Server database")
        except pyodbc.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

    def get_connected_devices(self) -> Set[str]:
        """
        Get MAC addresses of currently connected devices
        
        Returns:
            Set of MAC addresses
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT MACAddress FROM DeviceConnections 
                WHERE IsConnected = 1
            """)
            return {row[0] for row in cursor.fetchall()}
        except pyodbc.Error as e:
            logger.error(f"Error retrieving connected devices: {e}")
            return set()

    def update_device_status(self, devices: Dict[str, Device]):
        """
        Update database with current device status
        
        Args:
            devices: Dictionary of currently detected devices (MAC -> Device)
        """
        try:
            cursor = self.connection.cursor()
            current_time = datetime.now()
            current_macs = set(devices.keys())
            
            # Get previously known connected devices
            previous_macs = self.get_connected_devices()
            
            # Find newly connected and disconnected devices
            new_devices = current_macs - previous_macs
            disconnected_devices = previous_macs - current_macs
            
            # Process newly connected devices
            for mac in new_devices:
                self._handle_device_connection(cursor, devices[mac], current_time)
            
            # Process disconnected devices
            for mac in disconnected_devices:
                self._handle_device_disconnection(cursor, mac, current_time)
            
            # Update LastSeen for all currently connected devices
            for mac in current_macs:
                self._update_device_last_seen(cursor, devices[mac], current_time)
            
            self.connection.commit()
            
            if new_devices or disconnected_devices:
                logger.info(
                    f"Database updated: {len(new_devices)} connected, "
                    f"{len(disconnected_devices)} disconnected"
                )
                
        except pyodbc.Error as e:
            logger.error(f"Error updating database: {e}", exc_info=True)
            self.connection.rollback()
            raise

    def _handle_device_connection(self, cursor, device: Device, timestamp: datetime):
        """
        Handle a device connection event
        
        Args:
            cursor: Database cursor
            device: Device that connected
            timestamp: Connection timestamp
        """
        logger.info(f"New device connected: {device.mac_address} ({device.ip_address})")
        
        # Check if device exists in database
        cursor.execute("""
            SELECT ConnectionID FROM DeviceConnections 
            WHERE MACAddress = ?
        """, device.mac_address)
        
        if cursor.fetchone():
            # Update existing device
            cursor.execute("""
                UPDATE DeviceConnections 
                SET IPAddress = ?, 
                    Hostname = ?,
                    LastSeen = ?, 
                    IsConnected = 1
                WHERE MACAddress = ?
            """, device.ip_address, device.hostname, timestamp, device.mac_address)
        else:
            # Insert new device
            cursor.execute("""
                INSERT INTO DeviceConnections 
                (MACAddress, IPAddress, Hostname, FirstSeen, LastSeen, IsConnected)
                VALUES (?, ?, ?, ?, ?, 1)
            """, device.mac_address, device.ip_address, device.hostname, timestamp, timestamp)
        
        # Log connection event
        cursor.execute("""
            INSERT INTO ConnectionLog 
            (MACAddress, IPAddress, EventType, EventTime)
            VALUES (?, ?, 'CONNECTED', ?)
        """, device.mac_address, device.ip_address, timestamp)

    def _handle_device_disconnection(self, cursor, mac_address: str, timestamp: datetime):
        """
        Handle a device disconnection event
        
        Args:
            cursor: Database cursor
            mac_address: MAC address of disconnected device
            timestamp: Disconnection timestamp
        """
        logger.info(f"Device disconnected: {mac_address}")
        
        # Update device status
        cursor.execute("""
            UPDATE DeviceConnections 
            SET IsConnected = 0
            WHERE MACAddress = ?
        """, mac_address)
        
        # Log disconnection event
        cursor.execute("""
            INSERT INTO ConnectionLog 
            (MACAddress, IPAddress, EventType, EventTime)
            VALUES (?, NULL, 'DISCONNECTED', ?)
        """, mac_address, timestamp)

    def _update_device_last_seen(self, cursor, device: Device, timestamp: datetime):
        """
        Update the last seen timestamp for a device
        
        Args:
            cursor: Database cursor
            device: Device to update
            timestamp: Current timestamp
        """
        cursor.execute("""
            UPDATE DeviceConnections 
            SET LastSeen = ?,
                IPAddress = ?,
                Hostname = ?
            WHERE MACAddress = ?
        """, timestamp, device.ip_address, device.hostname, device.mac_address)

    def get_device_count(self) -> Dict[str, int]:
        """
        Get count of connected and total devices
        
        Returns:
            Dictionary with 'connected' and 'total' counts
        """
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM DeviceConnections WHERE IsConnected = 1")
            connected = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM DeviceConnections")
            total = cursor.fetchone()[0]
            
            return {"connected": connected, "total": total}
        except pyodbc.Error as e:
            logger.error(f"Error getting device count: {e}")
            return {"connected": 0, "total": 0}
