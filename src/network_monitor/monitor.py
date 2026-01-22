"""
Main network monitoring orchestration
"""
import logging
import time
from typing import Optional
from .config import Config
from .scanner import NetworkScanner
from .database import DatabaseManager

logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Main network monitoring class that orchestrates scanning and database updates"""

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the network monitor
        
        Args:
            config: Configuration object (loads from environment if None)
        """
        self.config = config or Config.load()
        
        # Initialize components
        self.scanner = NetworkScanner(
            subnet=self.config.network.subnet,
            timeout=self.config.network.timeout
        )
        self.database = DatabaseManager(self.config.database)
        
        logger.info("Network Monitor initialized")
        logger.info(f"Monitoring network: {self.config.network.subnet}")
        logger.info(f"Scan interval: {self.config.network.scan_interval} seconds")

    def scan_once(self) -> bool:
        """
        Perform a single network scan and update database
        
        Returns:
            True if scan was successful, False otherwise
        """
        try:
            # Scan network
            devices = self.scanner.scan()
            
            # Update database
            if devices:
                self.database.update_device_status(devices)
                return True
            else:
                logger.warning("No devices found in scan")
                return False
                
        except Exception as e:
            logger.error(f"Error during scan: {e}", exc_info=True)
            return False

    def run(self):
        """
        Main monitoring loop - runs continuously until interrupted
        """
        logger.info("Starting network monitoring...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                # Perform scan
                self.scan_once()
                
                # Wait for next scan
                logger.info(
                    f"Waiting {self.config.network.scan_interval} seconds until next scan..."
                )
                time.sleep(self.config.network.scan_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}", exc_info=True)
            raise
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.database:
            self.database.close()
        logger.info("Cleanup complete")

    def get_status(self) -> dict:
        """
        Get current monitoring status
        
        Returns:
            Dictionary with monitoring status information
        """
        try:
            device_counts = self.database.get_device_count()
            return {
                "status": "running",
                "network": self.config.network.subnet,
                "scan_interval": self.config.network.scan_interval,
                "connected_devices": device_counts["connected"],
                "total_devices": device_counts["total"],
            }
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
