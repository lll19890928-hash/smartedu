#!/usr/bin/env python3
"""
构建独立版 dashboard HTML：所有数据内嵌，无服务器依赖。
动态检测行号（不依赖固定行号）。
"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "static", "dashboard.html")

# ── 1. 读取所有 JSON 数据 ──────────────────────────────────
data = {}
for tid in ["profile", "lulili", "metaverse", "base", "related", "honors"]:
    path = os.path.join(BASE, "results", tid + ".json")
    with open(path, "r", encoding="utf-8") as f:
        data[tid] = json.load(f)
with open(os.path.join(BASE, "static", "yimu.json"), "r", encoding="utf-8") as f:
    data["yimu"] = json.load(f)

# ── 2. 读取源 HTML，动态检测分割点 ─────────────────────────
with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 动态找行号
def find_line(pattern, start=0):
    """找第一个匹配 pattern 的行号（0-based）"""
    for i in range(start, len(lines)):
        if re.search(pattern, lines[i]):
            return i
    return -1

# </head> 的位置
end_head = find_line(r'</head>')
# <body> 的位置
body_start = find_line(r'<body', end_head)
# 第一个 <script> 的位置（在 <body> 之后）
script_start = find_line(r'<script>', body_start)
# </script> 的位置（脚本结束）
script_end = find_line(r'</script>', script_start)
# </body> 的位置
body_end = find_line(r'</body>', script_end)
# init() 函数的位置（在脚本内）
init_start = find_line(r'function init\(\)', script_start)
# init() 结束的位置（在脚本内，找下一个 function 或 </script>）
# 找 switchSection 函数的位置（这是第一个要保留的函数）
switch_start = find_line(r'function switchSection', script_start)

print(f"动态行号: end_head={end_head}, body_start={body_start}, script_start={script_start}, script_end={script_end}")
print(f"  init_start={init_start}, switch_start={switch_start}")

# 分割：
# head_html: 0 .. end_head（包含 </head>）
# body_html: body_start+1 .. script_start-1（<body> 到 <script> 之前）
# func_js: switch_start .. script_end-1（switchSection 函数到 </script> 之前）

head_html = "".join(lines[0:end_head+1])          # 包含 </head>
# body_start 行本身是 <body>，取 body_start 到 script_start-1（包含<body>标签）
body_html = "".join(lines[body_start:script_start])  # 包含 <body> 标签
func_js_lines = lines[switch_start:script_end]
# 过滤掉独立成行的 init(); 调用（避免在函数定义中途提前执行）
func_js_lines = [l for l in func_js_lines if l.strip() != 'init();']
func_js_text = "".join(func_js_lines)

# </script> 之后、</body> 之前的 HTML（聊天窗口等）
post_script_html = "".join(lines[script_end+1:body_end])

# ── 3. 生成嵌入数据 JSON 块 ──────────────────────────────
data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

# 独立版可能被托管在子路径下（如 GitHub Pages 的 /smartedu/），
# 绝对路径 /static/... 会指到站点根目录导致 404，统一改成相对路径
data_json = data_json.replace('"/static/', '"static/')
data_json = re.sub(r'([("\'])/static/', r'\1static/', data_json)

# ── 4. 构造干净的 init 函数 ──────────────────────────────
clean_init = """let ALL_DATA={},currentSection='personal';

function init(){
try{
ALL_DATA=EMBEDDED_DATA;
switchSection('personal');
}catch(e){document.getElementById('contentArea').innerHTML='<div class="empty">⚠️ 数据加载失败：'+escHtml(String(e))+'</div>';}
}
"""

# ── 5. 组装独立版 HTML ──────────────────────────────────
# body_html 包含 <body> 开始标签，确保手机浏览器（iOS Safari/微信）正常解析
output = f"""{head_html}
<script>
var EMBEDDED_DATA={data_json};
</script>
{body_html}
<script>
{clean_init}
{func_js_text}
init();
</script>
{post_script_html}
</body>
</html>"""

# 更新 header 副标题
output = output.replace(
    "四大板块 · 覆盖时间 2011–2026 · 全网新闻链接追踪",
    "独立版 · 全网新闻链接追踪 · 离线可用"
)

# ── 手机兼容性修复 ──────────────────────────────────────
# 1. 独立版不需要调用 /api/meta（手机上无服务器），直接显示固定日期
import datetime
today_str = datetime.date.today().strftime("%Y-%m-%d")
output = output.replace(
    """function loadUpdateTime(){
  fetch('/api/meta').then(function(r){return r.json()}).then(function(d){
    var el=document.getElementById('updateTime');
    if(d&&d.updated_at){
      el.textContent='上次更新：'+d.updated_at;
    }else{
      // 从文件修改时间推断
      var p=new Date(performance.timing.navigationStart||Date.now());
      el.textContent='数据版本：'+p.getFullYear()+'-'+(p.getMonth()+1)+'-'+p.getDate();
    }
  }).catch(function(){
    document.getElementById('updateTime').textContent='数据版本：2026-06';
  });
}""",
    f"""function loadUpdateTime(){{
  // 独立版：直接显示构建日期，无需网络请求（手机离线可用）
  var el=document.getElementById('updateTime');
  if(el) el.textContent='数据版本：{today_str}';
}}"""
)

# ── 6. 写入文件 ──────────────────────────────────────────
paths = [
    os.path.join(BASE, "static", "dashboard_standalone.html"),
    os.path.join(BASE, "鲁力立学术动态监控_独立版.html"),
    # GitHub Pages 入口（Pages 从仓库根目录发布，论文链接 /static/papers/ 可直接命中）
    os.path.join(BASE, "index.html"),
]
for p in paths:
    with open(p, "w", encoding="utf-8") as f:
        f.write(output)

print(f"✅ 独立版已生成")
for p in paths:
    size_kb = os.path.getsize(p) / 1024
    print(f"   {p}  ({size_kb:.0f} KB)")
print(f"   嵌入数据: {len(data)} 个主题, {len(data_json):,} 字符")
