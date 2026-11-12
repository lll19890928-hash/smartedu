# -*- coding: utf-8 -*-
"""2026-10-12 用户补充信息入库：3条新事件（公众号检索未收录，按用户提供信息入库）
1. 2026-10-10 盐城市"五级梯队"培养工程·教育家型教师培养工程（第二期）专题讲座
2. 2026-10     上海市三林中学 AI教育主题讲座
3. 2026-09-28  ICEMT 2026 中国澳门（第10届教育多媒体技术国际会议）线上论坛主席 + 论文报告
同步更新: lulili.json / related.json / profile.json 4.3 / _meta.json
"""
import json
import os
import shutil
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
STATIC = os.path.join(ROOT, 'static')
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load(name):
    with open(os.path.join(BASE, name), encoding='utf-8') as f:
        return json.load(f)


def save(name, data):
    with open(os.path.join(BASE, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def sort_results(data):
    data['results'].sort(key=lambda x: str(x.get('date', '')), reverse=True)


def add_event(data, event):
    for ev in data['results']:
        if ev['id'] == event['id']:
            print(f"  [跳过-已存在] {event['id']}")
            return False
    data['results'].append(event)
    sort_results(data)
    print(f"  [新增] {event['id']}: {event['title'][:45]}")
    return True


# ============ 1. lulili.json ============
print("== lulili.json ==")
ll = load('lulili.json')

ll_yancheng = {
    "id": "evt-ll-yancheng-oct2026",
    "date": "2026-10-10",
    "title": "鲁力立为盐城市\"五级梯队\"培养工程·教育家型教师培养工程（第二期）做专题讲座",
    "title_full": "2026年10月10日，鲁力立受邀为盐城市\"五级梯队\"培养工程中\"教育家型教师培养工程\"（第二期）培养对象做专题讲座，主题聚焦AI时代教学变革。",
    "summary": "2026年10月10日，鲁力立受邀为盐城市\"五级梯队\"培养工程中\"教育家型教师培养工程\"（第二期）做专题讲座，主题聚焦AI时代教学变革。盐城市\"五级梯队\"培养工程由盐城市教育局、盐城市教师发展学院组织实施，涵盖教育家型教师、卓越教师、领航教师、骨干教师、新秀教师五个递进层次，是盐城市教师队伍建设的品牌项目。",
    "category": "培训讲座",
    "sources": [
        {"name": "盐城市教育局/盐城市教师发展学院公开信息", "url": "https://ycedu.yancheng.gov.cn/art/2025/4/15/art_579_4313304.html", "date": "2026-10"},
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 2,
    "type": "event_cluster",
    "importance": "medium"
}

ll_sanlin = {
    "id": "evt-ll-sanlin-oct2026",
    "date": "2026-10-05",
    "title": "鲁力立在上海市三林中学开展AI教育主题讲座",
    "title_full": "2026年10月，鲁力立受邀在上海市三林中学开展AI教育主题讲座（具体日期待补充）。",
    "summary": "2026年10月（具体日期待补充），鲁力立受邀在上海市三林中学开展AI教育主题讲座。三林中学创建于1896年，前身为三林书院，是上海市浦东新区实验性示范性高中、上海市特色普通高中项目学校。",
    "category": "培训讲座",
    "sources": [
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

ll_icemt = {
    "id": "evt-ll-icemt2026-macau",
    "date": "2026-09-28",
    "title": "鲁力立参加ICEMT 2026澳门会议，担任线上论坛主席并做论文报告",
    "title_full": "2026年9月28日，鲁力立参加在中国澳门举办的第10届教育多媒体技术国际会议（ICEMT 2026），担任线上论坛主席并进行论文报告。",
    "summary": "第10届教育多媒体技术国际会议（ICEMT 2026）于2026年9月26-28日在中国澳门举办，由澳门城市大学主办，会议地点为澳门十六浦索菲特酒店，录用论文由ACM出版并收录ACM Digital Library，EI Compendex与Scopus检索。9月28日，鲁力立在会上担任线上论坛主席，并进行论文报告（论文题目待补充）。",
    "category": "学术会议",
    "sources": [
        {"name": "ICEMT 2026 官网", "url": "https://www.icemt.org/", "date": "2026-09"},
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 2,
    "type": "event_cluster",
    "importance": "medium"
}

added_ll = 0
for ev in [ll_yancheng, ll_sanlin, ll_icemt]:
    if add_event(ll, ev):
        added_ll += 1
ll['searched_at'] = NOW
save('lulili.json', ll)
print(f"  lulili.json results: {len(ll['results'])} 条 (本次新增 {added_ll} 条)")

# ============ 2. related.json ============
print("== related.json ==")
rel = load('related.json')

rel_yancheng = {
    "id": "rel-evt-yancheng-oct2026",
    "date": "2026-10-10",
    "title": "盐城市\"五级梯队\"培养工程·教育家型教师培养工程（第二期）研修活动邀请鲁力立做专题讲座",
    "title_full": "2026年10月10日，盐城市\"五级梯队\"培养工程中\"教育家型教师培养工程\"（第二期）研修活动邀请鲁力立做专题讲座。",
    "summary": "2026年10月10日，鲁力立受邀为盐城市\"五级梯队\"培养工程中\"教育家型教师培养工程\"（第二期）做专题讲座，主题聚焦AI时代教学变革。该工程由盐城市教育局、盐城市教师发展学院组织实施，是盐城市教师队伍建设的品牌项目，包含教育家型教师、卓越教师、领航教师、骨干教师、新秀教师五个层次。",
    "category": "培训讲座",
    "sources": [
        {"name": "盐城市教育局/盐城市教师发展学院公开信息", "url": "https://ycedu.yancheng.gov.cn/art/2025/4/15/art_579_4313304.html", "date": "2026-10"},
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 2,
    "type": "event_cluster",
    "importance": "medium"
}

rel_sanlin = {
    "id": "rel-evt-sanlin-oct2026",
    "date": "2026-10-05",
    "title": "上海市三林中学开展AI教育主题讲座，鲁力立主讲",
    "title_full": "2026年10月，上海市三林中学邀请鲁力立开展AI教育主题讲座（具体日期待补充）。",
    "summary": "2026年10月（具体日期待补充），鲁力立受邀在上海市三林中学开展AI教育主题讲座。三林中学创建于1896年，前身为三林书院，是上海市浦东新区实验性示范性高中、上海市特色普通高中项目学校，校训\"勤敬诚肃\"。",
    "category": "培训讲座",
    "sources": [
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

rel_icemt = {
    "id": "rel-evt-icemt2026-macau",
    "date": "2026-09-28",
    "title": "ICEMT 2026第10届教育多媒体技术国际会议在中国澳门举行，鲁力立担任线上论坛主席并做论文报告",
    "title_full": "2026年9月26-28日，第10届教育多媒体技术国际会议（ICEMT 2026）在中国澳门举行，9月28日鲁力立担任线上论坛主席并进行论文报告。",
    "summary": "第10届教育多媒体技术国际会议（ICEMT 2026）于2026年9月26-28日在中国澳门举办，由澳门城市大学主办，会议地点为澳门十六浦索菲特酒店，录用论文由ACM出版并收录ACM Digital Library，EI Compendex与Scopus检索。华东师范大学鲁力立于9月28日担任线上论坛主席，并进行论文报告（题目待补充）。",
    "category": "学术会议",
    "sources": [
        {"name": "ICEMT 2026 官网", "url": "https://www.icemt.org/", "date": "2026-09"},
        {"name": "用户提供", "url": "", "date": "2026-10"}
    ],
    "source_count": 2,
    "type": "event_cluster",
    "importance": "medium"
}

added_rel = 0
for ev in [rel_yancheng, rel_sanlin, rel_icemt]:
    if add_event(rel, ev):
        added_rel += 1
rel['searched_at'] = NOW
save('related.json', rel)
print(f"  related.json results: {len(rel['results'])} 条 (本次新增 {added_rel} 条)")

# ============ 3. profile.json 4.3 社会培训与讲座 ============
print("== profile.json 4.3 ==")
prof = load('profile.json')
sec43 = None
for sec in prof.get('sections', []):
    for sub in sec.get('subsections', []) if isinstance(sec.get('subsections'), list) else []:
        if sub.get('title', '').startswith('4.3'):
            sec43 = sub
    if sec.get('title', '').startswith('4.3'):
        sec43 = sec
if sec43 is None:
    # 顶层结构兜底：递归查找
    def find43(obj):
        if isinstance(obj, dict):
            if str(obj.get('title', '')).startswith('4.3'):
                return obj
            for v in obj.values():
                r = find43(v)
                if r is not None:
                    return r
        elif isinstance(obj, list):
            for v in obj:
                r = find43(v)
                if r is not None:
                    return r
        return None
    sec43 = find43(prof)

assert sec43 is not None, "未找到 4.3 社会培训与讲座 小节"
last_no = int(sec43['rows'][-1][0])
print(f"  当前最后序号: {last_no}, 共 {len(sec43['rows'])} 行")

new_rows = [
    [str(last_no + 1), "2026年10月10日", "盐城市\"五级梯队\"培养工程·教育家型教师培养工程（第二期）",
     "为培养对象做专题讲座，主题聚焦AI时代教学变革"],
    [str(last_no + 2), "2026年10月", "上海市三林中学",
     "开展AI教育主题讲座（具体日期待补充）"],
    [str(last_no + 3), "2026年9月28日", "中国澳门·ICEMT 2026（第10届教育多媒体技术国际会议，澳门城市大学主办）",
     "担任线上论坛主席并进行论文报告（题目待补充）；会议于9月26-28日举行 [详情](https://www.icemt.org/)"],
]
sec43['rows'] = new_rows + sec43['rows']  # 最新在前（与序号1为2026年9月13日的排列一致）
print(f"  4.3 新增 {len(new_rows)} 行（序号 {last_no + 1}-{last_no + 3}），现共 {len(sec43['rows'])} 行")
save('profile.json', prof)

# ============ 4. _meta.json 重建 ============
print("== _meta.json ==")
meta = {
    "updated_at": NOW,
    "total_events": 0,
    "sources": [],
    "profile_sections": 5
}
for fname in ['lulili.json', 'metaverse.json', 'base.json', 'yimu.json', 'related.json', 'honors.json']:
    fdata = load(fname)
    count = len(fdata.get('results', []))
    meta['total_events'] += count
    meta['sources'].append({
        "file": fname,
        "topic": fdata['topic']['name'],
        "event_count": count
    })
save('_meta.json', meta)
print(f"  总事件数: {meta['total_events']}")

# ============ 5. 双份同步 results/ -> static/ ============
print("== 同步 static/ ==")
for fname in ['lulili.json', 'related.json', 'profile.json', '_meta.json']:
    shutil.copy2(os.path.join(BASE, fname), os.path.join(STATIC, fname))
    print(f"  已同步 {fname}")

# ============ 6. 校验 ============
print("== JSON 校验 ==")
for fname in ['lulili.json', 'related.json', 'profile.json', '_meta.json']:
    for d in [BASE, STATIC]:
        p = os.path.join(d, fname)
        with open(p, encoding='utf-8') as f:
            json.load(f)
    print(f"  OK {fname} (results/ 与 static/ 均为有效JSON)")

print("\n全部更新完成!")
