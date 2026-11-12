#!/bin/bash
# 学术动态监控系统 - 启动脚本
# 使用方法：bash start.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ 虚拟环境未找到，请先运行 setup.sh"
    exit 1
fi

echo "🚀 启动学术动态监控系统..."
echo ""
echo "========================================="
echo "  学术动态监控系统"
echo "  监控对象：鲁力立 | 教育元宇宙未来课堂 | 智慧教育产教基地"
echo "========================================="
echo "  访问地址：http://localhost:8888"
echo "  按 Ctrl+C 停止服务"
echo "========================================="
echo ""

cd "$SCRIPT_DIR"
"$VENV_PYTHON" server.py
