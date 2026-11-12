import json, os, urllib.request

RESULTS_DIR = '/Users/lulili/WorkBuddy/2026-06-02-20-17-02/news_monitor/results'
DESKTOP = '/Users/lulili/Desktop'

def load(fname):
    with open(os.path.join(RESULTS_DIR, fname), 'r', encoding='utf-8') as f:
        return json.load(f)

# 读取所有数据
print("=== 读取所有JSON数据 ===")
all_data = {}
for fname in ['lulili.json', 'base.json', 'metaverse.json', 'yimu.json', 'related.json', 'honors.json', 'profile.json']:
    d = load(fname)
    all_data[fname.replace('.json','')] = d
    if fname == 'yimu.json':
        print(f"  {fname}: results={len(d.get('results',[]))}, news={len(d.get('news',[]))}, stats有")
    else:
        print(f"  {fname}: total={d.get('total', '?')}, results={len(d.get('results',[]))}")

# 读取之前的独立版HTML模板
template_path = os.path.join(DESKTOP, '鲁力立学术动态监控_独立版.html')
with open(template_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 找到数据嵌入位置（在 </script> 之前，var SEARCH_TOPICS 之后）
# 策略：把 var ALL_DATA = ... 替换成最新数据

# 构建 ALL_DATA 对象（与 dashboard.html 中的格式一致）
all_data_js = "ALL_DATA = " + json.dumps(all_data, ensure_ascii=False, indent=2)

# 在HTML中找到 ALL_DATA = 的位置并替换
marker = 'ALL_DATA = '
idx = html.find(marker)
if idx == -1:
    print("❌ 未在模板中找到 ALL_DATA，尝试其他方法")
    # 尝试找 var ALL_DATA
    marker2 = 'var ALL_DATA'
    idx2 = html.find(marker2)
    if idx2 != -1:
        # 找到后面的 = 位置
        eq_idx = html.find('=', idx2)
        # 找到后面的 ; 位置
        semi_idx = html.find(';', eq_idx)
        # 替换从 eq_idx+1 到 semi_idx 的内容
        new_html = html[:eq_idx+1] + ' ' + all_data_js + ';' + html[semi_idx+1:]
        print(f"  ✅ 通过 var ALL_DATA 找到替换位置")
    else:
        print("❌ 无法定位数据位置")
        exit(1)
else:
    # 找到 ALL_DATA = 后面的 JSON 结束位置
    # 找到后面的 ;\n
    start = idx + len(marker)
    # 找到 JSON 数组/对象的结束位置
    # 简单方法：找到下一个 </script> 之前
    end_marker = ';\n'
    end_idx = html.find(end_marker, start)
    if end_idx == -1:
        end_idx = html.find(';</script>', start)
        if end_idx != -1:
            end_idx = end_idx + 1  # include the ;
    if end_idx == -1:
        print("❌ 无法找到数据结束位置")
        exit(1)
    new_html = html[:start] + all_data_js + html[end_idx:]
    print(f"  ✅ 替换了 ALL_DATA ({start}-{end_idx})")

# 同时更新 total 显示（在 h1 下方）
import re
# 更新右上角统计数字
total_all = sum(len(load(f).get('results', [])) for f in ['lulili.json', 'base.json', 'metaverse.json']) + \
            len(load('yimu.json').get('results', [])) + \
            len(load('honors.json').get('results', []))

print(f"\n=== 总条目数: {total_all} ===")

# 写回文件
output_path = os.path.join(DESKTOP, '鲁力立学术动态监控_独立版.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"✅ 已写入: {output_path}")
print(f"   文件大小: {len(new_html)/1024:.1f} KB")

# 验证：检查是否还有 /api/ 调用
api_count = new_html.count('/api/')
print(f"   ⚠️ 剩余 /api/ 调用: {api_count}")
if api_count > 0:
    print("     含有 /api/ 的行:")
    for i, line in enumerate(new_html.split('\n')):
        if '/api/' in line:
            print(f"      行{i+1}: {line.strip()[:80]}")
