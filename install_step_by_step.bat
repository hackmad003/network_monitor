@echo off
REM Installation fix for Python 3.14.x on Windows
echo ========================================
echo Network Monitor - Step by Step Install
echo ========================================
echo.
echo Your Python version:
python --version
echo.
echo ========================================
echo.

echo Step 1/5: Installing Flask and Flask-CORS (web framework)...
pip install flask flask-cors
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Flask. Check internet connection.
    pause
    exit /b 1
)
echo ✓ Flask installed successfully!
echo.

echo Step 2/5: Installing python-dotenv (configuration)...
pip install python-dotenv
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install python-dotenv.
    pause
    exit /b 1
)
echo ✓ python-dotenv installed successfully!
echo.

echo Step 3/5: Installing pyodbc (database driver)...
echo This might take a moment and requires Visual C++ build tools...
pip install pyodbc
if %errorlevel% neq 0 (
    echo.
    echo WARNING: pyodbc installation failed.
    echo This is OK for now - you can test the web interface without it.
    echo.
    echo To fix later, install: Visual C++ Build Tools
    echo Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
)
echo.

echo Step 4/5: Installing scapy (network scanner)...
echo.
echo IMPORTANT: Scapy needs Npcap to work on Windows!
echo.
echo Please ensure you have Npcap installed:
echo 1. Download from: https://npcap.com/#download
echo 2. Run installer as Administrator
echo 3. CHECK the box: "Install Npcap in WinPcap API-compatible Mode"
echo 4. Complete installation
echo.
pause
echo.
echo Now attempting to install scapy...
pip install scapy
if %errorlevel% neq 0 (
    echo.
    echo WARNING: scapy installation failed.
    echo Make sure Npcap is installed first, then try again.
    echo.
)
echo.

echo Step 5/5: Verifying installations...
echo ========================================
echo.

python -c "import flask; print('✓ Flask: OK')" 2>nul || echo "✗ Flask: FAILED"
python -c "import flask_cors; print('✓ Flask-CORS: OK')" 2>nul || echo "✗ Flask-CORS: FAILED"
python -c "import dotenv; print('✓ python-dotenv: OK')" 2>nul || echo "✗ python-dotenv: FAILED"
python -c "import pyodbc; print('✓ pyodbc: OK')" 2>nul || echo "✗ pyodbc: FAILED (needed for database)"
python -c "import scapy; print('✓ scapy: OK')" 2>nul || echo "✗ scapy: FAILED (needed for scanning)"

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo If pyodbc or scapy failed, you can still test the web interface.
echo See INSTALL_FIX_WINDOWS.md for detailed troubleshooting.
echo.
pause
