@echo off
REM 鲁力立学术动态监控 - 独立版启动脚本（Windows）
cd /d "%~dp0"

set PORT=8000
set HTML_FILE=鲁力立学术动态监控_独立版.html

echo ==================================================
echo   学术动态监控 - 启动中...
echo   访问地址: http://localhost:%PORT%/%HTML_FILE%
echo   按 Ctrl+C 停止服务器
echo ==================================================

REM 启动服务器（后台）并打开浏览器
start "" python standalone_server.py

REM 等待服务器启动
timeout /t 2 >nul
start "" http://localhost:%PORT%/%HTML_FILE%

echo 浏览器已打开，服务器运行中...
pause
