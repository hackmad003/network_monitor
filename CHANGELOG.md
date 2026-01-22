# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-04

### Added
- Initial release of Network Monitor
- ARP-based network scanning functionality
- SQL Server database integration for device tracking
- Connection/disconnection event logging
- Power BI ready database views
- Configuration via environment variables
- Comprehensive logging system
- Windows batch script for easy startup
- Quick start guide and full documentation

### Features
- Continuous network monitoring with configurable scan intervals
- Automatic device discovery and tracking
- MAC address, IP address, and hostname resolution
- Historical connection data storage
- Support for Windows Authentication and SQL Authentication
- Real-time console and file logging

### Database
- DeviceConnections table for device state management
- ConnectionLog table for event history
- Three pre-built views for reporting:
  - vw_CurrentlyConnected
  - vw_ConnectionHistory
  - vw_DailyConnectionSummary

## [Unreleased]

### Planned
- Web-based dashboard
- Email notifications for specific device events
- MAC vendor lookup integration
- Network performance metrics
- Docker containerization
- REST API for remote access
