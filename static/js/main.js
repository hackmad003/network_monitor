// Network Monitor Dashboard JavaScript

// Configuration
const REFRESH_INTERVAL = 5000; // 5 seconds
let refreshIntervalId = null;
let allDevices = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Network Monitor Dashboard initialized');
    loadDashboard();
    startAutoRefresh();
});

// Load all dashboard data
function loadDashboard() {
    loadStatus();
    loadStatistics();
    loadDevices();
    loadEvents();
}

// Auto-refresh
function startAutoRefresh() {
    refreshIntervalId = setInterval(() => {
        loadDashboard();
    }, REFRESH_INTERVAL);
}

function stopAutoRefresh() {
    if (refreshIntervalId) {
        clearInterval(refreshIntervalId);
        refreshIntervalId = null;
    }
}

// Load status information
async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.error) {
            showToast('Error loading status: ' + data.error, 'error');
            return;
        }
        
        // Update status bar
        const statusText = data.monitoring_active ? 'Monitoring Active' : 'Monitoring Stopped';
        const statusColor = data.monitoring_active ? 'var(--success-color)' : 'var(--danger-color)';
        document.getElementById('statusText').textContent = statusText;
        document.getElementById('statusText').style.color = statusColor;
        
        document.getElementById('networkText').textContent = data.network;
        document.getElementById('intervalText').textContent = data.scan_interval;
        
        const lastUpdate = new Date().toLocaleTimeString();
        document.getElementById('lastUpdate').textContent = 'Last Update: ' + lastUpdate;
        
        // Update monitor toggle button
        const toggleBtn = document.getElementById('monitorToggle');
        const toggleText = document.getElementById('monitorToggleText');
        if (data.monitoring_active) {
            toggleBtn.classList.add('monitoring-active');
            toggleBtn.innerHTML = '<i class="fas fa-stop"></i> <span id="monitorToggleText">Stop</span>';
        } else {
            toggleBtn.classList.remove('monitoring-active');
            toggleBtn.innerHTML = '<i class="fas fa-play"></i> <span id="monitorToggleText">Start</span>';
        }
        
        // Update basic counts
        document.getElementById('connectedCount').textContent = data.connected_devices || 0;
        document.getElementById('totalCount').textContent = data.total_devices || 0;
        
    } catch (error) {
        console.error('Error loading status:', error);
        showToast('Failed to load status', 'error');
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading statistics:', data.error);
            return;
        }
        
        document.getElementById('connections24h').textContent = data.connections_24h || 0;
        document.getElementById('disconnections24h').textContent = data.disconnections_24h || 0;
        
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load devices
async function loadDevices() {
    try {
        const response = await fetch('/api/devices');
        const data = await response.json();
        
        if (data.error) {
            showToast('Error loading devices: ' + data.error, 'error');
            return;
        }
        
        allDevices = data.devices || [];
        renderDevices(allDevices);
        
    } catch (error) {
        console.error('Error loading devices:', error);
        showToast('Failed to load devices', 'error');
    }
}

