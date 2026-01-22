@echo off
echo ====================================
echo Network Device Monitor
echo ====================================
echo.
echo Starting network monitor...
echo Press Ctrl+C to stop
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: This script must be run as Administrator
    echo Right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

python -m network_monitor.main

pause
