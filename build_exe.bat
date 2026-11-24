@echo off
cd /d "%~dp0"
python -m PyInstaller --noconfirm --clean --windowed --onefile --name cyber_code --icon "assets/cyber_code.ico" --add-data "fonts;fonts" --add-data "assets/cyber_code.ico;assets" terminal_app.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)
echo.
echo Built: "%~dp0dist\cyber_code.exe"
pause
