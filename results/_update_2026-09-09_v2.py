#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新脚本 v2: 整合清沐泽元数据要素大赛获奖、教育智能体研修班、
北虹高中讲座、西安小学讲座、网络安全培训等事件到各主题文件
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(filename):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  已保存: {filename}")

def add_event(data, event):
    """添加事件到results列表，按日期降序排列"""
    # 检查是否已存在相同id
    for existing in data['results']:
        if existing.get('id') == event['id']:
            print(f"  跳过重复: {event['id']}")
            return False
    data['results'].append(event)
    # 按日期降序排序
    data['results'].sort(key=lambda x: x.get('date', ''), reverse=True)
    return True

# ========== 定义新事件 ==========

# 1. 清沐泽元 数据要素大赛三等奖
evt_qingmu_honors = {
    "id": "hon-evt-qingmu-data2026",
    "date": "2026-08-20",
    "title": "清沐泽元「美术教育大数据精准教学平台」获2026年数据要素×大赛上海分赛三等奖",
    "title_full": "2026年8月20日，2026年'数据要素×'大赛上海分赛拟获奖项目名单公示，上海清沐泽元教育科技有限公司的'美术教育大数据精准教学平台'项目获开放性创新赛道三等奖。",
    "summary": "2026年'数据要素×'大赛上海分赛决赛于8月18日完成评审。上海清沐泽元教育科技有限公司（鲁力立持股30%）参赛项目'美术教育大数据精准教学平台'在开放性创新赛道中脱颖而出，荣获三等奖。该赛事由国家数据局主办，上海分赛由上海市数据局组织。",
    "category": "荣誉奖项",
    "sources": [
        {
            "name": "上海市数据局官网-获奖公示",
            "url": "https://dexc.sh.gov.cn/ssgg/rwgs/20260820/ac407b660186482f8f62d7b705f92905.html",
            "date": "2026-08-20"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high"
}

evt_qingmu_lulili = {
    "id": "evt-ll-qingmu-data2026",
    "date": "2026-08-20",
    "title": "鲁力立关联公司清沐泽元获数据要素×大赛上海分赛三等奖",
    "title_full": "鲁力立持股30%的上海清沐泽元教育科技有限公司在2026年'数据要素×'大赛上海分赛中获开放性创新赛道三等奖。",
    "summary": "2026年8月，鲁力立关联企业上海清沐泽元教育科技有限公司的'美术教育大数据精准教学平台'项目荣获2026年'数据要素×'大赛上海分赛开放性创新赛道三等奖。该公司由鲁力立持股30%，上海花狮信息科技持股70%，成立于2025年8月。",
    "category": "荣誉奖项",
    "sources": [
        {
            "name": "上海市数据局官网-获奖公示",
            "url": "https://dexc.sh.gov.cn/ssgg/rwgs/20260820/ac407b660186482f8f62d7b705f92905.html",
            "date": "2026-08-20"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high"
}

evt_qingmu_related = {
    "id": "rel-evt-qingmu-data2026",
    "date": "2026-08-20",
    "title": "清沐泽元获2026年数据要素×大赛上海分赛开放性创新赛道三等奖",
    "title_full": "上海清沐泽元教育科技有限公司的'美术教育大数据精准教学平台'获2026年'数据要素×'大赛上海分赛三等奖。",
    "summary": "2026年8月18日决赛评审结束后，上海清沐泽元教育科技有限公司的'美术教育大数据精准教学平台'项目在开放性创新赛道获得三等奖。该赛事由国家数据局主办。",
    "category": "荣誉奖项",
    "sources": [
        {
            "name": "上海市数据局官网",
            "url": "https://dexc.sh.gov.cn/ssgg/rwgs/20260820/ac407b660186482f8f62d7b705f92905.html",
            "date": "2026-08-20"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

# 2. 教育智能体开发与应用高级研修班 (2026-08-19至21)
evt_agent_base = {
    "id": "evt-base-agent-training2026",
    "date": "2026-08-21",
    "title": "教育智能体开发与应用高级研修班在华东师范大学圆满结业，学员实地研学智慧教育产教基地",
    "title_full": "2026年8月19日至21日，华东师范大学教育信息技术学系主办'教育智能体开发与应用高级研修班'。鲁力立老师带领学员走进智慧教育产教基地开展实地研学，将产业端真实实践经验反哺到个人方案设计中。",
    "summary": "2026年8月19-21日，华东师大教育信息技术学系主办'教育智能体开发与应用高级研修班'。研修将智慧教育产教基地实地研学纳入课程闭环，鲁力立带领学员体验已落地的先进教育智能体产品，在企业导师讲解下剖析产品设计逻辑与应用思路，实现课堂理论学习与产业实践体验的有机结合。",
    "category": "培训活动",
    "sources": [
        {
            "name": "工程中心官网-研修班结业报道",
            "url": "https://ercdee.ecnu.edu.cn/d2/7d/c16571a774781/page.htm",
            "date": "2026-09-02"
        },
        {
            "name": "工程中心官网-研修班招募",
            "url": "https://ercdee.ecnu.edu.cn/b6/c7/c16571a767687/page.htm",
            "date": "2026-08"
        }
    ],
    "source_count": 2,
    "type": "event_cluster",
    "importance": "high"
}

evt_agent_lulili = {
    "id": "evt-ll-agent-training2026",
    "date": "2026-08-21",
    "title": "鲁力立带领教育智能体研修班学员实地研学智慧教育产教基地",
    "title_full": "2026年8月19-21日，鲁力立在华东师范大学'教育智能体开发与应用高级研修班'中负责带领学员走进智慧教育产教基地开展实地研学。",
    "summary": "2026年8月19-21日，华东师范大学教育信息技术学系主办'教育智能体开发与应用高级研修班'。鲁力立作为基地负责人，带领研修班学员走进智慧教育产教基地，体验已落地的教育智能体产品，剖析产品设计逻辑，将产业实践经验反哺学员的个人方案设计。",
    "category": "培训活动",
    "sources": [
        {
            "name": "工程中心官网",
            "url": "https://ercdee.ecnu.edu.cn/d2/7d/c16571a774781/page.htm",
            "date": "2026-09-02"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "high"
}

evt_agent_metaverse = {
    "id": "evt-mv-agent-training2026",
    "date": "2026-08-21",
    "title": "华东师大教育智能体研修班结业，学员在智慧教育产教基地完成实地研学",
    "title_full": "2026年8月19-21日，华东师范大学'教育智能体开发与应用高级研修班'圆满结业。研修将智慧教育产教基地实地研学纳入课程闭环，学员在基地体验教育智能体产品。",
    "summary": "2026年8月19-21日，华东师大教育信息技术学系主办的'教育智能体开发与应用高级研修班'圆满结业。研修构建'产品开发+落地规划'全链条培养模式，并将智慧教育产教基地实地研学作为正式教学环节，学员在基地切身体验已落地的先进教育智能体产品。",
    "category": "培训活动",
    "sources": [
        {
            "name": "工程中心官网",
            "url": "https://ercdee.ecnu.edu.cn/d2/7d/c16571a774781/page.htm",
            "date": "2026-09-02"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_agent_related = {
    "id": "rel-evt-agent-training2026",
    "date": "2026-08-21",
    "title": "华东师范大学教育智能体开发与应用高级研修班（8月19-21日）",
    "title_full": "华东师范大学教育信息技术学系于2026年8月19-21日主办'教育智能体开发与应用高级研修班'，研修地点在华东师大，费用3000元/人。",
    "summary": "2026年8月19-21日，华东师大教育信息技术学系主办'教育智能体开发与应用高级研修班'，面向全国中小学、职业院校、高校教师及教育管理者。研修将智慧教育产教基地实地研学纳入课程闭环。",
    "category": "培训活动",
    "sources": [
        {
            "name": "工程中心官网",
            "url": "https://ercdee.ecnu.edu.cn/d2/7d/c16571a774781/page.htm",
            "date": "2026-09-02"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

# 3. 北虹高中讲座 (2026年7月及8月)
evt_beihong_lulili_jul = {
    "id": "evt-ll-beihong-jul2026",
    "date": "2026-07-15",
    "title": "鲁力立在上海音乐学院虹口区北虹高级中学开展AI教育讲座（暑期第一场）",
    "title_full": "2026年7月中旬，鲁力立受邀在上海音乐学院虹口区北虹高级中学（原北虹高级中学）开展为期一天的AI教育主题讲座，面向该校教师。",
    "summary": "2026年7月，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展AI教育主题讲座。北虹高中是虹口区重点中学，2024年更名为上海音乐学院虹口区北虹高级中学。此次讲座是鲁力立2026年暑假期间在北虹高中系列培训的第一场。",
    "category": "培训讲座",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-07"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_beihong_lulili_aug = {
    "id": "evt-ll-beihong-aug2026",
    "date": "2026-08-25",
    "title": "鲁力立在上海音乐学院虹口区北虹高级中学开展AI教育讲座（暑期第三场）",
    "title_full": "2026年8月下旬，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展为期两天的AI教育主题讲座，面向该校教师。",
    "summary": "2026年8月下旬，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展为期两天的AI教育主题讲座。这是鲁力立2026年暑假期间在北虹高中系列培训的第三场（7月一场，8月底两场）。",
    "category": "培训讲座",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_beihong_related = {
    "id": "rel-evt-beihong-2026",
    "date": "2026-08-25",
    "title": "鲁力立2026年暑假在上海音乐学院虹口区北虹高级中学开展系列AI教育讲座",
    "title_full": "2026年暑假期间，鲁力立受邀在上海音乐学院虹口区北虹高级中学开展多场AI教育主题讲座，共计约3-4场，覆盖7月和8月。",
    "summary": "2026年暑假，鲁力立在上海音乐学院虹口区北虹高级中学开展系列AI教育讲座。该校是虹口区重点中学，2024年更名为上海音乐学院虹口区北虹高级中学。系列讲座覆盖7月一场、8月底两场。",
    "category": "培训讲座",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

# 4. 西安小学讲座 (2026年8月底)
evt_xian_lulili = {
    "id": "evt-ll-xian-aug2026",
    "date": "2026-08-28",
    "title": "鲁力立在西安市某小学开展AI教育主题讲座",
    "title_full": "2026年8月底，鲁力立受邀在西安市一所小学开展为期一天的AI教育主题讲座。",
    "summary": "2026年8月底，鲁力立受邀前往西安市一所小学开展AI教育主题讲座，为期一天。这是鲁力立2026年暑假期间在外地开展的培训活动之一。",
    "category": "培训讲座",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_xian_related = {
    "id": "rel-evt-xian-aug2026",
    "date": "2026-08-28",
    "title": "鲁力立2026年8月底赴西安小学开展AI教育讲座",
    "title_full": "2026年8月底，鲁力立受邀在西安市一所小学开展为期一天的AI教育主题讲座。",
    "summary": "2026年8月底，鲁力立前往西安市一所小学开展AI教育主题讲座，为期一天。",
    "category": "培训讲座",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

# 5. 网络安全培训 (2026年8月下旬)
evt_security_base = {
    "id": "evt-base-security-aug2026",
    "date": "2026-08-26",
    "title": "网络安全主题培训活动在华东师范大学智慧教育产教基地举办",
    "title_full": "2026年8月下旬，一场网络安全主题培训活动在华东师范大学智慧教育产教基地举办，鲁力立参加该活动。",
    "summary": "2026年8月下旬，一场网络安全主题培训活动在华东师范大学智慧教育产教基地举办。鲁力立作为基地负责人参与了该培训活动。",
    "category": "培训活动",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_security_lulili = {
    "id": "evt-ll-security-aug2026",
    "date": "2026-08-26",
    "title": "鲁力立参加在智慧教育产教基地举办的网络安全培训活动",
    "title_full": "2026年8月下旬，鲁力立参加在华东师范大学智慧教育产教基地举办的网络安全主题培训活动。",
    "summary": "2026年8月下旬，鲁力立参加在华东师范大学智慧教育产教基地举办的网络安全主题培训活动。",
    "category": "培训活动",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

evt_security_related = {
    "id": "rel-evt-security-aug2026",
    "date": "2026-08-26",
    "title": "智慧教育产教基地举办网络安全主题培训活动",
    "title_full": "2026年8月下旬，华东师范大学智慧教育产教基地举办网络安全主题培训活动。",
    "summary": "2026年8月下旬，华东师范大学智慧教育产教基地举办网络安全主题培训活动，鲁力立参加。",
    "category": "培训活动",
    "sources": [
        {
            "name": "用户提供",
            "url": "",
            "date": "2026-08"
        }
    ],
    "source_count": 1,
    "type": "event_cluster",
    "importance": "medium"
}

# ========== 更新各主题文件 ==========

print("=" * 60)
print("开始更新主题文件...")
print("=" * 60)

# lulili.json
print("\n[1/6] 更新 lulili.json ...")
data = load_json('lulili.json')
added = 0
for evt in [evt_qingmu_lulili, evt_agent_lulili, evt_beihong_lulili_jul, evt_beihong_lulili_aug, evt_xian_lulili, evt_security_lulili]:
    if add_event(data, evt):
        added += 1
save_json('lulili.json', data)
print(f"  新增 {added} 条事件")

# metaverse.json
print("\n[2/6] 更新 metaverse.json ...")
data = load_json('metaverse.json')
added = 0
for evt in [evt_agent_metaverse]:
    if add_event(data, evt):
        added += 1
save_json('metaverse.json', data)
print(f"  新增 {added} 条事件")

# base.json
print("\n[3/6] 更新 base.json ...")
data = load_json('base.json')
added = 0
for evt in [evt_agent_base, evt_security_base]:
    if add_event(data, evt):
        added += 1
save_json('base.json', data)
print(f"  新增 {added} 条事件")

# yimu.json
print("\n[4/6] 更新 yimu.json ...")
data = load_json('yimu.json')
added = 0
# 清沐泽元获奖与壹幕工作室相关（鲁力立关联公司）
evt_qingmu_yimu = evt_qingmu_lulili.copy()
evt_qingmu_yimu['id'] = 'evt-yimu-qingmu-data2026'
if add_event(data, evt_qingmu_yimu):
    added += 1
save_json('yimu.json', data)
print(f"  新增 {added} 条事件")

# related.json
print("\n[5/6] 更新 related.json ...")
data = load_json('related.json')
added = 0
for evt in [evt_qingmu_related, evt_agent_related, evt_beihong_related, evt_xian_related, evt_security_related]:
    if add_event(data, evt):
        added += 1
save_json('related.json', data)
print(f"  新增 {added} 条事件")

# honors.json
print("\n[6/6] 更新 honors.json ...")
data = load_json('honors.json')
added = 0
for evt in [evt_qingmu_honors]:
    if add_event(data, evt):
        added += 1
save_json('honors.json', data)
print(f"  新增 {added} 条事件")

print("\n" + "=" * 60)
print("主题文件更新完成!")
print("=" * 60)

# ========== 更新 _meta.json ==========
print("\n更新 _meta.json ...")
meta = {
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_events": 0,
    "sources": [],
    "profile_sections": 5
}

for fname in ['lulili.json', 'metaverse.json', 'base.json', 'yimu.json', 'related.json', 'honors.json']:
    fdata = load_json(fname)
    count = len(fdata.get('results', []))
    meta['total_events'] += count
    meta['sources'].append({
        "file": fname,
        "topic": fdata['topic']['name'],
        "event_count": count
    })

save_json('_meta.json', meta)
print(f"  总事件数: {meta['total_events']}")

print("\n全部更新完成!")
