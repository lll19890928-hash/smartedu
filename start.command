#!/bin/bash
# 鲁力立学术动态监控 - 独立版启动脚本（macOS）
# 双击此文件即可启动服务器并在浏览器中打开

cd "$(dirname "$0")"

PORT=8000
HTML_FILE="鲁力立学术动态监控_独立版.html"

echo "=================================================="
echo "   学术动态监控 - 启动中..."
echo "   访问地址: http://localhost:$PORT/$HTML_FILE"
echo "   按 Ctrl+C 停止服务器"
echo "=================================================="

# 启动服务器（后台）并打开浏览器
python3 standalone_server.py

# 注意：浏览器由 standalone_server.py 自动打开
