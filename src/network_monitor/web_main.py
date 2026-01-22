"""
Entry point for Network Monitor Web Dashboard
"""
import logging
import sys
import os
from .config import Config
from .web import app, init_app, run_server


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
    """Main entry point for the web dashboard"""
    print("=" * 60)
    print("Network Device Monitor - Web Dashboard")
    print("=" * 60)
    print()
    
    try:
        # Load configuration
        config = Config.load()
        
        # Setup logging
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        # Initialize web application
        init_app(config)
        
        # Get web server settings from environment
        host = os.getenv('WEB_HOST', '0.0.0.0')
        port = int(os.getenv('WEB_PORT', '5000'))
        debug = os.getenv('WEB_DEBUG', 'no').lower() == 'yes'
        auto_start = os.getenv('AUTO_START_MONITORING', 'yes').lower() == 'yes'
        
        print(f"✓ Configuration loaded")
        print(f"✓ Monitoring network: {config.network.subnet}")
        print(f"✓ Scan interval: {config.network.scan_interval} seconds")
        print(f"✓ Web server starting on http://{host}:{port}")
        print()
        print("=" * 60)
        print(f"🌐 Open your browser and navigate to: http://localhost:{port}")
        print("=" * 60)
        print()
        
        if auto_start:
            print("✓ Network monitoring will start automatically")
        else:
            print("ℹ Network monitoring is disabled. Start it from the web interface.")
        
        print()
        print("Press Ctrl+C to stop the server")
        print()
        
        # Run the web server
        run_server(host=host, port=port, debug=debug, auto_start_monitoring=auto_start)
        
    except PermissionError:
        print("\n❌ ERROR: Permission Denied")
        print("\nNetwork scanning requires administrator/root privileges.")
        print("\nPlease run as administrator:")
        print("  Windows: Right-click → 'Run as administrator'")
        print("  Linux/Mac: Use 'sudo python -m network_monitor.web_main'")
        sys.exit(1)
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to start web server: {e}", exc_info=True)
        
        print(f"\n❌ ERROR: {e}")
        print("\nPlease check:")
        print("  1. Your .env file is configured correctly")
        print("  2. SQL Server is running and accessible")
        print("  3. Database has been set up (run database_setup.sql)")
        print("  4. Port 5000 is not already in use")
        print("  5. You have administrator/root privileges")
        print("\nSee network_monitor.log for detailed error information.")
        sys.exit(1)


if __name__ == "__main__":
    main()
