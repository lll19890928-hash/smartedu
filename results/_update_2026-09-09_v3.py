# -*- coding: utf-8 -*-
"""2026-09-09 第三轮数据补全：修正/新增5类事件（用户补充信息）
1. 西安培训地点细化：大南小学 + 宏景小学
2. 北虹高级中学：为期4次的系列培训（7月1场 + 8月下旬3场）
3. 网络安全培训：上海市教育系统网络安全培训（约8月20日前后）
4. 教育智能体研修班：鲁力立参与讲课（不只带队研学）
5. 新增：华师大艺术教育部艺术疗愈师研修班（7月6-9日在智慧教育产教基地）
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(BASE, name), encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(BASE, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def sort_results(data):
    data['results'].sort(key=lambda x: str(x.get('date', '')), reverse=True)

def update_event(data, eid, **fields):
    for ev in data['results']:
        if ev['id'] == eid:
            for k, v in fields.items():
                ev[k] = v
            print(f"  [更新] {eid}: {fields.get('title', '')[:40]}")
            return True
    print(f"  [!!未找到] {eid}")
    return False

def add_event(data, event):
    for ev in data['results']:
        if ev['id'] == event['id']:
            print(f"  [跳过-已存在] {event['id']}")
            return False
    data['results'].append(event)
    sort_results(data)
    print(f"  [新增] {event['id']}: {event['title'][:40]}")
    return True

# ============ 1. lulili.json ============
print("== lulili.json ==")
ll = load('lulili.json')
update_event(ll, 'evt-ll-xian-aug2026',
    title="鲁力立在西安市大南小学、宏景小学开展AI教育主题培训",
    title_full="2026年8月底，鲁力立受邀在西安市大南小学、宏景小学开展为期一天的AI教育主题培训。",
    summary="2026年8月底，鲁力立受邀前往西安，为西安市大南小学、宏景小学开展为期一天的AI教育主题培训，面向两校教师。这是鲁力立2026年暑假期间在外地开展的培训活动之一。")
update_event(ll, 'evt-ll-security-aug2026',
    title_full="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训活动在华东师范大学智慧教育产教基地举办，鲁力立参加。",
    summary="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训活动在华东师范大学智慧教育产教基地举办，鲁力立参加该培训。")
update_event(ll, 'evt-ll-beihong-aug2026',
    title="鲁力立在上海音乐学院虹口区北虹高级中学开展AI教育系列讲座（8月三场）",
    title_full="2026年8月下旬，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展AI教育系列讲座（三场），与7月的一场共同构成本次为期四次的系列培训。",
    summary="2026年8月下旬，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展AI教育系列讲座（三场）。北虹高中2026年暑假共开展为期四次的AI教育系列培训（7月一场、8月下旬三场），均由鲁力立主讲，面向该校教师。")
update_event(ll, 'evt-ll-beihong-jul2026',
    title_full="2026年7月，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展为期一天的AI教育主题讲座（系列第一场），面向该校教师。",
    summary="2026年7月，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展AI教育主题讲座（系列第一场）。北虹高中是虹口区重点中学，2024年更名为上海音乐学院虹口区北虹高级中学。该校2026年暑假共安排为期四次的AI教育系列培训，此为第一场。")
update_event(ll, 'evt-ll-agent-training2026',
    title_full="2026年8月19-21日，鲁力立在华东师范大学'教育智能体开发与应用高级研修班'中参与授课，并负责带领学员走进智慧教育产教基地开展实地研学。",
    summary="2026年8月19-21日，华东师范大学教育信息技术学系主办'教育智能体开发与应用高级研修班'。鲁力立作为基地负责人参与研修班授课，并带领学员走进智慧教育产教基地，体验已落地的教育智能体产品，剖析产品设计逻辑，将产业实践经验反哺学员的个人方案设计。")
sort_results(ll)
save('lulili.json', ll)

# ============ 2. base.json ============
print("== base.json ==")
base = load('base.json')
update_event(base, 'evt-base-security-aug2026',
    title_full="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训活动在华东师范大学智慧教育产教基地举办，鲁力立参加该活动。",
    summary="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训活动在华东师范大学智慧教育产教基地举办。鲁力立作为基地负责人参加了该培训活动。")
update_event(base, 'evt-base-agent-training2026',
    title_full="2026年8月19日至21日，华东师范大学教育信息技术学系主办'教育智能体开发与应用高级研修班'。鲁力立老师参与授课，并带领学员走进智慧教育产教基地开展实地研学，将产业端真实实践经验反哺到个人方案设计中。",
    summary="2026年8月19-21日，华东师大教育信息技术学系主办'教育智能体开发与应用高级研修班'。研修将智慧教育产教基地实地研学纳入课程闭环，鲁力立参与授课并带领学员体验已落地的先进教育智能体产品，在企业导师讲解下剖析产品设计逻辑与应用思路，实现课堂理论学习与产业实践体验的有机结合。")
art_base = {
    "id": "evt-base-arttherapy-jul2026",
    "date": "2026-07-08",
    "title": "华东师大艺术教育部艺术疗愈师研修班（第二期）在智慧教育产教基地开班",
    "title_full": "2026年7月6-9日，华东师范大学教育学部艺术教育部主办的第二期艺术疗愈师研修班在华东师范大学智慧教育产教基地集中授课，7月10/12/13日开展场景实训。",
    "summary": "2026年7月6-9日，华东师大教育学部艺术教育部在智慧教育产教基地举办第二期艺术疗愈师研修班，面向艺术教育、心理、康养等行业从业者，采用'理论赋能+场景实训'双轨模式，课程涵盖音乐疗愈、美术疗愈、舞动与戏剧疗育等方向。基地的智慧美育工坊、未来课堂等空间为课程提供了沉浸式教学场景。",
    "category": "培训活动",
    "sources": [
        {
            "name": "华东师大艺术疗愈师研修班招生公告（公众号/官网）",
            "url": "https://zsjy.ecnu.edu.cn/2026nfxljyxmgs/list5.htm",
            "date": "2026-06"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}
add_event(base, art_base)
save('base.json', base)

# ============ 3. related.json ============
print("== related.json ==")
rel = load('related.json')
update_event(rel, 'rel-evt-xian-aug2026',
    title="鲁力立2026年8月底赴西安大南小学、宏景小学开展AI教育培训",
    title_full="2026年8月底，鲁力立受邀在西安市大南小学、宏景小学开展为期一天的AI教育主题培训。",
    summary="2026年8月底，鲁力立前往西安，为西安市大南小学、宏景小学开展AI教育主题培训，为期一天，面向两校教师。")
update_event(rel, 'rel-evt-security-aug2026',
    title_full="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训在华东师范大学智慧教育产教基地举办。",
    summary="2026年8月下旬（约8月20日前后），上海市教育系统网络安全培训在华东师范大学智慧教育产教基地举办，鲁力立参加。")
update_event(rel, 'rel-evt-beihong-2026',
    title_full="2026年暑假期间，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展AI教育主题讲座，共4场（7月一场、8月下旬三场）。",
    summary="2026年暑假，鲁力立在上海音乐学院虹口区北虹高级中学开展系列AI教育讲座，共4场（7月一场、8月下旬三场）。该校是虹口区重点中学，2024年更名为上海音乐学院虹口区北虹高级中学。")
update_event(rel, 'rel-evt-agent-training2026',
    summary="2026年8月19-21日，华东师大教育信息技术学系主办'教育智能体开发与应用高级研修班'，面向全国中小学、职业院校、高校教师及教育管理者。鲁力立参与授课，并将智慧教育产教基地实地研学纳入课程闭环。")
art_rel = {
    "id": "rel-evt-arttherapy-jul2026",
    "date": "2026-07-08",
    "title": "华东师大艺术教育部第二期艺术疗愈师研修班在智慧教育产教基地举办",
    "title_full": "2026年7月6-9日，华东师范大学教育学部艺术教育部主办的第二期艺术疗愈师研修班在智慧教育产教基地集中授课。",
    "summary": "2026年7月6-9日，华东师大教育学部艺术教育部在智慧教育产教基地举办第二期艺术疗愈师研修班（2025年首期在普陀校区举办），采用'理论赋能+场景实训'双轨模式，华东师大艺术教育部主任董放、副教授徐韵等专家联合授课，合作单位为华和国颐（上海）健康服务有限公司。",
    "category": "培训活动",
    "sources": [
        {
            "name": "华东师大艺术疗愈师研修班招生公告（公众号/官网）",
            "url": "https://zsjy.ecnu.edu.cn/2026nfxljyxmgs/list5.htm",
            "date": "2026-06"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}
add_event(rel, art_rel)
save('related.json', rel)

print("\n全部完成")
