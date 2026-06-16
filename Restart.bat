@echo off
taskkill /F /IM python.exe
timeout /t 1
cd /d "%~dp0"
call env\Scripts\activate.bat
env\Scripts\python.exe Roura.py
