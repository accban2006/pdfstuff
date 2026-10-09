@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
  echo Please follow README.md to create the Python 3.12 environment first.
  pause
  exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" -m pdftomd
