@echo off
cd /d "%~dp0"
where pyw >nul 2>&1
if %errorlevel%==0 (
  start "" pyw -3 "%~dp0terminal_app.py"
  exit /b 0
)
where pythonw >nul 2>&1
if %errorlevel%==0 (
  start "" pythonw "%~dp0terminal_app.py"
  exit /b 0
)
python "%~dp0terminal_app.py"
