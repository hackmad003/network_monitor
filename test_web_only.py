"""
Test the web dashboard without database/scanner dependencies
This lets you see the UI before fixing all dependencies
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Mock data for testing
MOCK_DEVICES = [
    {
        'mac_address': 'AA:BB:CC:DD:EE:01',
        'ip_address': '192.168.1.100',
        'hostname': 'desktop-pc',
        'device_name': 'Desktop Computer',
        'device_type': 'Computer',
        'vendor': 'Dell',
        'first_seen': '2024-01-01T10:00:00',
        'last_seen': datetime.now().isoformat(),
        'is_connected': True
    },
    {
        'mac_address': 'AA:BB:CC:DD:EE:02',
        'ip_address': '192.168.1.101',
        'hostname': 'iphone',
        'device_name': 'iPhone',
        'device_type': 'Mobile',
        'vendor': 'Apple',
        'first_seen': '2024-01-01T10:00:00',
        'last_seen': datetime.now().isoformat(),
        'is_connected': True
    },
    {
        'mac_address': 'AA:BB:CC:DD:EE:03',
        'ip_address': '192.168.1.102',
        'hostname': 'smart-tv',
        'device_name': 'Living Room TV',
        'device_type': 'TV',
        'vendor': 'Samsung',
        'first_seen': '2024-01-01T10:00:00',
        'last_seen': '2024-01-15T22:00:00',
        'is_connected': False
    }
]

MOCK_EVENTS = [
    {
        'log_id': 1,
        'mac_address': 'AA:BB:CC:DD:EE:02',
        'ip_address': '192.168.1.101',
        'event_type': 'CONNECTED',
        'event_time': datetime.now().isoformat(),
        'hostname': 'iphone',
        'device_name': 'iPhone',
        'device_type': 'Mobile'
    },
    {
        'log_id': 2,
        'mac_address': 'AA:BB:CC:DD:EE:03',
        'ip_address': '192.168.1.102',
        'event_type': 'DISCONNECTED',
        'event_time': '2024-01-15T22:00:00',
        'hostname': 'smart-tv',
        'device_name': 'Living Room TV',
        'device_type': 'TV'
    }
]

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current monitoring status"""
    return jsonify({
        'status': 'running',
        'monitoring_active': True,
        'network': '192.168.1.0/24',
        'scan_interval': 60,
        'connected_devices': 2,
        'total_devices': 3,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/devices')
def get_devices():
    """Get all devices"""
    return jsonify({'devices': MOCK_DEVICES})

@app.route('/api/devices/connected')
def get_connected_devices():
    """Get only connected devices"""
    connected = [d for d in MOCK_DEVICES if d['is_connected']]
    return jsonify({'devices': connected})

@app.route('/api/events')
def get_events():
    """Get recent events"""
    return jsonify({'events': MOCK_EVENTS})

@app.route('/api/statistics')
def get_statistics():
    """Get network statistics"""
    return jsonify({
        'connected_devices': 2,
        'total_devices': 3,
        'connections_24h': 5,
        'disconnections_24h': 3,
        'hourly_activity': [
            {'hour': 10, 'connections': 2, 'disconnections': 1},
            {'hour': 14, 'connections': 1, 'disconnections': 0},
            {'hour': 18, 'connections': 2, 'disconnections': 2}
        ]
    })

@app.route('/api/device/<mac_address>')
def get_device_details(mac_address):
    """Get device details"""
    device = next((d for d in MOCK_DEVICES if d['mac_address'] == mac_address), None)
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device_copy = device.copy()
    device_copy['history'] = [
        {
            'event_type': 'CONNECTED',
            'event_time': datetime.now().isoformat(),
            'ip_address': device['ip_address']
        },
        {
            'event_type': 'DISCONNECTED',
            'event_time': '2024-01-15T22:00:00',
            'ip_address': device['ip_address']
        }
    ]
    
    return jsonify({'device': device_copy})

@app.route('/api/control/start', methods=['POST'])
def start_monitoring():
    """Start monitoring (mock)"""
    return jsonify({'message': 'Monitoring started (DEMO MODE)'})

@app.route('/api/control/stop', methods=['POST'])
def stop_monitoring():
    """Stop monitoring (mock)"""
    return jsonify({'message': 'Monitoring stopped (DEMO MODE)'})

@app.route('/api/control/scan', methods=['POST'])
def trigger_scan():
    """Trigger scan (mock)"""
    return jsonify({'message': 'Scan completed (DEMO MODE)'})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Network Monitor - WEB DASHBOARD TEST MODE")
    print("="*60)
    print("\n✓ Running in TEST MODE with mock data")
    print("✓ No database or network scanner needed")
    print("✓ This lets you see the interface before fixing dependencies")
    print("\n" + "="*60)
    print("🌐 Open your browser: http://localhost:5000")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
