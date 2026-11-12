import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, 'static')
RESULTS = os.path.join(BASE, 'results')

# 读取模板 dashboard.html
with open(os.path.join(STATIC, 'dashboard.html'), 'r', encoding='utf-8') as f:
    html = f.read()

print(f"模板大小: {len(html)/1024:.1f} KB")

# 读取所有JSON数据
all_data = {}
for fname in ['lulili.json', 'base.json', 'metaverse.json', 'yimu.json', 'related.json', 'honors.json', 'profile.json']:
    fpath = os.path.join(RESULTS, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        all_data[fname.replace('.json', '')] = json.load(f)
print(f"已读取 {len(all_data)} 个JSON文件")

# 策略：完全重写HTML，嵌入数据，移除所有/api/调用
# 1. 在数据嵌入区（</body>之前）插入 ALL_DATA
# 2. 把所有 fetch('/api/...') 替换成从 ALL_DATA 读取

# 先嵌入数据：在 </body> 前插入 <script> 块
data_script = f'<script>\nconst ALL_DATA = {json.dumps(all_data, ensure_ascii=False, indent=2)};\n</script>\n'

# 找到 </body> 位置
body_idx = html.rfind('</body>')
if body_idx == -1:
    print("❌ 未找到 </body>")
    exit(1)

html_new = html[:body_idx] + data_script + html[body_idx:]

# 替换所有 /api/ 调用为从 ALL_DATA 读取
# 替换1: fetch('/api/search?topic=...') → 从 ALL_DATA 同步读取
# 由于这是独立版，我们用一个统一的拦截函数

interceptor = '''
<script>
// 离线独立版：拦截所有 /api/ 调用，改为从 ALL_DATA 读取
(function(){
  const origFetch = window.fetch;
  window.fetch = function(url) {
    if (typeof url === 'string' && url.includes('/api/')) {
      return new Promise((resolve) => {
        // 解析 url 获取 topic
        const u = new URL(url, window.location.href);
        const params = new URLSearchParams(u.search);
        const topic = params.get('topic') || 'lulili';
        const q = params.get('q') || '';
        let data = ALL_DATA[topic] || {results:[], total:0};
        // 简单搜索过滤
        if (q && data.results) {
          const filtered = data.results.filter(r => 
            (r.title||'').includes(q) || (r.summary||'').includes(q) || (r.title_full||'').includes(q)
          );
          data = {...data, results: filtered, total: filtered.length};
        }
        resolve(new Response(JSON.stringify(data), {headers:{'Content-Type':'application/json'}}));
      });
    }
    return origFetch.apply(this, arguments);
  };
})();
</script>
'''

# 在 <head> 结束前插入拦截器
head_idx = html_new.find('</head>')
if head_idx != -1:
    html_new = html_new[:head_idx] + interceptor + html_new[head_idx:]

# 还需要处理：聊天功能（/api/chat）→ 提示离线
chat_offline = '''
<script>
function offlineChatNotice() {
  return new Promise((resolve) => {
    resolve({answer: "⚠️ 离线版无法使用AI聊天功能，请设置DeepSeek API Key或连接服务器。"});
  });
}
// 覆盖 chat 相关函数
if (typeof sendMessage === 'function') {
  window._origSend = sendMessage;
}
</script>
'''

# 在 </body> 前插入
body_idx2 = html_new.rfind('</body>')
if body_idx2 != -1:
    html_new = html_new[:body_idx2] + chat_offline + html_new[body_idx2:]

# 验证
api_count = html_new.count('/api/')
print(f"替换后 /api/ 次数: {api_count}")
print(f"新文件大小: {len(html_new)/1024:.1f} KB")

# 写入文件
output = os.path.join(BASE, '鲁力立学术动态监控_独立版.html')
with open(output, 'w', encoding='utf-8') as f:
    f.write(html_new)
print(f"✅ 已写入: {output}")
print(f"   条目统计:")
for k in ['lulili','base','metaverse','yimu','related','honors']:
    d = all_data.get(k, {})
    if k == 'yimu':
        print(f"     {k}: results={len(d.get('results',[]))}, news={len(d.get('news',[]))}")
    else:
        print(f"     {k}: {d.get('total', len(d.get('results',[])))} 条")
