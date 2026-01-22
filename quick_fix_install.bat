@echo off
echo ========================================
echo Network Monitor - Fix Installation
echo ========================================
echo.

echo Step 1: Installing Flask and Flask-CORS...
pip install flask flask-cors python-dotenv
echo.

echo Step 2: Installing pyodbc (pre-built)...
pip install pyodbc --prefer-binary
echo.

echo Step 3: Checking if Npcap is needed for Scapy...
echo.
echo IMPORTANT: Scapy needs Npcap on Windows!
echo.
echo Please do the following:
echo 1. Go to: https://npcap.com/#download
echo 2. Download and install Npcap
echo 3. During installation, CHECK "WinPcap API-compatible Mode"
echo 4. Restart your computer
echo 5. Then run this script again
echo.

echo Attempting to install Scapy anyway...
pip install scapy
echo.

echo ========================================
echo Testing installations...
echo ========================================
echo.

python -c "import flask; print('✓ Flask installed')" 2>nul || echo "✗ Flask failed"
python -c "import flask_cors; print('✓ Flask-CORS installed')" 2>nul || echo "✗ Flask-CORS failed"
python -c "import dotenv; print('✓ python-dotenv installed')" 2>nul || echo "✗ python-dotenv failed"
python -c "import pyodbc; print('✓ pyodbc installed')" 2>nul || echo "✗ pyodbc failed - try conda install"
python -c "import scapy; print('✓ scapy installed')" 2>nul || echo "✗ scapy failed - install Npcap first"

echo.
echo ========================================
echo.

pause
