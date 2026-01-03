-- Network Monitor Database Setup Script
-- Run this in SQL Server Management Studio (SSMS)

-- Create the database
CREATE DATABASE NetworkMonitor;
GO

USE NetworkMonitor;
GO

-- Table to store known devices and their current status
CREATE TABLE DeviceConnections (
    ConnectionID INT IDENTITY(1,1) PRIMARY KEY,
    MACAddress VARCHAR(17) NOT NULL UNIQUE,
    IPAddress VARCHAR(15),
    Hostname VARCHAR(255),
    FirstSeen DATETIME NOT NULL,
    LastSeen DATETIME NOT NULL,
    IsConnected BIT DEFAULT 1,
    DeviceName VARCHAR(255), -- Friendly name you can manually assign
    DeviceType VARCHAR(50),   -- Will be populated automatically where possible
    Vendor VARCHAR(255)       -- MAC address vendor lookup
);

-- Table to log all connection/disconnection events
CREATE TABLE ConnectionLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    MACAddress VARCHAR(17) NOT NULL,
    IPAddress VARCHAR(15),
    EventType VARCHAR(20) NOT NULL, -- 'CONNECTED' or 'DISCONNECTED'
    EventTime DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT FK_ConnectionLog_Device 
        FOREIGN KEY (MACAddress) 
        REFERENCES DeviceConnections(MACAddress)
);

-- Indexes for better query performance
CREATE INDEX IX_DeviceConnections_LastSeen ON DeviceConnections(LastSeen);
CREATE INDEX IX_DeviceConnections_IsConnected ON DeviceConnections(IsConnected);
CREATE INDEX IX_ConnectionLog_EventTime ON ConnectionLog(EventTime);
CREATE INDEX IX_ConnectionLog_MACAddress ON ConnectionLog(MACAddress);
CREATE INDEX IX_ConnectionLog_EventType ON ConnectionLog(EventType);

-- Create some useful views for Power BI

-- View: Current connected devices
CREATE VIEW vw_CurrentlyConnected AS
SELECT 
    MACAddress,
    IPAddress,
    Hostname,
    COALESCE(DeviceName, Hostname, 'Unknown Device') AS DisplayName,
    DeviceType,
    Vendor,
    FirstSeen,
    LastSeen,
    DATEDIFF(MINUTE, FirstSeen, LastSeen) AS MinutesConnected
FROM DeviceConnections
WHERE IsConnected = 1;
GO

-- View: Connection history summary
CREATE VIEW vw_ConnectionHistory AS
SELECT 
    dc.MACAddress,
    COALESCE(dc.DeviceName, dc.Hostname, 'Unknown Device') AS DisplayName,
    dc.DeviceType,
    dc.Vendor,
    cl.EventType,
    cl.EventTime,
    cl.IPAddress
FROM ConnectionLog cl
INNER JOIN DeviceConnections dc ON cl.MACAddress = dc.MACAddress;
GO

-- View: Daily connection summary
CREATE VIEW vw_DailyConnectionSummary AS
SELECT 
    CAST(EventTime AS DATE) AS Date,
    COUNT(CASE WHEN EventType = 'CONNECTED' THEN 1 END) AS TotalConnections,
    COUNT(CASE WHEN EventType = 'DISCONNECTED' THEN 1 END) AS TotalDisconnections,
    COUNT(DISTINCT MACAddress) AS UniqueDevices
FROM ConnectionLog
GROUP BY CAST(EventTime AS DATE);
GO

PRINT 'Database setup complete! You can now run the Python network monitor.';
