@echo off
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
  python proxy_server.py
  goto :end
)

where py >nul 2>nul
if %errorlevel%==0 (
  py proxy_server.py
  goto :end
)

echo 파이썬이 설치되어 있지 않습니다.
echo https://python.org 에서 설치한 뒤(설치 화면에서 "Add python.exe to PATH" 체크) 이 파일을 다시 더블클릭하세요.
pause
exit /b 1

:end
pause
