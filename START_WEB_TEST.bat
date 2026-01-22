@echo off
echo ========================================
echo Network Monitor - Web Dashboard TEST
echo ========================================
echo.
echo This runs the web dashboard with MOCK data
echo No database or network scanning needed!
echo.
echo Installing ONLY Flask and Flask-CORS...
pip install flask flask-cors
echo.
echo ========================================
echo Starting test web server...
echo ========================================
echo.
python test_web_only.py
pause
