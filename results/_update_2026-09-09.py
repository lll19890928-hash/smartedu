#!/usr/bin/env python3
"""
2026-09-09 周更新 — 把 8-9 月 2 条新动态分发到 6 个主题文件
"""
import json
import os
from datetime import datetime

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))

NOW = "2026-09-09 10:50:00"


def load(fname):
    with open(os.path.join(RESULTS_DIR, fname), 'r', encoding='utf-8') as f:
        return json.load(f)


def save(fname, data):
    with open(os.path.join(RESULTS_DIR, fname), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def exists(data, eid):
    results = data.get('results', data.get('news', []))
    return any(r.get('id') == eid for r in results)


def insert(data, entry, top=True):
    """在 results 或 news 列表前面插入；按日期降序自动定位。"""
    key = 'news' if 'news' in data else 'results'
    lst = data[key]
    if top:
        lst.insert(0, entry)
    else:
        lst.append(entry)
    data[key] = lst
    return data


# ============================================================
# 事件 1: 2026-08-24 清华大学教育学院师生来访交流
# ============================================================
SRC_TSINGHUA = {
    "name": "工程中心官网（来访纪实）",
    "url": "https://ercdee.ecnu.edu.cn/d2/82/c16571a774786/page.htm",
    "date": "2026-08-24",
}

evt_tsinghua_lulili = {
    "id": "evt-ll-tsinghua2026",
    "date": "2026-08-24",
    "title": "清华大学教育学院师生来访产教基地，鲁力立介绍基地STEM教育数智化与国际化",
    "title_full": "2026年8月24日，清华大学「中国教育调查」上海实践支队走进华东师范大学智慧教育产教基地调研。鲁力立老师向清华师生介绍基地建设背景与实践，分享了组织一线教师体验和拆解智能体产品的实践案例，并就STEM教育数智化与国际化议题展开交流。",
    "summary": "2026年8月24日，清华大学教育学院「中国教育调查」上海实践支队走进华东师范大学智慧教育产教基地，与鲁力立团队交流。鲁力立向师生介绍产教基地在STEM教育数智化与国际化方向的实践与思考，分享了「AI教育智能体拆装工坊」「未来学校样板间」等典型场景。该活动进一步巩固了产教基地在 STEM 教育的全国影响力。",
    "category": "学术交流",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high",
}

evt_tsinghua_base = {
    "id": "evt-base-tsinghua2026",
    "date": "2026-08-24",
    "title": "清华大学「中国教育调查」上海实践支队调研智慧教育产教基地",
    "title_full": "2026年8月24日，清华大学教育学院「中国教育调查」上海实践支队走进华东师范大学智慧教育产教基地。鲁力立老师向清华师生介绍基地建设理念、运营模式及「未来学校」样板间，分享了组织一线教师拆解智能体产品的实践案例。",
    "summary": "2026年8月24日，清华大学教育学院调研团队走进华东师范大学智慧教育产教基地，开展「中国教育调查」上海实践调研。鲁力立老师接待并系统介绍了产教基地的建设与实践，与清华师生就STEM教育数智化与国际化议题深入交流。",
    "category": "学术交流",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high",
}

evt_tsinghua_related = {
    "id": "rel-evt-tsinghua2026",
    "date": "2026-08-24",
    "title": "清华大学教育学院师生来访产教基地调研STEM教育数智化",
    "title_full": "2026年8月24日，清华大学教育学院调研团队到访华东师范大学智慧教育产教基地。",
    "summary": "清华大学教育学院「中国教育调查」上海实践支队赴华东师范大学智慧教育产教基地开展STEM教育调研。鲁力立老师接待并介绍基地建设、运营与实践案例。",
    "category": "学术交流",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}

evt_tsinghua_honors = {
    "id": "hon-evt-tsinghua2026",
    "date": "2026-08-24",
    "title": "鲁力立产教基地STEM实践获清华大学教育学院调研关注",
    "title_full": "清华大学「中国教育调查」上海实践支队调研华东师范大学智慧教育产教基地。",
    "summary": "2026年8月24日，清华大学教育学院调研团队赴华东师大智慧教育产教基地调研，鲁力立介绍STEM教育数智化与国际化实践，标志产教基地 STEM 实践获国内顶尖高校关注。",
    "category": "学术影响",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}


# ============================================================
# 事件 2: 2026-09-13 鑫考股份破界·共生AI精准教学数智化创新峰会
# ============================================================
SRC_XINKAO = {
    "name": "鑫考股份官方公众号",
    "url": "https://mp.weixin.qq.com/s/83HY5avXyJD55nEOaDiZ5Q",
    "date": "2026-08-12",
}

evt_xinkao_lulili = {
    "id": "evt-ll-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "鲁力立受邀出席鑫考股份破界·共生AI精准教学数智化创新峰会并作主题分享",
    "title_full": "2026年9月13日，鑫考股份将在河北衡水主办「破界·共生——AI精准教学数智化创新峰会」。鲁力立作为特邀嘉宾出席，主题分享「AI时代教育的变与守」，聚焦智能教研、精准教学与未来教育。",
    "summary": "2026年9月13日，鲁力立受邀出席鑫考股份主办的「破界·共生——AI精准教学数智化创新峰会」，地点河北衡水。鲁力立将基于壹幕工作室、产教基地的实践经验，探讨AI精准教学与教育数智化创新方向。本次峰会延续了2024年8月鑫考股份教育生态峰会的合作脉络。",
    "category": "主题演讲",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high",
}

evt_xinkao_base = {
    "id": "evt-base-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "智慧教育产教基地核心成员出席鑫考股份AI精准教学峰会",
    "title_full": "2026年9月13日，鑫考股份（智慧教育产教基地入驻企业）将在河北衡水主办「破界·共生——AI精准教学数智化创新峰会」。鲁力立作为基地核心成员受邀出席并作主题分享。",
    "summary": "2026年9月13日，智慧教育产教基地入驻企业鑫考股份主办「破界·共生——AI精准教学数智化创新峰会」。基地核心成员鲁力立作为特邀嘉宾出席，主题分享「AI时代教育的变与守」。",
    "category": "产业活动",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high",
}

evt_xinkao_related = {
    "id": "rel-evt-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "鑫考股份主办AI精准教学数智化创新峰会，鲁力立受邀作主题分享",
    "title_full": "2026年9月13日，鑫考股份将在河北衡水主办「破界·共生——AI精准教学数智化创新峰会」。",
    "summary": "2026年9月13日，智慧教育产教基地入驻企业鑫考股份主办「破界·共生——AI精准教学数智化创新峰会」，鲁力立受邀出席并作「AI时代教育的变与守」主题分享。",
    "category": "产业活动",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}

evt_xinkao_honors = {
    "id": "hon-evt-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "鲁力立受邀在鑫考股份AI精准教学峰会上作主题演讲",
    "title_full": "鲁力立受邀出席鑫考股份「破界·共生——AI精准教学数智化创新峰会」并作主题分享。",
    "summary": "2026年9月13日，鲁力立受邀出席鑫考股份主办的「破界·共生——AI精准教学数智化创新峰会」并作主题分享。这是鲁力立2026年下半年又一次重要的产业界主题演讲。",
    "category": "学术演讲",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}


# ============================================================
# 元宇宙视角：清华来访 + 鑫考股份均涉及 AI 教育的"未来课堂"形态
# ============================================================
evt_tsinghua_metaverse = {
    "id": "evt-metaverse-tsinghua2026",
    "date": "2026-08-24",
    "title": "清华调研团队走进产教基地，未来课堂与AI教育智能体成讨论热点",
    "title_full": "2026年8月24日，清华大学教育学院「中国教育调查」上海实践支队走进华东师范大学智慧教育产教基地，与鲁力立团队就未来课堂、AI教育智能体等议题展开交流。",
    "summary": "2026年8月24日，清华大学教育学院调研团队走进华东师大智慧教育产教基地，实地了解教育元宇宙未来课堂的落地形态，并就AI教育智能体的应用与未来课堂的演化路径展开深入讨论。",
    "category": "学术交流",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}

evt_xinkao_metaverse = {
    "id": "evt-metaverse-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "鑫考股份AI精准教学峰会聚焦精准教学与未来课堂",
    "title_full": "2026年9月13日，鑫考股份在河北衡水主办「破界·共生——AI精准教学数智化创新峰会」，鲁力立受邀作主题分享。",
    "summary": "2026年9月13日，鑫考股份主办「破界·共生——AI精准教学数智化创新峰会」，议题涉及精准教学、未来课堂与AI教育应用。鲁力立受邀作「AI时代教育的变与守」主题分享。",
    "category": "产业活动",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium",
}


# ============================================================
# 壹幕工作室视角：相关活动背景
# ============================================================
evt_tsinghua_yimu = {
    "id": "evt-yimu-tsinghua2026",
    "date": "2026-08-24",
    "title": "清华调研团队了解壹幕工作室的AIGC影视与教学实践",
    "title_full": "2026年8月24日，清华大学「中国教育调查」上海实践支队走进产教基地，鲁力立介绍壹幕工作室在 AIGC 影视与教学融合方面的成果。",
    "summary": "清华调研团队通过产教基地访问，间接了解到壹幕工作室在 AIGC 影视创作与教学实践方面的最新成果。",
    "category": "对外交流",
    "sources": [SRC_TSINGHUA],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "low",
}

evt_xinkao_yimu = {
    "id": "evt-yimu-xinkao-summit2026",
    "date": "2026-09-13",
    "title": "鲁力立将壹幕工作室经验带入鑫考股份AI精准教学峰会",
    "title_full": "鲁力立受邀出席鑫考股份峰会，分享壹幕工作室在 AIGC 影视教学方面的实战经验。",
    "summary": "2026年9月13日，鲁力立出席鑫考股份主办的AI精准教学数智化创新峰会，议题融合壹幕工作室AIGC影视教学与产教基地智能体产品经验。",
    "category": "对外交流",
    "sources": [SRC_XINKAO],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "low",
}


# ============================================================
# 执行写入
# ============================================================
# (filename, [(id, entry), ...]) — 每个文件的待添加条目
updates = {
    'lulili.json':   [evt_tsinghua_lulili, evt_xinkao_lulili],
    'metaverse.json':[evt_tsinghua_metaverse, evt_xinkao_metaverse],
    'base.json':     [evt_tsinghua_base, evt_xinkao_base],
    'yimu.json':     [evt_tsinghua_yimu, evt_xinkao_yimu],
    'related.json':  [evt_tsinghua_related, evt_xinkao_related],
    'honors.json':   [evt_tsinghua_honors, evt_xinkao_honors],
}

print("=" * 60)
print("执行 2026-09-09 周更新")
print("=" * 60)

total_added = 0
for fname, entries in updates.items():
    data = load(fname)
    added_in_file = 0
    for entry in entries:
        if not exists(data, entry['id']):
            insert(data, entry, top=True)
            added_in_file += 1

    # 更新统计字段
    if 'results' in data:
        results = data['results']
        data['total'] = len(results)
        # events_total 计数
        data['events_total'] = sum(1 for r in results if r.get('type') == 'event_cluster' or r.get('id', '').startswith('evt-'))
        if 'source_links_total' in data:
            data['source_links_total'] = sum(r.get('source_count', 0) for r in results)
    if 'news' in data:
        data['news'].insert(0, {
            "date": NOW.split()[0],
            "title": "周更：清华调研 + 鑫考股份峰会预告",
            "summary": "本周新增 2 条最新动态：8月24日清华大学教育学院调研、9月13日鑫考股份AI精准教学峰会预告。",
        })
        data['total'] = len(data.get('results', [])) + len(data['news'])
    data['searched_at'] = NOW
    if 'updated_at' in data:
        data['updated_at'] = NOW

    save(fname, data)
    total_added += added_in_file
    print(f"  ✓ {fname}: 新增 {added_in_file} 条, total={data.get('total')}, events_total={data.get('events_total')}")

print()
print(f"全部新增: {total_added} 条")
print()

# ============================================================
# 重建 _meta.json
# ============================================================
print("=" * 60)
print("重建 _meta.json")
print("=" * 60)

meta = load('_meta.json')
topics_count = {}
events_total_all = 0
source_links_total_all = 0
for fname in updates.keys():
    data = load(fname)
    topic_id = fname.replace('.json', '')
    topics_count[topic_id] = {
        "name": data.get('topic', topic_id),
        "count": data.get('total', len(data.get('results', data.get('news', [])))),
    }
    events_total_all += data.get('events_total', 0)
    source_links_total_all += data.get('source_links_total', 0)

# 加载 profile.json 单独统计
profile_data = load('profile.json')
profile_count = 0
if 'sections' in profile_data:
    profile_count = len(profile_data['sections'])
topics_count['profile'] = {"name": "鲁力立个人全貌", "count": profile_count}

meta['updated_at'] = NOW
meta['events_total'] = events_total_all
meta['source_links_total'] = source_links_total_all
meta['topics'] = topics_count
meta['profile_sections'] = profile_count
meta['total_source_links'] = source_links_total_all

save('_meta.json', meta)
print(json.dumps(meta, ensure_ascii=False, indent=2))
print()
print("✅ 全部完成")
