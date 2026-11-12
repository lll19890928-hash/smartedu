#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量添加18篇微信文章到各JSON数据文件"""

import json, os, uuid, re

BASE = "/Users/lulili/WorkBuddy/2026-06-02-20-17-02/news_monitor/results"

def load(fname):
    with open(os.path.join(BASE, fname), encoding="utf-8") as f:
        return json.load(f)

def save(fname, data):
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def uid():
    return "evt-" + uuid.uuid4().hex[:8]

# ═══════════════════════════════════════════════════════════
# 分类好的18篇文章（含鲁力立名字的 → lulili.json；否则按主题分）
# ═══════════════════════════════════════════════════════════

new_entries = {
    "lulili": [
        # 1. 浦东新区社区学院青年教师培训 (2026)
        {
            "id": uid(),
            "date": "2026-05",
            "title": "浦东新区社区学院青年教师专题培训",
            "title_full": "数字赋能·文脉润心 - 浦东新区社区学院青年教师专题培训纪实",
            "summary": "受邀为浦东新区社区学院青年教师开展"数字赋能"专题培训，上午场在华东师范大学智慧教育产教基地进行，分享数字化教学工具应用、混合式教学设计、教育元宇宙场景等前沿技术，引导教师树立"人机协同"的现代化教学思维，并与教师们进行互动研讨。下午场为武康路历史文化行走。",
            "category": "教学活动",
            "sources": [{"name": "浦东社区教育（微信公众号）", "url": "https://mp.weixin.qq.com/s/iM1aVf1TimrgqZVw7YxZDA"}],
            "keywords": ["浦东新区", "社区教育", "青年教师培训", "数字化教学", "人机协同"]
        },
        # 2. 吴迅中学特色通识课(I) (2026.02.27)
        {
            "id": uid(),
            "date": "2026-02-27",
            "title": "吴迅中学特色通识课：AI时代我们应当如何教学",
            "title_full": "【第1827期】AI时代，我们应当如何教学？--记2025学年第二学期特色通识课（I）",
            "summary": "受邀赴吴迅中学开展2025学年第二学期首场特色通识课，以《AI时代，我们应当如何教学？》为题，围绕AI赋能教学资源革新、推动课堂模式变革、明确AI能力边界、掌握AI使用方法论四个维度展开，现场演示30秒生成交互式网页课件，提出PERP人机协作新路径。",
            "category": "教学活动",
            "sources": [{"name": "吴迅中学家校联盟（微信公众号）", "url": "https://mp.weixin.qq.com/s/WuemeP4ZdUDxVJT1HVFJTg"}],
            "keywords": ["吴迅中学", "AI教学", "通识课", "人机协同", "PERP"]
        },
        # 3. 观澜小学信息化培训 (2026.05.09)
        {
            "id": uid(),
            "date": "2026-05-09",
            "title": "观澜小学教师信息化培训",
            "title_full": "拥抱AI变革，探寻教学新径--观澜小学信息化培训掠影",
            "summary": "受邀为上海市浦东新区观澜小学全体教师开展信息化培训，主讲《AI时代，我们要如何教学？》，针对不同大模型特性讲解使用技巧（通用大模型4W公式、推理大模型SPACE设计原则），提醒教师警惕AI幻觉问题，倡导以积极心态拥抱AI变革。",
            "category": "教学活动",
            "sources": [{"name": "上海市浦东新区观澜小学（微信公众号）", "url": "https://mp.weixin.qq.com/s/fEu_1QachONJkVM__nZWYA"}],
            "keywords": ["观澜小学", "浦东新区", "教师培训", "SPACE提示词", "AI幻觉"]
        },
        # 4. 吴迅中学教育智能体培训 (2026.05.08)
        {
            "id": uid(),
            "date": "2026-05-08",
            "title": "吴迅中学教育智能体应用能力提升培训",
            "title_full": "【第1863期】教育智能体赋能，助力教师数字转型--记我校开展教育智能体应用能力提升培训活动",
            "summary": "受邀赴吴迅中学开展'AI时代的教师核心素养 - 教育智能体的设计和搭建'专题培训，以'2026年是智能体元年'开篇，系统讲解AI智能体核心定义与技术逻辑，以腾讯WorkBuddy工具为案例现场演示备课、课堂互动、作业批改、学情分析等全流程应用。",
            "category": "教学活动",
            "sources": [{"name": "吴迅中学家校联盟（微信公众号）", "url": "https://mp.weixin.qq.com/s/AjZc65v3gGO3LmcyskBWCg"}],
            "keywords": ["吴迅中学", "教育智能体", "WorkBuddy", "数字转型", "AI素养"]
        },
        # 5. 吴迅中学特色通识课(II) (2026.03.17)
        {
            "id": uid(),
            "date": "2026-03-17",
            "title": "吴迅中学特色通识课（II）：AI时代教师核心素养",
            "title_full": "【第1842期】拥抱AI变革，赋能智慧育人--记2025学年第二学期特色通识课（II）",
            "summary": "受邀赴吴迅中学开展《AI时代教师的核心素养》专题培训，从精准提问（SPACE提示词方法论）、顶层设计（意义建构模型E-M-G）、人机协作（多模型协同覆盖教学全流程）、批判思维（警惕技术异化）四个维度展开，助力教师拥抱数字化变革。",
            "category": "教学活动",
            "sources": [{"name": "吴迅中学家校联盟（微信公众号）", "url": "https://mp.weixin.qq.com/s/gqDfVK846aG3ZtZ_eVI9iA"}],
            "keywords": ["吴迅中学", "SPACE", "E-M-G模型", "批判思维", "教师核心素养"]
        },
        # 6. 龚路中学AI教学分享 (2025.10.24)
        {
            "id": uid(),
            "date": "2025-10-24",
            "title": "上海第二工业大学附属龚路中学AI教育分享",
            "title_full": "【思敬书院】AI时代，我们要如何教学？--上海第二工业大学附属龚路中学组织开展教师培训",
            "summary": "受邀为上海第二工业大学附属龚路中学全校教师开展"AI时代，我们要如何教学？"教育分享会，展示AI在定制错题集、主观题批阅、知识点动画化、交互式网页课件等教学中的多元应用，提出教育三大变革（效能革命、范式重构、人机协同）。",
            "category": "教学活动",
            "sources": [{"name": "上海第二工业大学附属龚路中学（微信公众号）", "url": "https://mp.weixin.qq.com/s/DuDnpznsMBsLX9TNRcHLWg"}],
            "keywords": ["龚路中学", "AI教学", "效能革命", "范式重构", "人机协同"]
        },
        # 7. 华东师大暑期学校教师培训·乌鲁木齐 (2025.07.03-04)
        {
            "id": uid(),
            "date": "2025-07-03",
            "title": "华东师大暑期学校教师培训（乌鲁木齐）",
            "title_full": "名校领航逐梦·智启教育新章 | 生态文明教育基地及特色校授牌仪式暨华东师大暑期学校教师培训活动圆满举行",
            "summary": "受邀在华东师范大学生态与环境科学学院与乌鲁木齐市教育研究中心联合主办的暑期学校教师培训中开展《AI时代，我要如何教学》专题讲座，围绕AI时代教师四大核心素养展开讲解，带领现场教师动手实操，为边疆地区教师应对教育数字化转型提供指导。",
            "category": "教学活动",
            "sources": [{"name": "华师生环（微信公众号）", "url": "https://mp.weixin.qq.com/s/mxO2tgAsgLOFVTlNBXhjZA"}],
            "keywords": ["乌鲁木齐", "暑期学校", "生态文明教育", "教师培训", "数字化转型"]
        },
        # 8. 鑫考股份教育生态峰会 (2024.08.12)
        {
            "id": uid(),
            "date": "2024-08-12",
            "title": "鑫考股份教育生态峰会主题分享",
            "title_full": "共探教育新未来！鑫考股份教育生态峰会（运营商渠道专场）圆满落幕",
            "summary": "受邀出席鑫考股份教育生态峰会（运营商渠道专场），以《AI时代教育的变与守》为题作主题分享，提出技术打破传统教育边界、精准赋能取代批量培养的"变"，以及教师思维引导、情感关怀、价值塑造不可替代的"守"，引发全场共鸣。",
            "category": "媒体报道",
            "sources": [{"name": "鑫考股份（微信公众号）", "url": "https://mp.weixin.qq.com/s/83HY5avXyJD55nEOaDiZ5Q"}],
            "keywords": ["鑫考股份", "教育生态", "AI教育", "智慧校园", "教育公平"]
        },
        # 9. 普教院附校日本塩尻中学来访 (2025.10.20)
        {
            "id": uid(),
            "date": "2025-10-20",
            "title": "普教院附校教育元宇宙舱展示",
            "title_full": "迎国际好友 展附校之美--甘泉外国语学校姐妹校日本长野县塩尻中学学生代表来访交流",
            "summary": "在上海市普陀区教育学院附属学校接待日本长野县塩尻中学师生代表团的交流活动中，负责"慧课程"体验环节「遨游元宇宙」内容展示，介绍设立在普教院附校的全区首个教育元宇宙舱，展示AI互动体验、信息化教材使用、创新课堂模式等模块。",
            "category": "基地建设",
            "sources": [{"name": "上海市普陀区教育学院附属学校（微信公众号）", "url": "https://mp.weixin.qq.com/s/kuHmwX_KIcBNXBd3E5pKbw"}],
            "keywords": ["教育元宇宙舱", "普教院附校", "日本交流", "国际化", "元宇宙"]
        },
        # 10. 沈阳科技学院新教师研修班 (2025.10.28-11.01)
        {
            "id": uid(),
            "date": "2025-10-28",
            "title": "沈阳科技学院新教师教学能力提升研修班",
            "title_full": "华东师范大学--沈阳科技学院新教师教学能力提升研修班（第二期）圆满结束",
            "summary": "作为授课讲师参加华东师范大学与沈阳科技学院联合举办的第二期新教师教学能力提升研修班，与张琳老师共同主讲《教学观摩：优秀教学示范与交流》课程，讲解教学设计流程、方法技巧、课堂管理与学生评价反馈，指导教学软件实现第一第二课堂联动。",
            "category": "教学活动",
            "sources": [{"name": "沈阳科技学院（微信公众号）", "url": "https://mp.weixin.qq.com/s/zTL64hIJA2pOcd9xgteWtQ"}],
            "keywords": ["沈阳科技学院", "新教师培训", "教学观摩", "教学设计", "课堂管理"]
        },
        # 11. E生向党 长征VR活动交流 (2025.05.18)
        {
            "id": uid(),
            "date": "2025-05-18",
            "title": "华师大教育信息技术系党支部智慧基地交流活动",
            "title_full": "循长征光影之途 感数智教育之脉",
            "summary": "参与华东师范大学教育信息技术学系专业型硕士研究生党支部赴智慧教育产教基地的红色采风活动，在交流环节与同学们就智慧教育产品的课堂需求、用户体验、教育适配性及底层技术实现等专业问题展开深入讨论。",
            "category": "基地建设",
            "sources": [{"name": "E生向党（微信公众号）", "url": "https://mp.weixin.qq.com/s/ymuj48vQLGI6N61YxX3ocg"}],
            "keywords": ["智慧教育产教基地", "长征VR", "党支部", "红色教育", "数智教育"]
        },
    ],

    "yimu": [
        # 壹幕工作室 - AIGC人机协同研究参加第三届短视频创研国际会议 (2023.05.23)
        {
            "id": uid(),
            "date": "2023-05-23",
            "title": "壹幕工作室AIGC人机协同研究参加第三届短视频创研国际会议",
            "title_full": "【研究进展】团队AIGC人机协同研究成果参会第三届短视频创研国际会议",
            "summary": "壹幕工作室指导老师鲁力立、团队成员刘子衿受邀参加第三届短视频创研国际会议（上海师范大学），在"产业生态与协同进化"分论坛分享《从技术路径到能力图谱：AIGC驱动下影视创作的人机协同螺旋模型研究》阶段性成果，以《信息安全科普动画》系列AIGC创作实践为案例。",
            "category": "学术会议",
            "sources": [{"name": "EMOVIE壹幕工作室（微信公众号）", "url": "https://mp.weixin.qq.com/s/zw1xT5D3N732DwOs2_oSGg"}],
            "keywords": ["AIGC", "人机协同", "短视频创研国际会议", "影视创作", "螺旋模型"]
        },
    ],

    "base": [
        # 华东师大科技园走进腾讯 (2024.04.10)
        {
            "id": uid(),
            "date": "2024-04-10",
            "title": "华东师大科技成果转化对接会走进腾讯",
            "title_full": "【园区动态】华东师范大学科技成果转化项目要素对接会"人工智能·走进腾讯"专场活动成功举办",
            "summary": "在华东师大科技园与腾讯云联合主办的"人工智能·走进腾讯"科技成果转化对接会上，鲁力立团队在项目路演环节展示"教育元宇宙未来课堂"项目，介绍融合CAVE、MR、全息交互等技术构建的"未来教室+课堂"体系，包含小型接入舱、中型空间站、大型实验室三类虚实融合教学空间。",
            "category": "基地建设",
            "sources": [{"name": "华东师范大学国家大学科技园（微信公众号）", "url": "https://mp.weixin.qq.com/s/GGiYlWd7BIewfQMkjVJSFw"}],
            "keywords": ["科技园", "腾讯云", "科技成果转化", "教育元宇宙", "CAVE", "项目路演"]
        },
        # 智慧教育产教基地揭牌 - 世界教育者大会报道
        {
            "id": uid(),
            "date": "2026-04",
            "title": "智慧教育产教基地揭牌暨"四个未来"试验场报道",
            "title_full": "破局教育科技转化死局！华东师大打造「四个未来」试验场，重构智慧教育产教新生态",
            "summary": "华东师范大学上海数字化教育装备工程技术研究中心智慧教育产教基地在上海静安多媒体谷正式揭牌，基地联合清华、北师大等高校智库及全国40余所中小学、30余家企业，围绕未来学校、未来课堂、未来美育、未来育人构建智慧教育改革试验场，现场首发四款自研孵化产品。",
            "category": "基地建设",
            "sources": [{"name": "世界教育者大会（微信公众号）", "url": "https://mp.weixin.qq.com/s/FelCiDWLt_NYq8N8V2ykiw"}],
            "keywords": ["智慧教育产教基地", "揭牌", "四个未来", "成果孵化", "产学研"]
        },
        # ECNU艺教 参观智慧教育产教基地 (2026.05.26)
        {
            "id": uid(),
            "date": "2026-05-26",
            "title": "艺术教育部赴智慧教育产教基地参观学习",
            "title_full": "艺术教育部赴智慧教育产教基地参观学习 沉浸式体验智慧美育前沿场景",
            "summary": "华东师范大学艺术教育部教师赴智慧教育产教基地参观学习，实地体验"未来教室""教育元宇宙未来课堂""智慧美育工坊"等场景，重点围绕数字技术与美育教学、艺术疗愈研究及师资培训的融合路径展开调研，为美育教师数字素养提升提供方向。",
            "category": "基地建设",
            "sources": [{"name": "ECNU艺教（微信公众号）", "url": "https://mp.weixin.qq.com/s/Z3CygG8AB3FgfNxCUK6_CQ"}],
            "keywords": ["智慧教育产教基地", "艺术教育部", "智慧美育", "师资培训", "数字素养"]
        },
        # 大民堂 周回顾提及基地 (2026.04)
        {
            "id": uid(),
            "date": "2026-04",
            "title": "大民堂周回顾：全国首个智慧教育产教基地落地上海",
            "title_full": "一周回顾 | 教育部发布青少年阅读教育行业标准，全国首个智慧教育产教基地落地上海",
            "summary": "教育行业周报大民堂报道：全国首个智慧教育产教基地落地上海静安区，打造集"自选超市+联合研发"于一体的未来学校样板间。",
            "category": "媒体报道",
            "sources": [{"name": "大民堂（微信公众号）", "url": "https://mp.weixin.qq.com/s/YT3FOn8Enmulq1uSIG3nIA"}],
            "keywords": ["智慧教育产教基地", "大民堂", "上海静安", "未来学校"]
        },
    ],
}

