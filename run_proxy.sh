#!/bin/bash
cd "$(dirname "$0")"

if command -v python3 &>/dev/null; then
  python3 proxy_server.py
elif command -v python &>/dev/null; then
  python proxy_server.py
else
  echo "파이썬이 설치되어 있지 않습니다. https://python.org 에서 설치 후 다시 실행해주세요."
  read -p "엔터를 누르면 종료합니다..." _
fi
