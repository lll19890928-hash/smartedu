import json, os
from datetime import datetime

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
def load(fname):
    fpath = os.path.join(RESULTS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(fname, data):
    fpath = os.path.join(RESULTS_DIR, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  已保存 {fname}")

# 读取所有文件
lulili = load('lulili.json')
base = load('base.json')
metaverse = load('metaverse.json')
related = load('related.json')
honors = load('honors.json')

# ===== 第一步：从 lulili.json 分离条目 =====
results = lulili.get('results', [])
stay_lulili = []
add_to_base = []
add_to_metaverse = []
add_to_yimu_news = []  # 壹幕动态，加到 yimu.json 的 news 区
add_to_related = []

for r in results:
    title = r.get('title', '')
    summary = r.get('summary', '')
    title_full = r.get('title_full', '')
    combined = title + summary + title_full
    cat = r.get('category', '')
    has_lulili = '鲁力立' in combined
    
    if has_lulili:
        stay_lulili.append(r)
    else:
        # 不含鲁力立名字
        if '基地' in title or '产教基地' in title or cat == '基地建设':
            add_to_base.append(r)
        elif '元宇宙' in title or '未来课堂' in title or '未来学习' in title or 'CAVE' in title or 'MR' in title or '全息' in title:
            add_to_metaverse.append(r)
        elif '壹幕' in title or 'EMOVIE' in title or 'EMOVIE' in title or cat == '壹幕工作室':
            add_to_yimu_news.append(r)
        else:
            add_to_related.append(r)

print(f"=== 分离结果 ===")
print(f"  留在 lulili: {len(stay_lulili)} 条")
print(f"  移到 base: {len(add_to_base)} 条")
print(f"  移到 metaverse: {len(add_to_metaverse)} 条")
print(f"  移到 yimu_news: {len(add_to_yimu_news)} 条")
print(f"  移到 related: {len(add_to_related)} 条")

# ===== 第二步：更新 lulili.json =====
lulili['results'] = stay_lulili
lulili['total'] = len(stay_lulili)
save('lulili.json', lulili)

# ===== 第三步：更新 base.json =====
base_results = base.get('results', [])
# 去重：检查 id 是否已存在
existing_ids = {r.get('id','') for r in base_results}
for r in add_to_base:
    if r.get('id','') not in existing_ids:
        base_results.append(r)
        existing_ids.add(r.get('id',''))
base['results'] = base_results
base['total'] = len(base_results)
save('base.json', base)

# ===== 第四步：更新 metaverse.json =====
meta_results = metaverse.get('results', [])
existing_ids = {r.get('id','') for r in meta_results}
for r in add_to_metaverse:
    if r.get('id','') not in existing_ids:
        meta_results.append(r)
        existing_ids.add(r.get('id',''))
metaverse['results'] = meta_results
metaverse['total'] = len(meta_results)
save('metaverse.json', metaverse)

# ===== 第五步：更新 related.json =====
rel_results = related.get('results', [])
existing_ids = {r.get('id','') for r in rel_results}
for r in add_to_related:
    if r.get('id','') not in existing_ids:
        rel_results.append(r)
        existing_ids.add(r.get('id',''))
related['results'] = rel_results
related['total'] = len(rel_results)
save('related.json', related)

# ===== 第六步：在 yimu.json 中添加 news 区块 =====
yimu = load('yimu.json')
if 'news' not in yimu:
    yimu['news'] = []
existing_titles = {n.get('title','') for n in yimu.get('news', [])}
for r in add_to_yimu_news:
    if r.get('title','') not in existing_titles:
        # 转换为 yimu news 格式
        news_item = {
            'date': r.get('date', ''),
            'title': r.get('title', ''),
            'summary': r.get('summary', ''),
            'category': r.get('category', '壹幕动态'),
            'sources': r.get('sources', [])
        }
        yimu['news'].append(news_item)
        existing_titles.add(r.get('title',''))
save('yimu.json', yimu)

print()
print("=== 更新后各文件条目数 ===")
for fname in ['lulili.json', 'base.json', 'metaverse.json', 'related.json', 'yimu.json']:
    d = load(fname)
    if fname == 'yimu.json':
        n_results = len(d.get('results', []))
        n_news = len(d.get('news', []))
        print(f"  {fname}: 学生成果 {n_results} 条, 动态 {n_news} 条")
    else:
        n = len(d.get('results', []))
        t = d.get('total', n)
        print(f"  {fname}: {n} 条 (total={t})")
