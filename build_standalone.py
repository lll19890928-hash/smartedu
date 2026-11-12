#!/usr/bin/env python3
"""
构建独立版 dashboard HTML：所有数据内嵌，无服务器依赖。
动态检测行号（不依赖固定行号）。

访问密码：如设置了环境变量 DASHBOARD_PASSWORD（或 .env 中配置），
则把内嵌数据用该密码做 AES-GCM 加密，页面显示密码门，输对才解密渲染。
密码不写入仓库；不设置则构建无密码的公开版。
"""
import json, os, re, base64, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "static", "dashboard.html")


def _load_dotenv_simple():
    """读取项目根目录 .env，补充到环境变量（不覆盖已有值）"""
    path = os.path.join(BASE, ".env")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() and k.strip() not in os.environ:
                os.environ[k.strip()] = v.strip().strip('"').strip("'")


def _get_password():
    _load_dotenv_simple()
    return os.environ.get("DASHBOARD_PASSWORD", "").strip()


def encrypt_payload(plaintext: str, password: str) -> dict:
    """PBKDF2-HMAC-SHA256 派生密钥 + AES-256-GCM 加密，输出 base64 载荷"""
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Random import get_random_bytes

    salt = get_random_bytes(16)
    iv = get_random_bytes(12)
    key = PBKDF2(password, salt, dkLen=32, count=150000, hmac_hash_module=SHA256)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ct, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    b64 = lambda b: base64.b64encode(b).decode()
    return {"v": 1, "iterations": 150000, "salt": b64(salt), "iv": b64(iv), "ct": b64(ct + tag)}

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
# 密码门（可选）：设置 DASHBOARD_PASSWORD 时数据加密 + 门页拦截
DASHBOARD_PASSWORD = _get_password()
if DASHBOARD_PASSWORD:
    enc_payload = json.dumps(encrypt_payload(data_json, DASHBOARD_PASSWORD))
    print(f"🔒 访问密码已启用（数据 AES-GCM 加密，密码不写入文件）")
    gate_css = """
<style>
#lockGate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif}
#lockGate .card{background:rgba(255,255,255,.96);border-radius:18px;padding:38px 34px;width:320px;max-width:86vw;
  box-shadow:0 20px 60px rgba(0,0,0,.35);text-align:center}
#lockGate .icon{font-size:40px;margin-bottom:8px}
#lockGate h1{font-size:19px;color:#333;margin:0 0 4px}
#lockGate p{font-size:13px;color:#888;margin:0 0 18px}
#lockGate input{width:100%;box-sizing:border-box;padding:11px 14px;border:1.5px solid #d5d9f2;border-radius:10px;
  font-size:16px;text-align:center;letter-spacing:2px;outline:none;transition:border .2s}
#lockGate input:focus{border-color:#667eea}
#lockGate button{width:100%;margin-top:14px;padding:11px;border:none;border-radius:10px;font-size:15px;color:#fff;
  background:linear-gradient(135deg,#667eea,#764ba2);cursor:pointer;letter-spacing:4px}
#lockGate button:active{opacity:.85}
#lockGate .err{display:none;margin-top:12px;font-size:13px;color:#e74c3c}
body.locked>*:not(#lockGate){display:none!important}
</style>"""
    gate_html = """
<div id="lockGate">
  <div class="card">
    <div class="icon">🔒</div>
    <h1>学术动态监控系统</h1>
    <p>内容已加密，请输入访问密码</p>
    <input id="lockPwd" type="password" inputmode="numeric" autocomplete="off" placeholder="访问密码"/>
    <button id="lockBtn">解 锁</button>
    <div class="err" id="lockErr">密码不正确，请重试</div>
  </div>
</div>
<script>
function _b64buf(b){var s=atob(b),n=s.length,r=new Uint8Array(n);for(var i=0;i<n;i++)r[i]=s.charCodeAt(i);return r}
async function _deriveKey(pw){
  var km=await crypto.subtle.importKey("raw",new TextEncoder().encode(pw),"PBKDF2",false,["deriveKey"]);
  return await crypto.subtle.deriveKey({name:"PBKDF2",salt:_b64buf(ENC_PAYLOAD.salt),
    iterations:ENC_PAYLOAD.iterations||150000,hash:"SHA-256"},km,{name:"AES-GCM",length:256},false,["decrypt"]);
}
async function _tryUnlock(pw){
  var key=await _deriveKey(pw);
  var plain=await crypto.subtle.decrypt({name:"AES-GCM",iv:_b64buf(ENC_PAYLOAD.iv)},key,_b64buf(ENC_PAYLOAD.ct));
  window.EMBEDDED_DATA=JSON.parse(new TextDecoder().decode(plain));
}
async function unlockWith(pw){
  try{
    await _tryUnlock(pw);
    try{sessionStorage.setItem("smartedu_gate",pw)}catch(e){}
    document.getElementById("lockGate").remove();
    document.body.classList.remove("locked");
    init();
  }catch(e){
    var err=document.getElementById("lockErr");
    if(err){err.style.display="block"}
    document.getElementById("lockPwd").select();
  }
}
function _gateReady(){
  var btn=document.getElementById("lockBtn"),input=document.getElementById("lockPwd");
  btn.addEventListener("click",function(){unlockWith(input.value)});
  input.addEventListener("keydown",function(e){if(e.key==="Enter")unlockWith(input.value)});
  var saved=null;try{saved=sessionStorage.getItem("smartedu_gate")}catch(e){}
  if(saved){unlockWith(saved)}else{input.focus()}
}
_gateReady();
</script>"""
    output = f"""{head_html}{gate_css}
<script>
var ENC_PAYLOAD={enc_payload};
var EMBEDDED_DATA=null;
</script>
{body_html.replace('<body', '<body class="locked"', 1)}
<script>
{clean_init}
{func_js_text}
</script>
{post_script_html}
{gate_html}
</body>
</html>"""
else:
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
