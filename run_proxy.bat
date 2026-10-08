@echo off
setlocal
cd /d "%~dp0"

python --version >nul 2>&1
if not errorlevel 1 goto RUN_PYTHON

py --version >nul 2>&1
if not errorlevel 1 goto RUN_PY

echo Python was not found on this computer.
echo Install it from https://python.org
echo During setup, check the box "Add python.exe to PATH".
echo Then double-click this file again.
pause
exit /b 1

:RUN_PYTHON
python proxy_server.py
goto END

:RUN_PY
py proxy_server.py
goto END

:END
pause