# ═══════════════════════════════════════════════════════════
# 去重 + 写入
# ═══════════════════════════════════════════════════════════

stats = {}

for topic, entries in new_entries.items():
    data = load(topic + ".json")
    existing_urls = set()
    for r in data["results"]:
        for s in r.get("sources", []):
            existing_urls.add(s.get("url", ""))
    
    added = 0
    skipped = 0
    for entry in entries:
        entry_urls = [s.get("url", "") for s in entry.get("sources", [])]
        if any(u in existing_urls for u in entry_urls):
            skipped += 1
            print(f"  SKIP (duplicate URL): {entry['title'][:40]}")
            continue
        data["results"].append(entry)
        added += 1
        for u in entry_urls:
            existing_urls.add(u)
    
    data["results"].sort(key=lambda x: x.get("date", ""), reverse=True)
    data["total"] = len(data["results"])
    data["stats"] = {"total": len(data["results"])}
    save(topic + ".json", data)
    stats[topic] = {"added": added, "skipped": skipped, "total": len(data["results"])}
    print(f"  {topic}.json: +{added}, skip={skipped}, total={len(data['results'])}")

# ═══════════════════════════════════════════════════════════
# 龚路中学月回顾（重复URL，跳过）
# ═══════════════════════════════════════════════════════════
print("\n注意：以下文章已存在或不含鲁力立信息，已跳过：")
skip_list = [
    ("https://mp.weixin.qq.com/s/YHLGMhCqFOxfDTpcGY_S7g", "龚路中学10月要闻回顾（与DuDnpzns链接内容重叠）"),
    ("https://mp.weixin.qq.com/s/ymuj48vQLGI6N61YxX3ocg", "E生向党长征VR活动（已入库）"),
]
for url, reason in skip_list:
    print(f"  SKIP: {reason}")

print("\n完成！汇总：")
for t, s in stats.items():
    print(f"  {t}: 新增{s['added']}条, 跳过{s['skipped']}条, 总计{s['total']}条")
