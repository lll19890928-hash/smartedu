#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-12 周更：将本次检索结果合并入 _new_findings.json（按 URL / 标题去重）"""
import json, os, io

BASE = os.path.dirname(os.path.abspath(__file__))
FINDINGS = os.path.join(BASE, "_new_findings.json")
FOUND_AT = "2026-11-12T09:30:00+08:00"

Q1 = '"鲁力立" 华东师范大学 高级工程师 副教授'
Q2 = '"鲁力立" 教育元宇宙 未来课堂'
Q3 = '"鲁力立" 壹幕工作室'
Q4 = '"鲁力立" 智慧教育 产教基地'
Q5 = '"清沐泽元" 上海清沐泽元教育科技有限公司'
Q6 = '鲁力立 2026年11月 最新动态 讲座 论坛'

NEW = [
    # ---------- Q1 ----------
    {
        "query": Q1,
        "title": "媒体关注丨科研落地也需“问诊” 华东师大首开科技成果转化门诊反响热烈",
        "url": "https://www.ecnu.edu.cn/info/1426/67552.htm",
        "snippet": "教育信息技术学系高级工程师鲁力立研发的“教育元宇宙未来课堂”项目2022年在世界人工智能大会首发，去年落地普陀区教育学院附属学校，但面对转化难题因经验不足遇阻。深度问诊环节专家用一个多小时从商业识别、路径设计、专利布局等维度提供转化方案。科技处处长杨海波表示已规划每月邀请专家“坐诊”。",
        "date": "2024-10-31",
        "found_at": FOUND_AT,
    },
    {
        "query": Q1,
        "title": "新书首发｜《AIGC重塑数字媒体创作》正式出版（含主编简介最新职务）",
        "url": "http://mp.weixin.qq.com/s?__biz=MzU4ODAzNzA2OA==&mid=2247491507&idx=1&sn=27c22c0021acedc98ddf7289e0288a7b",
        "snippet": "主编简介更新：鲁力立，华东师范大学教育学部高级工程师，教育数字媒体综合实验室负责人，上海市数字化教育装备工程技术研究中心主任助理，国家大学科技园概念验证中心智库专家；2024年起专注科技成果转化，成立壹生万幕（上海）教育科技有限公司，并负责华东师大智慧教育产教基地具体工作。文中另述团队走进上海吴迅中学开展AIGC进课堂实践。",
        "date": "2025-11",
        "found_at": FOUND_AT,
    },
    # ---------- Q3：壹幕工作室历史报道（首次检索到，补全早期档案） ----------
    {
        "query": Q3,
        "title": "【壹幕速报】停课不停学！全民抗疫，壹幕工作室在行动！",
        "url": "http://mp.weixin.qq.com/s?__biz=MzU4ODAzNzA2OA==&mid=2247484465&idx=1&sn=8e35f032467a80bb5792acf7d42c99e0",
        "snippet": "疫情期间壹幕工作室在鲁力立老师带领下，3名2017级同学与全体2018级同学历时一个月完成“抗疫中的教育学”100+个微课程制作，累计500+分钟、50万+浏览量，同步在学习强国、澎湃、喜马拉雅、B站推出，文汇报等媒体报道。",
        "date": "2020-03-06",
        "found_at": FOUND_AT,
    },
    {
        "query": Q3,
        "title": "喜报｜我系壹幕工作室与大夏书院联合创作的专题短片在中国教育电视台播出",
        "url": "https://www.deit.ecnu.edu.cn/20/11/c26198a270353/page.htm",
        "snippet": "教育部关工委“读懂中国”活动，鲁力立老师团队与大夏书院联合创作《变化的时代，不变的奋斗——俞立中校长访谈录》，从全国过百件作品中入选15个展播作品，作为代表我校的唯一作品于2019年1月4日在中国教育电视台（CETV1）播出。",
        "date": "2019-01",
        "found_at": FOUND_AT,
    },
    {
        "query": Q3,
        "title": "我系本科生团队在第五届上海市公益广告大赛中获奖 并在上海地铁公交展播作品",
        "url": "https://www.deit.ecnu.edu.cn/20/07/c26198a270343/page.htm",
        "snippet": "鲁力立老师指导的公益短片《亡烟》在“微公益·新征程”第五届上海市公益广告大赛获视频类优秀奖（第11名），为我校唯一视频类获奖作品；作品脱胎于《影视编导》期末作业，经壹幕工作室6个月针对性孵化。",
        "date": "2018-12-22",
        "found_at": FOUND_AT,
    },
    {
        "query": Q3,
        "title": "摄像大师&华东师大出版社：入门级摄像教程（壹幕工作室系列教学视频）",
        "url": "http://mp.weixin.qq.com/s?__biz=MzUyOTUzMTQ5Mg==&mid=2247483697&idx=1&sn=80584ca027236f9e5f1a8dae23392462",
        "snippet": "壹幕工作室与华东师大出版社合作开发摄像系列教学视频并出版数字课程，鲁力立任指导老师，团队完成教学大纲、拍摄脚本、解说词与成品，配套交互Flash与H5页面。",
        "date": "2019",
        "found_at": FOUND_AT,
    },
    # ---------- Q4：产教基地 2026-04-18 揭牌 ----------
    {
        "query": Q4,
        "title": "破局教育数字化“最后一公里”！华东师范大学打造全国首个面向未来的智慧教育产品交易、发展、生态平台",
        "url": "https://www.deit.ecnu.edu.cn/8c/01/c26198a756737/page.htm",
        "snippet": "智慧教育产教基地揭牌仪式2026年4月18日在静安区多媒体大厦举行，40余所中小学代表与30余家行业领军企业到场。三大平台同步点亮：智慧教育产教基地、数智教育产教联盟、智慧教育成果孵化空间。副校长戴立益、彭浦镇党委书记程凯致辞，提出“教育出题、高校解题、企业答题”协同机制与“四个未来”先行试验场。",
        "date": "2026-04-18",
        "found_at": FOUND_AT,
    },
    {
        "query": Q4,
        "title": "黑科技云集！全国首个智慧教育产品超市正式营业（齐鲁晚报）",
        "url": "https://m.qlwb.com.cn/detail/27505945.html",
        "snippet": "4月18日全国首个面向未来的智慧教育产品交易、发展、生态平台在上海落地。500㎡“未来学校”样板空间采用“沉浸式体验+线上购物车”交易模式，中小学代表化身“采购官”。首批孵化产品“云痕智能教学一体化平台”“数智优学”“教育元宇宙未来课堂”“星脉智育”正式发布。",
        "date": "2026-04-18",
        "found_at": FOUND_AT,
    },
    {
        "query": Q4,
        "title": "政校合力｜彭浦镇党委书记程凯带队调研华东师范大学智慧教育产教基地（公众号版）",
        "url": "http://mp.weixin.qq.com/s?__biz=MzIyMDEzMzA1MQ==&mid=2247509224&idx=1&sn=f64da9b480626258c288c01adde8fe63",
        "snippet": "2026年2月5日调研报道公众号原文，明确称鲁力立为“华东师范大学智慧教育产教基地具体负责人”，并附基地建设背景图解（2025年7月正式揭牌、彭浦镇政府统筹协调、静安超高清产业政策赋能）。",
        "date": "2026-02-05",
        "found_at": FOUND_AT,
    },
    {
        "query": Q4,
        "title": "亮相WAIC｜智慧教育产教基地入选静安六大AI场景运营子平台（公众号版）",
        "url": "http://mp.weixin.qq.com/s?__biz=MzY5NjE3NjMzNA==&mid=2247500267&idx=1&sn=20246ff354733d1953f3eb9100519bef",
        "snippet": "2026年7月17日WAIC2026“Connect静安·场景涌现”专场，静安六大AI场景运营子平台启动，产教基地入选“AI+教育”子平台，鲁力立作为基地代表参与启动仪式；大会期间基地开放日接待超30场参访。",
        "date": "2026-07-17",
        "found_at": FOUND_AT,
    },
    # ---------- Q5：清沐泽元 ----------
    {
        "query": Q5,
        "title": "上海清沐泽元教育科技有限公司（企查查，2026-11-08 更新）—— 对外投资增至3家",
        "url": "https://www.qcc.com/firm/dc355270f75496e0c923cb66425120af.html",
        "snippet": "法定代表人陈炯毅，注册资本100万元、实缴40万元，成立2025-08-07，地址静安区广中西路757号1508室。对外投资3家：上海昕乔壹教育科技有限公司（2025-11-17，35%）、上海光启智瞳信息科技有限公司（2026-03-31，8%）、上海学小满智能科技有限公司（2026-03-10，8%）。企业族群标注“花狮信科”。",
        "date": "2026-11-08",
        "found_at": FOUND_AT,
    },
    {
        "query": Q5,
        "title": "上海清沐泽元教育科技有限公司 股权关系查询（企百科）—— 3家对外投资明细",
        "url": "https://www.qibook.com/company-wiki-s/shanghaiqingmuzeyuanjiaoyukejiyouxiangongsi-08cc1528.html",
        "snippet": "对外投资共3家，均为货币出资、非上市：昕乔壹（35.00%，35万元，2025-11-17）、光启智瞳（8.00%，8万元，2026-03-31）、学小满（8.00%，4万元，注册资本50万元，2026-03-10）。",
        "date": "2026-11",
        "found_at": FOUND_AT,
    },
    {
        "query": Q5,
        "title": "上海清沐泽元教育科技有限公司（猎聘企业页）",
        "url": "https://m.liepin.com/company/gs126740518",
        "snippet": "企业性质：IT服务/私营民营企业；注册地上海市静安区广中西路757号1508室，注册资本100万元，成立2025-08-07，法人代表陈炯毅，统一信用代码91310106MAETDB3X9K，登记机关静安区市场监管局，经营状态存续。",
        "date": "2026-11",
        "found_at": FOUND_AT,
    },
]

def main():
    with io.open(FINDINGS, "r", encoding="utf-8") as f:
        data = json.load(f)
    seen_url = {x.get("url", "").strip() for x in data if x.get("url")}
    seen_title = {x.get("title", "").strip() for x in data if x.get("title")}
    added = 0
    for rec in NEW:
        u = rec["url"].strip()
        if u and u in seen_url:
            continue
        # 以标题前 18 字做弱去重
        key = rec["title"][:18]
        if any(t[:18] == key for t in seen_title):
            continue
        data.append(rec)
        seen_url.add(u)
        seen_title.add(rec["title"])
        added += 1
    with io.open(FINDINGS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("added:", added)
    print("total:", len(data))

if __name__ == "__main__":
    main()