// Render devices table
function renderDevices(devices) {
    const tbody = document.getElementById('deviceTableBody');
    
    if (devices.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="loading">No devices found</td></tr>';
        return;
    }
    
    tbody.innerHTML = devices.map(device => {
        const statusBadge = device.is_connected 
            ? '<span class="status-badge connected">Connected</span>'
            : '<span class="status-badge disconnected">Disconnected</span>';
        
        const deviceName = device.device_name || device.hostname || 'Unknown Device';
        const hostname = device.hostname || '-';
        const lastSeen = device.last_seen ? formatDateTime(device.last_seen) : '-';
        
        return `
            <tr>
                <td>${statusBadge}</td>
                <td>${escapeHtml(deviceName)}</td>
                <td>${escapeHtml(device.ip_address || '-')}</td>
                <td><code>${escapeHtml(device.mac_address)}</code></td>
                <td>${escapeHtml(hostname)}</td>
                <td>${lastSeen}</td>
                <td>
                    <div class="device-actions">
                        <button class="action-btn" onclick="showDeviceDetails('${device.mac_address}')" title="View Details">
                            <i class="fas fa-info-circle"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// Filter devices
function filterDevices() {
    const filterValue = document.getElementById('deviceFilter').value;
    const searchValue = document.getElementById('searchBox').value.toLowerCase();
    
    let filtered = allDevices;
    
    // Apply status filter
    if (filterValue === 'connected') {
        filtered = filtered.filter(d => d.is_connected);
    } else if (filterValue === 'disconnected') {
        filtered = filtered.filter(d => !d.is_connected);
    }
    
    // Apply search filter
    if (searchValue) {
        filtered = filtered.filter(d => {
            const searchString = [
                d.device_name,
                d.hostname,
                d.ip_address,
                d.mac_address
            ].filter(Boolean).join(' ').toLowerCase();
            
            return searchString.includes(searchValue);
        });
    }
    
    renderDevices(filtered);
}

// Load recent events
async function loadEvents() {
    try {
        const response = await fetch('/api/events?limit=20');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading events:', data.error);
            return;
        }
        
        renderEvents(data.events || []);
        
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Render events
function renderEvents(events) {
    const eventsList = document.getElementById('eventsList');
    
    if (events.length === 0) {
        eventsList.innerHTML = '<div class="loading">No recent events</div>';
        return;
    }
    
    eventsList.innerHTML = events.map(event => {
        const isConnected = event.event_type === 'CONNECTED';
        const iconClass = isConnected ? 'connected' : 'disconnected';
        const icon = isConnected ? 'fa-arrow-up' : 'fa-arrow-down';
        const deviceName = event.device_name || event.hostname || 'Unknown Device';
        const eventTime = formatDateTime(event.event_time);
        
        return `
            <div class="event-item">
                <div class="event-icon ${iconClass}">
                    <i class="fas ${icon}"></i>
                </div>
                <div class="event-content">
                    <div class="event-title">${escapeHtml(deviceName)}</div>
                    <div class="event-details">
                        ${event.event_type} • ${escapeHtml(event.ip_address || '-')} • ${escapeHtml(event.mac_address)}
                    </div>
                </div>
                <div class="event-time">${eventTime}</div>
            </div>
        `;
    }).join('');
}

// Show device details modal
async function showDeviceDetails(macAddress) {
    const modal = document.getElementById('deviceModal');
    const modalBody = document.getElementById('modalBody');
    
    modal.classList.add('active');
    modalBody.innerHTML = '<div class="loading">Loading device details...</div>';
    
    try {
        const response = await fetch(`/api/device/${encodeURIComponent(macAddress)}`);
        const data = await response.json();
        
        if (data.error) {
            modalBody.innerHTML = `<div class="loading">Error: ${escapeHtml(data.error)}</div>`;
            return;
        }
        
        const device = data.device;
        const statusBadge = device.is_connected 
            ? '<span class="status-badge connected">Connected</span>'
            : '<span class="status-badge disconnected">Disconnected</span>';
        
        modalBody.innerHTML = `
            <div class="device-info">
                <div class="info-item">
                    <div class="info-label">Status</div>
                    <div class="info-value">${statusBadge}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Device Name</div>
                    <div class="info-value">${escapeHtml(device.device_name || device.hostname || 'Unknown')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">IP Address</div>
                    <div class="info-value">${escapeHtml(device.ip_address || '-')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">MAC Address</div>
                    <div class="info-value"><code>${escapeHtml(device.mac_address)}</code></div>
                </div>
                <div class="info-item">
                    <div class="info-label">Hostname</div>
                    <div class="info-value">${escapeHtml(device.hostname || '-')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Device Type</div>
                    <div class="info-value">${escapeHtml(device.device_type || '-')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Vendor</div>
                    <div class="info-value">${escapeHtml(device.vendor || '-')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">First Seen</div>
                    <div class="info-value">${formatDateTime(device.first_seen)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Seen</div>
                    <div class="info-value">${formatDateTime(device.last_seen)}</div>
                </div>
            </div>
            
            <div class="history-section">
                <h3>Connection History (Last 100 Events)</h3>
                <div class="table-container">
                    <table class="history-table">
                        <thead>
                            <tr>
                                <th>Event</th>
                                <th>Time</th>
                                <th>IP Address</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${device.history.map(event => {
                                const statusBadge = event.event_type === 'CONNECTED'
                                    ? '<span class="status-badge connected">Connected</span>'
                                    : '<span class="status-badge disconnected">Disconnected</span>';
                                return `
                                    <tr>
                                        <td>${statusBadge}</td>
                                        <td>${formatDateTime(event.event_time)}</td>
                                        <td>${escapeHtml(event.ip_address || '-')}</td>
                                    </tr>
                                `;
                            }).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
    } catch (error) {
        console.error('Error loading device details:', error);
        modalBody.innerHTML = '<div class="loading">Failed to load device details</div>';
    }
}

// Close modal
function closeModal() {
    document.getElementById('deviceModal').classList.remove('active');
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('deviceModal');
    if (event.target === modal) {
        closeModal();
    }
}

// Toggle monitoring
async function toggleMonitoring() {
    const response = await fetch('/api/status');
    const status = await response.json();
    
    const endpoint = status.monitoring_active ? '/api/control/stop' : '/api/control/start';
    const action = status.monitoring_active ? 'stopped' : 'started';
    
    try {
        const response = await fetch(endpoint, { method: 'POST' });
        const data = await response.json();
        
        if (response.ok) {
            showToast(`Monitoring ${action} successfully`, 'success');
            loadStatus();
        } else {
            showToast(data.error || `Failed to ${action.slice(0, -2)} monitoring`, 'error');
        }
    } catch (error) {
        console.error('Error toggling monitoring:', error);
        showToast('Failed to toggle monitoring', 'error');
    }
}

// Trigger manual scan
async function triggerScan() {
    const btn = document.getElementById('scanBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-sync fa-spin"></i> Scanning...';
    
    try {
        const response = await fetch('/api/control/scan', { method: 'POST' });
        const data = await response.json();
        
        if (response.ok) {
            showToast('Scan completed successfully', 'success');
            loadDashboard();
        } else {
            showToast(data.error || 'Failed to perform scan', 'error');
        }
    } catch (error) {
        console.error('Error triggering scan:', error);
        showToast('Failed to trigger scan', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-sync"></i> Scan Now';
    }
}

// Refresh events manually
function refreshEvents() {
    loadEvents();
    showToast('Events refreshed', 'success');
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility: Format date/time
function formatDateTime(isoString) {
    if (!isoString) return '-';
    
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) {
        return 'Just now';
    } else if (diffMins < 60) {
        return `${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
    } else if (diffMins < 1440) {
        const hours = Math.floor(diffMins / 60);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
        return date.toLocaleString();
    }
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
