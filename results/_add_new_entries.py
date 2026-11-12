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

# ===== 新增条目 =====

# 1. 基地揭牌仪式 2026-04-18 → base.json
new_base_entry = {
    "id": "evt-base-official2026",
    "date": "2026-04-18",
    "title": "智慧教育产教基地正式揭牌，「未来学校」样板间对外开放",
    "title_full": "2026年4月18日，华东师范大学上海数字化教育装备工程技术研究中心智慧教育产教基地揭牌仪式在上海市静安区多媒体大厦举行。副校长戴立益、彭浦镇党委书记程凯出席并致辞。基地打造500平方米「未来学校」样板间和超1万平方米专属办公空间，汇聚腾讯教育、Classin、希沃、鑫考股份、钉钉等数十家头部企业。同步揭牌「数智教育产教联盟」和「智慧教育成果孵化空间」。首批孵化产品发布：云痕智能教学一体化平台、数智优学、教育元宇宙未来课堂、星脉智育。",
    "summary": "2026年4月18日，华东师范大学智慧教育产教基地正式揭牌，标志着全国首个深度融合「教育产品×商业地产×金融投资」的实体化、场景化、市场化教育成果交易与发展生态平台落地。基地坐落于静安区多媒体谷，打造500㎡「未来学校」样板间，汇聚数十家头部教育企业，面向全国开放承接参观交流、教师培训、学术会议，并计划建设青少年科普实践基地。",
    "category": "基地建设",
    "sources": [
        {
            "name": "华东师范大学官网",
            "url": "https://www.ecnu.edu.cn/info/1094/72008.htm",
            "date": "2026-04-22"
        },
        {
            "name": "科学网",
            "url": "https://paper.sciencenet.cn/htmlnews/2026/4/563400.shtm",
            "date": "2026-04-21"
        },
        {
            "name": "东方网",
            "url": "https://new.eastday.com/bjzx/20260419/9fa526569e694aec9567d6c6ed893195.html",
            "date": "2026-04-19"
        },
        {
            "name": "看看新闻",
            "url": "https://www.kankanews.com/detail/qMyEAXV9Ky8",
            "date": "2026-04-20"
        }
    ],
    "source_count": 4,
    "type": "event_cluster"
}

# 2. 鲁力立在基地揭牌仪式上的角色（含鲁力立名字）→ lulili.json
new_lulili_entry = {
    "id": "evt-base-luke2026",
    "date": "2026-04-18",
    "title": "鲁力立作为基地负责人，在揭牌仪式上介绍基地功能与孵化产品",
    "title_full": "在华东师范大学智慧教育产教基地揭牌仪式上，基地负责人鲁力立（上海数字化教育装备工程技术研究中心科技转化主任助理）向与会嘉宾介绍基地「自选超市+联合研发+投资融资+示范空间」四位一体运营模式，以及首批四大孵化产品（云痕智能教学一体化平台、数智优学、教育元宇宙未来课堂、星脉智育）。鲁力立团队研发的「教育元宇宙未来课堂」作为首批孵化产品正式发布。",
    "summary": "2026年4月18日，华东师范大学智慧教育产教基地揭牌仪式举行。基地负责人鲁力立向来自全国40余所顶尖中小学代表和30余家行业领军企业的嘉宾，介绍基地功能和首批孵化产品。「教育元宇宙未来课堂」作为鲁力立团队的核心成果，在揭牌仪式上正式发布，标志着该项目从科研走向市场化的重要里程碑。",
    "category": "基地建设",
    "sources": [
        {
            "name": "华东师范大学官网",
            "url": "https://www.ecnu.edu.cn/info/1094/72008.htm",
            "date": "2026-04-22"
        },
        {
            "name": "静安区政府官网",
            "url": "https://www.jingan.gov.cn/rmtzx/003001/20260421/39fc0bce-b91b-4872-8fdf-11b3335896f5.html",
            "date": "2026-04-21"
        }
    ],
    "source_count": 2,
    "type": "event_cluster"
}

# 3. 富桂通战略合作 2026-05-12 → related.json 或 base.json
new_related_entry = {
    "id": "evt-fuguijia2026",
    "date": "2026-05-12",
    "title": "富桂通与华东师范大学达成战略合作，携手共筑智慧教育发展生态",
    "title_full": "基于与树人托管达成的教育场景成熟战略合作经验，富桂通此次携手华东师范大学，是教育领域布局步伐的持续深化，进一步完善「高校科研+企业制造+场景应用」的产教融合生态。富桂通作为黑马企业已入驻智慧教育产教基地。",
    "summary": "2026年5月12日，富桂通与华东师范大学达成战略合作，进一步完善「高校科研+企业制造+场景应用」的产教融合生态。富桂通作为智慧教育产教基地入驻企业，与鲁力立团队及工程中心在智慧教育产品孵化、场景落地等方面开展深度合作。",
    "category": "基地建设",
    "sources": [
        {
            "name": "网易新闻",
            "url": "https://www.163.com/dy/article/KSNOURIH0556CBLT.html",
            "date": "2026-05-12"
        }
    ],
    "source_count": 1,
    "type": "event_cluster"
}

# ===== 写入文件 =====
print("=== 写入新增条目 ===")

# base.json
base = load('base.json')
existing_ids = {r.get('id','') for r in base.get('results', [])}
if new_base_entry['id'] not in existing_ids:
    base['results'].append(new_base_entry)
    base['total'] = len(base['results'])
    save('base.json', base)
    print(f"  ✅ 已添加基地揭牌条目到 base.json (现 {base['total']} 条)")
else:
    print(f"  ⚠️ 基地揭牌条目已存在，跳过")

# lulili.json
lulili = load('lulili.json')
existing_ids = {r.get('id','') for r in lulili.get('results', [])}
if new_lulili_entry['id'] not in existing_ids:
    lulili['results'].append(new_lulili_entry)
    lulili['total'] = len(lulili['results'])
    save('lulili.json', lulili)
    print(f"  ✅ 已添加鲁力立基地揭牌条目到 lulili.json (现 {lulili['total']} 条)")
else:
    print(f"  ⚠️ 鲁力立基地揭牌条目已存在，跳过")

# related.json (或 base.json)
related = load('related.json')
existing_ids = {r.get('id','') for r in related.get('results', [])}
if new_related_entry['id'] not in existing_ids:
    related['results'].append(new_related_entry)
    related['total'] = len(related['results'])
    save('related.json', related)
    print(f"  ✅ 已添加富桂通合作条目到 related.json (现 {related['total']} 条)")
else:
    print(f"  ⚠️ 富桂通合作条目已存在，跳过")

print()
print("=== 完成 ===")
