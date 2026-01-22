"""
Web dashboard for Network Monitor
"""
import logging
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from typing import Optional
from .config import Config
from .database import DatabaseManager
from .monitor import NetworkMonitor

logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='../../templates',
            static_folder='../../static')
CORS(app)

# Global variables
config: Optional[Config] = None
db_manager: Optional[DatabaseManager] = None
monitor: Optional[NetworkMonitor] = None
monitor_thread: Optional[threading.Thread] = None
monitoring_active = False


def init_app(app_config: Config):
    """Initialize the web application with configuration"""
    global config, db_manager
    config = app_config
    db_manager = DatabaseManager(config.database)
    logger.info("Web application initialized")


def start_monitoring():
    """Start the network monitoring in a background thread"""
    global monitor, monitor_thread, monitoring_active
    
    if monitoring_active:
        logger.warning("Monitoring is already active")
        return
    
    try:
        monitor = NetworkMonitor(config)
        monitoring_active = True
        
        def monitoring_loop():
            global monitoring_active
            logger.info("Background monitoring started")
            try:
                while monitoring_active:
                    monitor.scan_once()
                    time.sleep(config.network.scan_interval)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                monitoring_active = False
        
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()
        logger.info("Monitoring thread started")
        
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}", exc_info=True)
        monitoring_active = False
        raise


def stop_monitoring():
    """Stop the network monitoring"""
    global monitoring_active
    monitoring_active = False
    logger.info("Monitoring stopped")


# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get current monitoring status"""
    try:
        device_counts = db_manager.get_device_count()
        return jsonify({
            'status': 'running' if monitoring_active else 'stopped',
            'monitoring_active': monitoring_active,
            'network': config.network.subnet,
            'scan_interval': config.network.scan_interval,
            'connected_devices': device_counts['connected'],
            'total_devices': device_counts['total'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices')
def get_devices():
    """Get all devices with their current status"""
    try:
        cursor = db_manager.connection.cursor()
        cursor.execute("""
            SELECT 
                MACAddress,
                IPAddress,
                Hostname,
                DeviceName,
                DeviceType,
                Vendor,
                FirstSeen,
                LastSeen,
                IsConnected
            FROM DeviceConnections
            ORDER BY IsConnected DESC, LastSeen DESC
        """)
        
        devices = []
        for row in cursor.fetchall():
            devices.append({
                'mac_address': row.MACAddress,
                'ip_address': row.IPAddress,
                'hostname': row.Hostname,
                'device_name': row.DeviceName,
                'device_type': row.DeviceType,
                'vendor': row.Vendor,
                'first_seen': row.FirstSeen.isoformat() if row.FirstSeen else None,
                'last_seen': row.LastSeen.isoformat() if row.LastSeen else None,
                'is_connected': bool(row.IsConnected)
            })
        
        return jsonify({'devices': devices})
    except Exception as e:
        logger.error(f"Error getting devices: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices/connected')
def get_connected_devices():
    """Get only currently connected devices"""
    try:
        cursor = db_manager.connection.cursor()
        cursor.execute("""
            SELECT 
                MACAddress,
                IPAddress,
                Hostname,
                DeviceName,
                DeviceType,
                Vendor,
                FirstSeen,
                LastSeen
            FROM DeviceConnections
            WHERE IsConnected = 1
            ORDER BY LastSeen DESC
        """)
        
        devices = []
        for row in cursor.fetchall():
            devices.append({
                'mac_address': row.MACAddress,
                'ip_address': row.IPAddress,
                'hostname': row.Hostname,
                'device_name': row.DeviceName,
                'device_type': row.DeviceType,
                'vendor': row.Vendor,
                'first_seen': row.FirstSeen.isoformat() if row.FirstSeen else None,
                'last_seen': row.LastSeen.isoformat() if row.LastSeen else None,
                'is_connected': True
            })
        
        return jsonify({'devices': devices})
    except Exception as e:
        logger.error(f"Error getting connected devices: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/events')
def get_events():
    """Get recent connection events"""
    try:
        # Get limit from query parameter, default to 50
        limit = request.args.get('limit', 50, type=int)
        
        cursor = db_manager.connection.cursor()
        cursor.execute(f"""
            SELECT TOP {limit}
                cl.LogID,
                cl.MACAddress,
                cl.IPAddress,
                cl.EventType,
                cl.EventTime,
                dc.Hostname,
                dc.DeviceName,
                dc.DeviceType
            FROM ConnectionLog cl
            LEFT JOIN DeviceConnections dc ON cl.MACAddress = dc.MACAddress
            ORDER BY cl.EventTime DESC
        """)
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'log_id': row.LogID,
                'mac_address': row.MACAddress,
                'ip_address': row.IPAddress,
                'event_type': row.EventType,
                'event_time': row.EventTime.isoformat() if row.EventTime else None,
                'hostname': row.Hostname,
                'device_name': row.DeviceName,
                'device_type': row.DeviceType
            })
        
        return jsonify({'events': events})
    except Exception as e:
        logger.error(f"Error getting events: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """Get network statistics"""
    try:
        cursor = db_manager.connection.cursor()
        
        # Get device counts
        device_counts = db_manager.get_device_count()
        
        # Get events in last 24 hours
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN EventType = 'CONNECTED' THEN 1 END) AS connections_24h,
                COUNT(CASE WHEN EventType = 'DISCONNECTED' THEN 1 END) AS disconnections_24h
            FROM ConnectionLog
            WHERE EventTime >= DATEADD(HOUR, -24, GETDATE())
        """)
        row = cursor.fetchone()
        connections_24h = row.connections_24h if row else 0
        disconnections_24h = row.disconnections_24h if row else 0
        
        # Get hourly connection activity for last 24 hours
        cursor.execute("""
            SELECT 
                DATEPART(HOUR, EventTime) AS hour,
                COUNT(CASE WHEN EventType = 'CONNECTED' THEN 1 END) AS connections,
                COUNT(CASE WHEN EventType = 'DISCONNECTED' THEN 1 END) AS disconnections
            FROM ConnectionLog
            WHERE EventTime >= DATEADD(HOUR, -24, GETDATE())
            GROUP BY DATEPART(HOUR, EventTime)
            ORDER BY hour
        """)
        
        hourly_activity = []
        for row in cursor.fetchall():
            hourly_activity.append({
                'hour': row.hour,
                'connections': row.connections,
                'disconnections': row.disconnections
            })
        
        return jsonify({
            'connected_devices': device_counts['connected'],
            'total_devices': device_counts['total'],
            'connections_24h': connections_24h,
            'disconnections_24h': disconnections_24h,
            'hourly_activity': hourly_activity
        })
    except Exception as e:
        logger.error(f"Error getting statistics: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/device/<mac_address>')
def get_device_details(mac_address):
    """Get detailed information about a specific device"""
    try:
        cursor = db_manager.connection.cursor()
        
        # Get device info
        cursor.execute("""
            SELECT 
                MACAddress,
                IPAddress,
                Hostname,
                DeviceName,
                DeviceType,
                Vendor,
                FirstSeen,
                LastSeen,
                IsConnected
            FROM DeviceConnections
            WHERE MACAddress = ?
        """, mac_address)
        
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Device not found'}), 404
        
        device = {
            'mac_address': row.MACAddress,
            'ip_address': row.IPAddress,
            'hostname': row.Hostname,
            'device_name': row.DeviceName,
            'device_type': row.DeviceType,
            'vendor': row.Vendor,
            'first_seen': row.FirstSeen.isoformat() if row.FirstSeen else None,
            'last_seen': row.LastSeen.isoformat() if row.LastSeen else None,
            'is_connected': bool(row.IsConnected)
        }
        
        # Get connection history
        cursor.execute("""
            SELECT TOP 100
                EventType,
                EventTime,
                IPAddress
            FROM ConnectionLog
            WHERE MACAddress = ?
            ORDER BY EventTime DESC
        """, mac_address)
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'event_type': row.EventType,
                'event_time': row.EventTime.isoformat() if row.EventTime else None,
                'ip_address': row.IPAddress
            })
        
        device['history'] = history
        
        return jsonify({'device': device})
    except Exception as e:
        logger.error(f"Error getting device details: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/control/start', methods=['POST'])
def start_monitoring_endpoint():
    """Start network monitoring"""
    try:
        if monitoring_active:
            return jsonify({'message': 'Monitoring is already active'}), 200
        
        start_monitoring()
        return jsonify({'message': 'Monitoring started successfully'}), 200
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/control/stop', methods=['POST'])
def stop_monitoring_endpoint():
    """Stop network monitoring"""
    try:
        stop_monitoring()
        return jsonify({'message': 'Monitoring stopped successfully'}), 200
    except Exception as e:
        logger.error(f"Error stopping monitoring: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/control/scan', methods=['POST'])
def trigger_scan():
    """Trigger an immediate network scan"""
    try:
        if not monitor:
            return jsonify({'error': 'Monitoring is not initialized'}), 400
        
        monitor.scan_once()
        return jsonify({'message': 'Scan completed successfully'}), 200
    except Exception as e:
        logger.error(f"Error triggering scan: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


def run_server(host='0.0.0.0', port=5000, debug=False, auto_start_monitoring=True):
    """
    Run the web server
    
    Args:
        host: Host address to bind to
        port: Port number to listen on
        debug: Enable debug mode
        auto_start_monitoring: Automatically start monitoring on server start
    """
    if auto_start_monitoring:
        start_monitoring()
    
    logger.info(f"Starting web server on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)
