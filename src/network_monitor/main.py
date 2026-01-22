"""
Entry point for Network Monitor application
"""
import logging
import sys
from .config import Config
from .monitor import NetworkMonitor


def setup_logging(config: Config):
    """
    Configure logging based on configuration
    
    Args:
        config: Application configuration
    """
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
        handlers=[
            logging.FileHandler(config.logging.file_path),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point for the application"""
    print("=" * 60)
    print("Network Device Monitor")
    print("=" * 60)
    print()
    
    try:
        # Load configuration
        config = Config.load()
        
        # Setup logging
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        # Create and run monitor
        monitor = NetworkMonitor(config)
        monitor.run()
        
    except PermissionError:
        print("\n❌ ERROR: Permission Denied")
        print("\nNetwork scanning requires administrator/root privileges.")
        print("\nPlease run as administrator:")
        print("  Windows: Right-click → 'Run as administrator'")
        print("  Linux/Mac: Use 'sudo python -m network_monitor.main'")
        sys.exit(1)
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to start monitor: {e}", exc_info=True)
        
        print(f"\n❌ ERROR: {e}")
        print("\nPlease check:")
        print("  1. Your .env file is configured correctly")
        print("  2. SQL Server is running and accessible")
        print("  3. Database has been set up (run database_setup.sql)")
        print("  4. You have administrator/root privileges")
        print("\nSee network_monitor.log for detailed error information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
