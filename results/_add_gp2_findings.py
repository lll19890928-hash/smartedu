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

def append_if_new(data_list, new_item, key='id'):
    existing = {r.get(key, '') for r in data_list}
    if new_item.get(key, '') not in existing:
        data_list.append(new_item)
        return True
    return False

print("=== 写入 general-purpose-2 搜索发现 ===\n")

# 1. 光明日报转化门诊 2024-10-31 → lulili.json
entry_1 = {
    "id": "evt-transform-clinic2024",
    "date": "2024-10-31",
    "title": "鲁力立携「教育元宇宙未来课堂」项目参加华东师大科技成果转化「门诊」",
    "title_full": "2024年10月31日，《光明日报》头版报道华东师范大学设立科技成果转化「门诊」。鲁力立作为教育信息技术学系高级工程师，带着「教育元宇宙未来课堂」项目资料参加问诊，表示：「给成果『问诊』！这是我的『教育元宇宙未来课堂』项目资料。成果出来后，很多来考察的，但我也不知道应该跟谁合作。听说学校开了科技成果转化『门诊』，我立刻预约了！刚才聊了一个多小时，思路一下子打开了！」该项目在2022年世界人工智能大会（WAIC）上首次发布后获广泛关注，入选2022年WAIC《产业元宇宙创新应用案例集》、上海教博会数字化转型应用标杆案例等。",
    "summary": "2024年10月，华东师范大学设立科技成果转化「门诊」，解决科研人员「不敢转、不想转、不会转」的问题。鲁力立携「教育元宇宙未来课堂」项目参加问诊，该项目已在普陀区教育学院附属学校落地应用，但因经验不足遇阻。专家们用了一个多小时，从多个角度提供了详细、规范、多元的转化方案。两次门诊共19个项目参与深度问诊，5个项目已遴选进入学校概念验证中心。",
    "category": "社会服务",
    "sources": [
        {
            "name": "华东师范大学官网（转载《光明日报》头版）",
            "url": "https://www.ecnu.edu.cn/info/1094/67865.htm",
            "date": "2024-10-31"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# 2. 鲁力立著作《AIGC重塑数字媒体创作》2026-04 → lulili.json
entry_2 = {
    "id": "pub-aigc-book2026",
    "date": "2026-04-01",
    "title": "鲁力立出版著作《AIGC重塑数字媒体创作》",
    "title_full": "2026年4月，鲁力立著作《AIGC重塑数字媒体创作》由上海高校智库华东师范大学数字文化发展协同创新中心出版上架。该书系统阐述AIGC技术在数字媒体创作领域的应用与影响，在新华书店、淘宝等渠道销售。",
    "summary": "2026年4月，鲁力立所著《AIGC重塑数字媒体创作》正式出版上架，由上海高校智库华东师范大学数字文化发展协同创新中心出版。该书是鲁力立在AIGC与数字媒体交叉领域的重要学术成果，标志着其在AI教育应用方向的持续深耕。",
    "category": "学术成果",
    "sources": [
        {
            "name": "新华书店",
            "url": "https://item.xhsd.com/items/110000104856697",
            "date": "2026-04-01"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# 3. 南京师范大学专题讲座 2026-05-19 → lulili.json
entry_3 = {
    "id": "evt-njnu-lecture2026",
    "date": "2026-05-19",
    "title": "鲁力立应邀赴南京师范大学环境学院作「AI赋能一流本科教育」专题讲座",
    "title_full": "2026年5月19日，鲁力立应邀赴南京师范大学环境学院，作「AI赋能一流本科教育」专题讲座。讲座聚焦「教、学、研、用」四大核心场景，强调「提问沟通力、人机协作力、批判思维力」三大核心能力，分享AI技术在本科教育中的创新应用实践。",
    "summary": "2026年5月19日，鲁力立应邀赴南京师范大学环境学院作专题讲座，主题为「AI赋能一流本科教育」。讲座围绕AI技术在教育教学全链条中的应用展开，重点探讨如何培养学生的AI时代核心竞争力，是鲁力立在AI+教育领域学术影响力的持续扩展。",
    "category": "学术会议",
    "sources": [
        {
            "name": "南京师范大学环境学院官网",
            "url": "https://env.njnu.edu.cn/info/1028/15433.htm",
            "date": "2026-05-19"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# 4. UNESCO奖项 2025-10-27 → honors.json 和 lulili.json
entry_4_honors = {
    "id": "award-unesco2025",
    "date": "2025-10-27",
    "title": "「教育元宇宙未来课堂」获联合国教科文组织「智慧学习生态系统优秀案例奖」",
    "title_full": "2025年10月27日，在「2025数字化终身学习国际会议」上，鲁力立带领团队打造的「面向基础教育的教育元宇宙未来课堂」项目获评「智慧学习生态系统优秀案例奖」。该奖项由联合国教科文组织终身学习研究所（UIL）和联合国教科文组织教育信息技术研究所（UNESCO IITE）联合颁发，标志着项目获得国际权威认可。",
    "summary": "2025年10月，鲁力立带领团队打造的「面向基础教育的教育元宇宙未来课堂」项目，在联合国教科文组织支持的「2025数字化终身学习国际会议」上获评「智慧学习生态系统优秀案例奖」，这是该项目获得的最高国际认可。",
    "category": "荣誉奖项",
    "sources": [
        {
            "name": "华东师范大学上海数字化教育装备工程技术研究中心官网",
            "url": "https://ercdee.ecnu.edu.cn/07/0f/c16571a722703/page.htm",
            "date": "2025-10-27"
        }
    ],
    "source_count": 1,
    "type": "article"
}

entry_4_lulili = {
    "id": "award-unesco2025-lulili",
    "date": "2025-10-27",
    "title": "鲁力立带领团队获联合国教科文组织「智慧学习生态系统优秀案例奖」",
    "title_full": "2025年10月27日，在「2025数字化终身学习国际会议」上，鲁力立带领团队打造的「面向基础教育的教育元宇宙未来课堂」项目获评「智慧学习生态系统优秀案例奖」。该奖项由联合国教科文组织终身学习研究所（UIL）和联合国教科文组织教育信息技术研究所（UNESCO IITE）联合颁发。",
    "summary": "2025年10月，鲁力立带领团队项目获联合国教科文组织「智慧学习生态系统优秀案例奖」，是其在教育元宇宙领域的国际学术影响力的重要里程碑。",
    "category": "荣誉奖项",
    "sources": [
        {
            "name": "华东师范大学上海数字化教育装备工程技术研究中心官网",
            "url": "https://ercdee.ecnu.edu.cn/07/0f/c16571a722703/page.htm",
            "date": "2025-10-27"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# 5. 壹生万幕公司 → related.json
entry_5 = {
    "id": "corp-yishengwanmu2026",
    "date": "2026-04-18",
    "title": "壹生万幕（上海）教育科技有限公司作为首批孵化企业入驻智慧教育产教基地",
    "title_full": "壹生万幕（上海）教育科技有限公司，法定代表人鲁力立，持股90%，是华东师范大学智慧教育产教基地首批重点孵化企业之一。在2026年4月18日基地揭牌仪式上获颁牌匾。公司聚焦教育影视内容创制与AIGC教育应用，与壹幕工作室形成「学术+产业」双轮驱动格局。",
    "summary": "壹生万幕（上海）教育科技有限公司是鲁力立创办的产教融合企业，作为华东师范大学智慧教育产教基地首批重点孵化企业，在2026年4月18日揭牌仪式上正式获颁牌匾，标志着鲁力立团队的成果从科研走向产业化落地。",
    "category": "创业动态",
    "sources": [
        {
            "name": "爱企查",
            "url": "https://aiqicha.baidu.com/human_lTM-TogKuTw7EhRJL5zQ**9ekic2Lq6WgH1Oa4mlwnn",
            "date": "2026-04-18"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# 6. 经济日报报道 2026-04-20 → related.json
entry_6 = {
    "id": "article-jingjiribao2026",
    "date": "2026-04-20",
    "title": "经济日报报道：华东师范大学打造全国首个面向未来的智慧教育产品交易与发展生态平台",
    "title_full": "2026年4月20日，《经济日报》报道华东师范大学智慧教育产教基地揭牌，打造全国首个深度融合「教育产品×商业地产×金融投资」的实体化、场景化、市场化教育成果交易与发展生态平台。报道未提及鲁力立姓名，但确认基地首批孵化产品包含「教育元宇宙未来课堂」。",
    "summary": "2026年4月20日，《经济日报》报道华东师范大学智慧教育产教基地揭牌。基地打造500㎡「未来学校」样板间，汇聚数十家头部教育企业，首批孵化产品包括鲁力立团队的「教育元宇宙未来课堂」。",
    "category": "基地建设",
    "sources": [
        {
            "name": "经济日报",
            "url": "https://www.jingjiribao.cn/static/detail.jsp?id=651186",
            "date": "2026-04-20"
        }
    ],
    "source_count": 1,
    "type": "article"
}

# ===== 写入文件 =====
added = []

# lulili.json：1,2,3,4_lulili
lulili = load('lulili.json')
for e in [entry_1, entry_2, entry_3, entry_4_lulili]:
    if append_if_new(lulili['results'], e):
        added.append(f"  ✅ lulili.json: {e['title'][:40]}")
lulili['total'] = len(lulili['results'])
save('lulili.json', lulili)

# honors.json：4_honors
honors = load('honors.json')
if append_if_new(honors['results'], entry_4_honors):
    added.append(f"  ✅ honors.json: {entry_4_honors['title'][:40]}")
honors['total'] = len(honors['results'])
save('honors.json', honors)

# related.json：5,6
related = load('related.json')
for e in [entry_5, entry_6]:
    if append_if_new(related['results'], e):
        added.append(f"  ✅ related.json: {e['title'][:40]}")
related['total'] = len(related['results'])
save('related.json', related)

print('\n'.join(added))
print(f"\n=== 完成，共添加 {len(added)} 条 ===")
print(f"  lulili.json 现共 {lulili['total']} 条")
print(f"  honors.json 现共 {honors['total']} 条")
print(f"  related.json 现共 {related['total']} 条")
