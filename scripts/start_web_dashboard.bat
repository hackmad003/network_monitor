@echo off
REM Start Network Monitor Web Dashboard
REM This script must be run as Administrator for network scanning

echo ========================================
echo Network Monitor Web Dashboard
echo ========================================
echo.

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Using system Python.
)

echo.
echo Starting web dashboard...
echo.

REM Start the web dashboard
python -m src.network_monitor.web_main

echo.
echo Dashboard stopped.
pause
