#!/usr/bin/env python3
"""
独立版监控页面 - 迷你服务器
提供静态文件服务 + /api/chat 代理（转发到 DeepSeek API）
双击 start.command 即可启动
"""
import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
import webbrowser
import threading
import time

# ============ 配置 ============
PORT = 8000
# 密钥从环境变量读取，不要把真实 Key 提交进仓库
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")
HTML_FILENAME = "鲁力立学术动态监控_独立版.html"


class ChatProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            self._proxy_deepseek()
        else:
            self.send_error(404)

    def _proxy_deepseek(self):
        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            payload = json.loads(body)
        except Exception:
            self._send_json({"error": {"message": "无效的请求体"}}, 400)
            return

        # 构建转发请求
        req = urllib.request.Request(
            DEEPSEEK_API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            }
        )

        try:
            resp = urllib.request.urlopen(req, timeout=120)
            result = json.loads(resp.read().decode("utf-8"))
            self._send_json(result, 200)
        except urllib.error.HTTPError as e:
            try:
                error_body = json.loads(e.read().decode("utf-8"))
            except Exception:
                error_body = {"message": f"HTTP {e.code}: {e.reason}"}
            self._send_json({"error": error_body}, e.code)
        except Exception as e:
            self._send_json({"error": {"message": f"代理错误: {str(e)}"}}, 500)

    def _send_json(self, data, status_code):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # 静默日志（只显示聊天请求）
        if self.path == "/api/chat":
            print(f"[聊天代理] {self.address_string()} - {args[0] if args else ''}")


def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = ChatProxyHandler
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print("=" * 50)
        print(f"  学术动态监控 - 独立版服务器已启动")
        print(f"  访问地址: http://localhost:{PORT}/{HTML_FILENAME}")
        print(f"  按 Ctrl+C 停止服务器")
        print("=" * 50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止。")


if __name__ == "__main__":
    # 延迟 1 秒后打开浏览器（等服务器启动完成）
    def open_browser():
        time.sleep(1.5)
        url = f"http://localhost:{PORT}/{HTML_FILENAME}"
        webbrowser.open(url)
        print(f"[浏览器] 已自动打开: {url}")

    t = threading.Thread(target=open_browser, daemon=True)
    t.start()

    start_server()
