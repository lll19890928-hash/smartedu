#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-11-12 数据入库（第二轮）
新增：
  1. ChinaVR 2026（第二十六届中国虚拟现实大会，2026-11-06/08 广州）论文口头报告
  2. 清沐泽元对外投资增至3家（光启智瞳 8% / 学小满 8% / 昕乔壹 35%）
  3. 壹幕工作室早期档案 4 条（2018-2020）
更新：
  4. 数据要素×大赛上海分赛三等奖 → 标注「第一完成人/第一作者」
  5. profile.json 3.1 论文新增 ChinaVR 论文、3.5 会议新增 2026.11、2.1 获奖补注
"""
import json, os, io, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DST = "/Users/lulili/WorkBuddy/2026-06-02-20-17-02/news_monitor"

def load(name):
    with io.open(os.path.join(BASE, name), "r", encoding="utf-8") as f:
        return json.load(f)

def save(name, data):
    with io.open(os.path.join(BASE, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- 事件定义
SRC_CHINAVR = [
    {"name": "ChinaVR 2026 会议官网（中国计算机学会）",
     "url": "https://ccf.org.cn/chinavr2026/brief_1008", "date": "2026-11"},
    {"name": "ChinaVR 2026 会议论文口头汇报日程",
     "url": "http://mp.weixin.qq.com/s?__biz=MzkzNzY4MTc0MA==&mid=2247486842&idx=5&sn=fa132d57e040b65f2fd7e7070800e8ec",
     "date": "2026-11-02"},
    {"name": "第二十六届中国虚拟现实大会在广州开幕（广州日报新花城）",
     "url": "https://huacheng.gz-cmc.com/pages/2026/11/08/756d4c306ab04943b2051019631c781d.html",
     "date": "2026-11-08"},
]

EVT_CHINAVR = {
    "id": "evt-ll-chinavr2026",
    "date": "2026-11-08",
    "title": "鲁力立参加ChinaVR 2026（第二十六届中国虚拟现实大会）并作论文口头报告",
    "title_full": "2026年11月6-8日，第二十六届中国虚拟现实大会（ChinaVR 2026）在广州举行，鲁力立参会并于11月8日在会议论文口头汇报「虚实交互与应用」专场报告论文《3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究》。",
    "summary": "第二十六届中国虚拟现实大会（ChinaVR 2026）于2026年11月6-8日在广州朗豪酒店举行，由中国计算机学会、中国仿真学会、中国图像图形学会联合主办，CCF/CSF/CSIG 虚拟现实专委会与暨南大学承办，与第三届国际扩展现实会议（ICXR 2026）同期同地举办，千余位专家学者参会，主题为「虚拟现实与人工智能的双向赋能」。11月8日15:40-17:30的会议论文口头汇报（四）「虚实交互与应用」专场（朗丰厅FG，主持人罗天任）中，16:20-16:30 报告论文《3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究》，鲁力立为第一作者。该研究以体积视频技术重建3D虚拟教师形象，测评其在教育场景中的情绪传播与感知效应，与团队此前在中国教育技术学术大会获奖的《基于体积视频技术的3D虚拟教师形象的情绪传播效应测评》属同一研究脉络。",
    "category": "学术会议",
    "sources": SRC_CHINAVR,
    "source_count": 3,
    "type": "event_cluster",
    "importance": "high",
}

EVT_META_CHINAVR = {
    "id": "evt-meta-chinavr2026",
    "date": "2026-11-08",
    "title": "ChinaVR 2026：体积视频驱动的3D虚拟教师情绪感知效应研究作口头报告",
    "title_full": "2026年11月8日，鲁力立团队在第二十六届中国虚拟现实大会（ChinaVR 2026）「虚实交互与应用」专场报告《3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究》。",
    "summary": "该研究聚焦教育元宇宙中的「数智教师」形象建构：以体积视频（Volumetric Video）技术采集真实教师的三维动态形象，生成高保真3D虚拟教师，并通过实验测评其在教学场景中的情绪表达与学习者感知效果。研究将数字人形象的真实感、情绪传播效力与教学临场感联系起来，为教育元宇宙未来课堂中「元元老师」等数智教师IP的设计提供实证依据。成果于ChinaVR 2026（2026年11月6-8日，广州，CCF/CSF/CSIG 联合主办）会议论文口头汇报（四）专场报告。",
    "category": "技术研究",
    "sources": SRC_CHINAVR,
    "source_count": 3,
    "type": "event_cluster",
    "importance": "high",
}

EVT_REL_CHINAVR = {
    "id": "evt-rel-chinavr2026",
    "date": "2026-11-08",
    "title": "鲁力立团队ChinaVR 2026报告3D虚拟教师情绪感知研究",
    "title_full": "2026年11月8日，第二十六届中国虚拟现实大会（ChinaVR 2026）「虚实交互与应用」专场，鲁力立团队报告《3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究》。",
    "summary": "ChinaVR 是中国虚拟现实领域创办最早（2001年，赵沁平院士发起）、规模最大的年度学术盛会。本届（第二十六届）于2026年11月6-8日在广州举行，主题「虚拟现实与人工智能的双向赋能」，设8场主旨报告（王自力、张文军、李树涛院士等）、十余场技术论坛与四场会议论文口头汇报。鲁力立团队的体积视频虚拟教师研究在「虚实交互与应用」专场报告，属XR内容与教育应用交叉方向。",
    "category": "学术会议",
    "sources": SRC_CHINAVR,
    "source_count": 3,
    "type": "event_cluster",
    "importance": "medium",
}

EVT_BASE_INVEST = {
    "id": "evt-base-qingmu-investments",
    "date": "2026-03-31",
    "title": "清沐泽元对外投资增至3家：昕乔壹35%、光启智瞳8%、学小满8%",
    "title_full": "截至2026年3月31日，智慧教育产教基地运营公司上海清沐泽元教育科技有限公司对外投资共3家企业：上海昕乔壹教育科技有限公司（35%）、上海光启智瞳信息科技有限公司（8%）、上海学小满智能科技有限公司（8%）。",
    "summary": "工商信息显示，上海清沐泽元教育科技有限公司（2025-08-07成立，注册资本100万元、实缴40万元，法定代表人陈炯毅，鲁力立持股30%、上海花狮信息科技有限公司持股70%，注册地静安区广中西路757号1508室）对外投资已增至3家：①上海昕乔壹教育科技有限公司（2025-11-17成立，注册资本100万元，持股35%，法定代表人黄英，另65%为上海通与通养老服务有限公司）；②上海光启智瞳信息科技有限公司（2026-03-31成立，注册资本100万元，持股8%，认缴8万元）；③上海学小满智能科技有限公司（2026-03-10成立，注册资本50万元，持股8%，认缴4万元，法定代表人陈宏鑫）。企查查将该企业族群标注为「花狮信科」。该投资布局与智慧教育产教基地「投资孵化」职能相衔接。",
    "category": "创业动态",
    "sources": [
        {"name": "企查查-上海清沐泽元教育科技有限公司（2026-11-08更新）",
         "url": "https://www.qcc.com/firm/dc355270f75496e0c923cb66425120af.html", "date": "2026-11-08"},
        {"name": "企百科-清沐泽元股权关系查询（对外投资明细）",
         "url": "https://www.qibook.com/company-wiki-s/shanghaiqingmuzeyuanjiaoyukejiyouxiangongsi-08cc1528.html", "date": "2026-11"},
        {"name": "水滴信用-上海昕乔壹教育科技有限公司",
         "url": "https://m.shuidi.cn/company-fe8ef769b99750c6974bb24aecf5f001.html", "date": "2026-11"},
    ],
    "source_count": 3,
    "type": "event_cluster",
    "importance": "medium",
}

EVT_YIMU_EARLY = [
    {
        "id": "evt-yimu-cetv2019",
        "date": "2019-01-04",
        "title": "壹幕工作室与大夏书院联合创作的《俞立中校长访谈录》在中国教育电视台播出",
        "title_full": "2019年1月4日，壹幕工作室与大夏书院联合创作的专题短片《变化的时代，不变的奋斗——俞立中校长访谈录》在中国教育电视台（CETV1）播出。",
        "summary": "教育部关工委「读懂中国」活动作品。在鲁力立老师带领下，壹幕工作室与大夏书院从脚本创作、实地考察、拍摄到后期反复打磨完成短片，从全国过百件报送作品中入选全国15个展播作品，为我校唯一入选作品。",
        "category": "壹幕工作室",
        "sources": [{"name": "华东师大教育信息技术学系官网",
                     "url": "https://www.deit.ecnu.edu.cn/20/11/c26198a270353/page.htm", "date": "2019-01"}],
        "source_count": 1, "type": "event_cluster", "importance": "medium",
    },
    {
        "id": "evt-yimu-wuyan2018",
        "date": "2018-12-22",
        "title": "壹幕工作室指导作品《亡烟》获第五届上海市公益广告大赛视频类优秀奖",
        "title_full": "2018年12月，鲁力立老师指导、壹幕工作室孵化的公益短片《亡烟》在「微公益·新征程」第五届上海市公益广告大赛中获视频类优秀奖（第11名），为我校唯一视频类获奖作品。",
        "summary": "作品脱胎于《影视编导》课程期末作业，经壹幕工作室6个月针对性专业改造与孵化后参赛，从2429份海选作品中入围训练营。大赛视频类设金奖2名、银奖3名、铜奖5名、优秀奖6名，团队以非艺术院系背景获第11名，并在上海地铁公交展播，12月22日于上海教育电视台录制颁奖晚会。",
        "category": "壹幕工作室",
        "sources": [{"name": "华东师大教育信息技术学系官网",
                     "url": "https://www.deit.ecnu.edu.cn/20/07/c26198a270343/page.htm", "date": "2018-12"}],
        "source_count": 1, "type": "event_cluster", "importance": "medium",
    },
    {
        "id": "evt-yimu-kangyi2020",
        "date": "2020-03-06",
        "title": "壹幕工作室完成「抗疫中的教育学」100+微课程制作",
        "title_full": "2020年2-3月，壹幕工作室在鲁力立老师带领下完成教育学部「抗疫中的教育学」100+个微课程制作，累计500+分钟、50万+浏览量。",
        "summary": "疫情期间教育学部倡议全体教师开设「抗疫中的教育学」微信微课程。壹幕工作室3名2017级同学与全体2018级同学历时一个月完成整套100+个微课程的制作，并在学习强国、澎湃新闻、喜马拉雅、哔哩哔哩同步推出，文汇报、华东师大官微等媒体报道，视频点击量27万余人次。团队另承担美国堪萨斯大学英文微课的中英文字幕校对工作。",
        "category": "壹幕工作室",
        "sources": [{"name": "壹幕工作室公众号【壹幕速报】",
                     "url": "http://mp.weixin.qq.com/s?__biz=MzU4ODAzNzA2OA==&mid=2247484465&idx=1&sn=8e35f032467a80bb5792acf7d42c99e0",
                     "date": "2020-03-06"}],
        "source_count": 1, "type": "event_cluster", "importance": "medium",
    },
    {
        "id": "evt-yimu-camera-course2019",
        "date": "2019-06",
        "title": "壹幕工作室与华东师大出版社合作出版摄像系列数字教程",
        "title_full": "2019年，壹幕工作室与华东师大出版社合作开发摄像系列教学视频并出版数字课程，鲁力立任指导老师。",
        "summary": "师生团队完成教学大纲、拍摄脚本、解说词与全部成品，配套交互Flash、H5页面与系列微课视频，形成可订阅的线上摄像入门课程，是壹幕工作室「教学—实践—科创—服务」四位一体育人模式的早期成果之一。",
        "category": "壹幕工作室",
        "sources": [{"name": "摄像大师×华东师大出版社 公众号",
                     "url": "http://mp.weixin.qq.com/s?__biz=MzUyOTUzMTQ5Mg==&mid=2247483697&idx=1&sn=80584ca027236f9e5f1a8dae23392462",
                     "date": "2019"}],
        "source_count": 1, "type": "event_cluster", "importance": "low",
    },
]

# ---------------------------------------------------------------- 工具
def add_events(data, evts, tag):
    existing = {e.get("id") for e in data["results"] if isinstance(e, dict)}
    added = []
    for e in evts:
        if e["id"] in existing:
            continue
        data["results"].append(e)
        existing.add(e["id"])
        added.append(e["id"])
    n = len(added)
    if n:
        data["total"] = data.get("total", 0) + n
        data["events_total"] = data.get("events_total", 0) + n
        if isinstance(data.get("stats"), dict):
            if "total" in data["stats"]:
                data["stats"]["total"] = data["stats"].get("total", 0) + n
    print(f"[{tag}] added {n}: {added}")
    return n

def bump_qingmu_refs(data):
    """在既有数据要素获奖事件中补注第一完成人/第一作者"""
    hits = 0
    for e in data.get("results", []):
        if not isinstance(e, dict):
            continue
        if e.get("id", "").endswith("qingmu-data2026") or "数据要素" in e.get("title", ""):
            for k in ("title_full", "summary"):
                v = e.get(k, "")
                if v and "第一完成人" not in v:
                    e[k] = v.replace(
                        "鲁力立代表智慧教育产教基地运营公司",
                        "鲁力立作为项目第一完成人（第一作者）代表智慧教育产教基地运营公司"
                    ).replace(
                        "鲁力立代表智慧教育产教基地运营公司上海清沐泽元教育科技有限公司参赛",
                        "鲁力立作为项目第一完成人（第一作者）代表智慧教育产教基地运营公司上海清沐泽元教育科技有限公司参赛"
                    )
                    if "第一完成人" not in e[k]:
                        e[k] = v + " 鲁力立为该项目第一完成人（第一作者）。"
            hits += 1
    print(f"  qingmu award events patched: {hits}")

# ---------------------------------------------------------------- 主流程
def main():
    # 1) lulili.json
    d = load("lulili.json"); add_events(d, [EVT_CHINAVR, EVT_BASE_INVEST], "lulili"); bump_qingmu_refs(d); save("lulili.json", d)
    # 2) metaverse.json
    d = load("metaverse.json"); add_events(d, [EVT_META_CHINAVR], "metaverse"); save("metaverse.json", d)
    # 3) related.json
    d = load("related.json"); add_events(d, [EVT_REL_CHINAVR], "related"); bump_qingmu_refs(d); save("related.json", d)
    # 4) base.json
    d = load("base.json"); add_events(d, [EVT_BASE_INVEST], "base"); bump_qingmu_refs(d); save("base.json", d)
    # 5) yimu.json
    d = load("yimu.json"); add_events(d, [dict(EVT_CHINAVR, id="evt-yimu-chinavr2026", category="壹幕工作室")] + EVT_YIMU_EARLY, "yimu"); bump_qingmu_refs(d); save("yimu.json", d)
    # 6) honors.json
    d = load("honors.json"); bump_qingmu_refs(d); save("honors.json", d)

    # 7) profile.json
    p = load("profile.json")
    blocks = p["results"]
    for b in blocks:
        for s in b.get("subsections", []):
            title = s.get("title", "")
            # 3.1 论文：插入 ChinaVR 论文并重排序号
            if title.startswith("3.1"):
                rows = s["rows"]
                if not any("ChinaVR" in r[1] for r in rows):
                    new_row = [
                        "[1]",
                        "鲁力立, 等. 3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究[C]. 第二十六届中国虚拟现实大会（ChinaVR 2026）论文集, 广州: 暨南大学, 2026年11月6-8日.（会议论文口头汇报·虚实交互与应用专场，2026年11月8日16:20-16:30；中国计算机学会、中国仿真学会、中国图像图形学会联合主办）",
                        "ChinaVR 2026",
                        "2026",
                        "国内会议论文",
                        "第一作者",
                        "[口头汇报日程](http://mp.weixin.qq.com/s?__biz=MzkzNzY4MTc0MA==&mid=2247486842&idx=5&sn=fa132d57e040b65f2fd7e7070800e8ec)",
                    ]
                    rows.insert(0, new_row)
                    for i, r in enumerate(rows, start=1):
                        r[0] = f"[{i}]"
                    print("  profile 3.1 论文: inserted ChinaVR row, total", len(rows))
            # 3.5 会议
            if title.startswith("3.5"):
                items = s["items"]
                if not any("ChinaVR" in json.dumps(it, ensure_ascii=False) for it in items):
                    items.insert(0, {
                        "label": "2026.11",
                        "value": "第二十六届中国虚拟现实大会（ChinaVR 2026，广州，11月6-8日，中国计算机学会/中国仿真学会/中国图像图形学会主办、暨南大学承办，与ICXR 2026同期），在会议论文口头汇报「虚实交互与应用」专场报告论文《3D虚拟教师在教育场景中的情绪感知效应：基于体积视频技术的实验研究》（11月8日16:20-16:30，朗丰厅FG）"
                    })
                    print("  profile 3.5 会议: inserted ChinaVR, total", len(items))
            # 2.1 获奖补注
            if title.startswith("2.1"):
                for it in s["items"]:
                    if "数据要素" in it.get("value", "") and "第一完成人" not in it["value"]:
                        it["value"] = it["value"].replace(
                            "（代表清沐泽元参赛",
                            "（第一完成人/第一作者；代表清沐泽元参赛"
                        )
                        print("  profile 2.1: patched 数据要素 award")
    save("profile.json", p)

    # 8) _meta.json
    m = load("_meta.json")
    print("  _meta before:", m.get("total_events"))
    # 重算总事件数
    tot = 0
    for f in ("lulili.json", "metaverse.json", "related.json", "base.json", "yimu.json", "honors.json"):
        tot += len(load(f).get("results", []))
    m["total_events"] = tot
    m["updated_at"] = "2026-11-12"
    save("_meta.json", m)
    print("  _meta after:", m["total_events"])

    # 9) 同步到 static/
    for f in ("lulili.json", "metaverse.json", "related.json", "base.json", "yimu.json", "honors.json", "profile.json", "_meta.json"):
        shutil.copy(os.path.join(BASE, f), os.path.join(DST, "static", f))
    print("synced to static/")

if __name__ == "__main__":
    main()
