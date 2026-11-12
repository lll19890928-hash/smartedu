#!/usr/bin/env python3
"""
学术动态监控系统 - 后端服务 v2.0
双层架构：优先从磁盘 JSON 缓存加载，实时搜索作为补充
"""
import json
import os
import time
import threading
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, send_file, make_response
from io import BytesIO

app = Flask(__name__, static_folder="static", static_url_path="/static")


def _load_dotenv(path=None):
    """极简 .env 加载：KEY=VALUE 逐行读取，已存在的环境变量不覆盖"""
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


_load_dotenv()

# ============ 配置 ============
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

SEARCH_TOPICS = [
    {"id": "profile",   "name": "鲁力立个人全貌",   "icon": "📋", "color": "#a18cd1"},
    {"id": "lulili",   "name": "鲁力立个人动态",   "icon": "👤", "color": "#667eea"},
    {"id": "metaverse", "name": "教育元宇宙未来课堂", "icon": "🌐", "color": "#f093fb"},
    {"id": "base",      "name": "智慧教育产教基地",   "icon": "🏫", "color": "#4facfe"},
    {"id": "yimu",      "name": "壹幕工作室学生成果", "icon": "🎬", "color": "#00838f"},
    {"id": "related",   "name": "关联机构动态",       "icon": "🔗", "color": "#43e97b"},
    {"id": "honors",    "name": "荣誉与成果",         "icon": "🏆", "color": "#fa709a"},
]

# 内存缓存（减少磁盘 IO）
_mem_cache = {}
_mem_cache_ts = 0
_MEM_CACHE_TTL = 30  # 秒
_data_version = 0  # 数据版本号，每次 reload 递增，用于前端缓存破除


# ============ 导出功能 ============
def _build_excel_bytes(topic_id, category=None):
    """将主题数据导出为 Excel 字节流"""
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    
    cache = _get_cache()
    if topic_id not in cache:
        return None
    
    data = cache[topic_id]
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # 删除默认 sheet
    
    def _add_sheet(ws, rows):
        """往 sheet 写数据，带基础样式"""
        thin = Side(style="thin", color="CCCCCC")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)
        header_fill = PatternFill("solid", fgColor="366092")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        for r_idx, row in enumerate(rows):
            for c_idx, val in enumerate(row):
                cell = ws.cell(row=r_idx+1, column=c_idx+1, value=val)
                cell.border = border
                cell.alignment = Alignment(wrap_text=True, vertical="center")
                if r_idx == 0:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center", vertical="center")
        # 自适应列宽（简单版）
        for col in ws.columns:
            max_len = max((len(str(cell.value or "")) for cell in col), default=10)
            ws.column_dimensions[openpyxl.utils.get_column_letter(col[0].column)].width = min(max_len + 4, 50)
        return ws
    
    # ---------- profile（个人全貌） ----------
    if topic_id == "profile":
        results = data.get("results", [])
        if category and category != "all":
            results = [b for b in results if b.get("id") == category or b.get("title", "").find(category) >= 0]
        
        for block in results:
            sheet_name = block.get("title", "未命名")[:30]  # Excel sheet名最长31字符
            ws = wb.create_sheet(sheet_name)
            rows = [["字段", "内容", "链接"]]
            for subsec in block.get("subsections", []):
                rows.append([f"── {subsec.get('title', '')} ──", "", ""])
                for item in subsec.get("items", []):
                    rows.append([
                        item.get("label", ""),
                        item.get("value", ""),
                        item.get("link", "")
                    ])
            _add_sheet(ws, rows)
    
    # ---------- yimu（壹幕工作室） ----------
    elif topic_id == "yimu":
        yimu_data = data.get("results", [])
        # yimu.json 结构是数组，每个元素是一条记录
        # 按 category 分组
        cat_map = {}
        for rec in yimu_data:
            cat = rec.get("category", "其他")
            cat_map.setdefault(cat, []).append(rec)
        
        cats_to_export = [category] if category and category != "all" else list(cat_map.keys())
        for cat in cats_to_export:
            records = cat_map.get(cat, [])
            if not records:
                continue
            ws = wb.create_sheet(cat[:30])
            # 动态表头：取第一条记录的所有键
            headers = list(records[0].keys()) if records else []
            rows = [headers]
            for rec in records:
                rows.append([rec.get(h, "") for h in headers])
            _add_sheet(ws, rows)
    
    # ---------- 其他主题（lulili / metaverse / base / related / honors） ----------
    else:
        results = data.get("results", [])
        ws = wb.create_sheet(SEARCH_TOPICS_dict.get(topic_id, {}).get("name", topic_id)[:30])
        rows = [["标题", "链接", "摘要", "日期", "来源"]]
        for item in results:
            rows.append([
                item.get("title", ""),
                item.get("link", ""),
                item.get("snippet", ""),
                item.get("date", ""),
                item.get("source", "")
            ])
        _add_sheet(ws, rows)
    
    # 如果没有任何 sheet，创建一个空的
    if not wb.sheetnames:
        wb.create_sheet("无数据")
    
    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()


def _build_word_bytes(topic_id, category=None):
    """将主题数据导出为 Word 字节流"""
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    
    cache = _get_cache()
    if topic_id not in cache:
        return None
    
    data = cache[topic_id]
    doc = Document()
    
    # 标题
    heading = doc.add_heading(SEARCH_TOPICS_dict.get(topic_id, {}).get("name", topic_id), level=0)
    
    # ---------- profile ----------
    if topic_id == "profile":
        results = data.get("results", [])
        if category and category != "all":
            results = [b for b in results if b.get("id") == category or b.get("title", "").find(category) >= 0]
        
        for block in results:
            doc.add_heading(block.get("title", ""), level=1)
            for subsec in block.get("subsections", []):
                doc.add_heading(subsec.get("title", ""), level=2)
                for item in subsec.get("items", []):
                    p = doc.add_paragraph()
                    p.add_run(f"{item.get('label', '')}：").bold = True
                    p.add_run(str(item.get("value", "")))
                    if item.get("link"):
                        p.add_run(f"  🔗 {item.get('link')}")
    
    # ---------- yimu ----------
    elif topic_id == "yimu":
        yimu_data = data.get("results", [])
        cat_map = {}
        for rec in yimu_data:
            cat = rec.get("category", "其他")
            cat_map.setdefault(cat, []).append(rec)
        
        cats_to_export = [category] if category and category != "all" else list(cat_map.keys())
        for cat in cats_to_export:
            records = cat_map.get(cat, [])
            if not records:
                continue
            doc.add_heading(cat, level=1)
            for rec in records:
                p = doc.add_paragraph(style="List Bullet")
                # 取主要字段显示
                summary = " | ".join(str(rec.get(k, "")) for k in ["project", "name", "title", "award", "year"] if rec.get(k))
                p.add_run(summary or str(rec))
    
    # ---------- 其他主题 ----------
    else:
        results = data.get("results", [])
        doc.add_heading("搜索结果", level=1)
        for item in results:
            p = doc.add_paragraph(style="List Number")
            p.add_run(item.get("title", "")).bold = True
            if item.get("date"):
                p.add_run(f"  [{item.get('date')}]")
            if item.get("snippet"):
                doc.add_paragraph(item.get("snippet", ""), style="Body Text")
            if item.get("link"):
                doc.add_paragraph(f"链接：{item.get('link')}", style="Intense Quote")
    
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.getvalue()


# 构建 topic id→name 映射（给导出函数用）
SEARCH_TOPICS_dict = {t["id"]: t for t in SEARCH_TOPICS}


def _load_cache_file(topic_id):
    """从磁盘加载单个主题缓存"""
    filepath = os.path.join(RESULTS_DIR, f"{topic_id}.json")
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[缓存] 读取失败 {topic_id}: {e}")
        return None


def _load_all_cache():
    """加载所有主题缓存到内存"""
    global _mem_cache, _mem_cache_ts
    _mem_cache = {}
    for t in SEARCH_TOPICS:
        data = _load_cache_file(t["id"])
        if data:
            _mem_cache[t["id"]] = data
    global _data_version
    _data_version += 1
    _mem_cache_ts = time.time()
    return _mem_cache


def _get_cache():
    """获取缓存（带 TTL）"""
    global _mem_cache_ts
    if time.time() - _mem_cache_ts > _MEM_CACHE_TTL:
        _load_all_cache()
    return _mem_cache


# ============ API 路由 ============

@app.route("/")
def index():
    return send_from_directory("static", "dashboard.html")


@app.route("/api/topics")
def api_topics():
    return jsonify({"topics": SEARCH_TOPICS})


@app.route("/api/search")
def api_search():
    """返回搜索结果（从缓存加载）"""
    topic_id = request.args.get("topic", "all")
    force = request.args.get("force", "0") == "1"

    cache = _get_cache()

    if topic_id == "all":
        # 返回所有主题
        result = {}
        for t in SEARCH_TOPICS:
            tid = t["id"]
            if tid in cache:
                result[tid] = cache[tid]
            else:
                result[tid] = {
                    "topic": {k: v for k, v in t.items()},
                    "results": [],
                    "total": 0,
                    "searched_at": ""
                }
        return jsonify(result)
    else:
        if topic_id in cache:
            return jsonify(cache[topic_id])
        # 未知主题
        return jsonify({"error": f"Unknown topic: {topic_id}"}), 404


@app.route("/api/search_single", methods=["GET"])
def api_search_single():
    """自定义搜索（尽力尝试实时搜索）"""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Missing query", "results": []}), 400

    results = []
    search_source = "none"

    # 尝试 DuckDuckGo
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            ddg_results = list(ddgs.text(query, max_results=5))
            for r in ddg_results:
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "date": "",
                    "source": "DuckDuckGo",
                    "type": "web"
                })
            search_source = "DuckDuckGo"
    except Exception:
        pass

    # 返回结果（即使为空）
    return jsonify({
        "query": query,
        "results": results,
        "source": search_source,
        "note": "实时搜索可能不可用，建议通过 WorkBuddy 说「更新学术动态监控缓存」来获取最新结果。"
    })


@app.route("/api/cache/reload")
def api_cache_reload():
    """强制从磁盘重新加载缓存"""
    _load_all_cache()
    return jsonify({"status": "ok", "topics_loaded": len(_mem_cache), "version": _data_version})


@app.route("/api/version")
def api_version():
    """返回当前数据版本号（前端用于判断是否需要刷新）"""
    return jsonify({"version": _data_version, "cache_ts": _mem_cache_ts})


@app.route("/papers")
def papers_page():
    """论文原文库页面"""
    return send_from_directory("static", "papers.html")


@app.route("/api/export")
def api_export():
    """导出主题为 Excel 或 Word"""
    topic_id = request.args.get("topic", "")
    category = request.args.get("category", "all")
    fmt = request.args.get("format", "xlsx")  # xlsx 或 docx
    
    if not topic_id:
        return jsonify({"error": "Missing topic parameter"}), 400
    
    if fmt not in ("xlsx", "docx"):
        return jsonify({"error": "format must be xlsx or docx"}), 400
    
    cache = _get_cache()
    if topic_id not in cache:
        return jsonify({"error": f"Topic {topic_id} not found in cache"}), 404
    
    try:
        if fmt == "xlsx":
            buf = _build_excel_bytes(topic_id, category)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ext = ".xlsx"
        else:
            buf = _build_word_bytes(topic_id, category)
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ext = ".docx"
        
        if buf is None:
            return jsonify({"error": "Export failed, no data"}), 500
        
        topic_name = SEARCH_TOPICS_dict.get(topic_id, {}).get("name", topic_id)
        filename = f"{topic_name}_{category}{ext}"
        # 清理文件名中的特殊字符
        import re
        filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
        
        resp = make_response(buf)
        resp.headers["Content-Type"] = mime
        resp.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
        return resp
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500


# ============ 独立版 HTML 动态生成 ============
@app.route("/standalone")
def standalone():
    """
    动态生成含最新数据的独立版 HTML。
    每次访问都嵌入服务器当前最新数据，下载后发给他人可离线使用。
    """
    import io

    # 1. 读取所有最新 JSON 数据
    cache = _get_cache()
    embedded = {}

    for t in SEARCH_TOPICS:
        tid = t["id"]
        embedded[tid] = cache.get(tid, {"results": [], "total": 0, "stats": {}})

    # yimu 数据（在 static/ 下）
    yimu_path = os.path.join(app.static_folder, "yimu.json")
    try:
        if os.path.exists(yimu_path):
            with open(yimu_path, encoding="utf-8") as f:
                embedded["yimu"] = json.load(f)
        else:
            embedded["yimu"] = {"results": [], "stats": {}}
    except Exception:
        embedded["yimu"] = {"results": [], "stats": {}}

    # 写入更新时间
    embedded["_meta"] = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "version": _data_version
    }

    # 2. 读取 dashboard.html 模板
    html_path = os.path.join(app.static_folder, "dashboard.html")
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # 3. 将数据嵌入 HTML：在 </head> 前插入 <script> 块
    data_js = json.dumps(embedded, ensure_ascii=False, indent=2)
    script_block = (
        '<script>\n'
        '// ════════════════════════════════════════════\n'
        '// 独立版嵌入数据 — 由 /standalone 路由自动生成\n'
        '// 上次数据更新时间：' + embedded["_meta"]["updateTime"] + '\n'
        '// ════════════════════════════════════════════\n'
        'var EMBEDDED_DATA = ' + data_js + ';\n'
        '</script>\n'
    )

    # 在 </head> 前插入（确保在使用前定义）
    html = html.replace('</head>', script_block + '</head>', 1)

    # 4. 强制编码声明放在 <head> 最前面（防御性修复）
    html = html.replace(
        '<head>',
        '<head>\n  <meta charset="UTF-8">\n  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">',
        1
    )

    # 5. 返回 HTML，触发下载
    buf = io.BytesIO(html.encode("utf-8"))
    resp = make_response(buf.getvalue())
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["Content-Disposition"] = (
        "attachment; filename*=UTF-8''%E9%BO%90%E5%8A%9B%E7%AB%8B%E5%AD%A6%E6%9C%AF%E5%8A%A8%E6%80%81_%E7%8B%AC%E7%AB%8B%E7%89%88.html"
    )
    return resp


@app.route("/api/global_search")
def api_global_search():
    """全局关键词检索：在所有主题中搜索关键词"""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"results": [], "total": 0})
    
    cache = _get_cache()
    results = []
    
    for topic_id, topic_data in cache.items():
        topic_info = SEARCH_TOPICS_dict.get(topic_id, {})
        
        # profile 数据：在 value 和 label 中搜索
        if topic_id == "profile":
            for block in topic_data.get("results", []):
                block_title = block.get("title", "")
                for subsec in block.get("subsections", []):
                    subsec_title = subsec.get("title", "")
                    for item in subsec.get("items", []):
                        val = f"{item.get('label', '')} {item.get('value', '')} {item.get('link', '')}"
                        if q in val:
                            results.append({
                                "topic_id": topic_id,
                                "topic_name": topic_info.get("name", topic_id),
                                "block": block_title,
                                "section": subsec_title,
                                "label": item.get("label", ""),
                                "value": item.get("value", ""),
                                "match": f"{block_title} > {subsec_title} > {item.get('label', '')}"
                            })
        
        # yimu 数据：在所有字段中搜索
        elif topic_id == "yimu":
            for rec in topic_data.get("results", []):
                val = " ".join(str(v) for v in rec.values())
                if q in val:
                    results.append({
                        "topic_id": topic_id,
                        "topic_name": topic_info.get("name", topic_id),
                        "category": rec.get("category", ""),
                        "project": rec.get("project", ""),
                        "name": rec.get("name", ""),
                        "year": rec.get("year", ""),
                        "match": f"{rec.get('category', '')} > {rec.get('project', '')}"
                    })
        
        # 其他主题：在 title 和 snippet 中搜索
        else:
            for item in topic_data.get("results", []):
                val = f"{item.get('title', '')} {item.get('snippet', '')}"
                if q in val:
                    results.append({
                        "topic_id": topic_id,
                        "topic_name": topic_info.get("name", topic_id),
                        "title": item.get("title", ""),
                        "date": item.get("date", ""),
                        "link": item.get("link", ""),
                        "match": item.get("title", "")
                    })
    
    return jsonify({"results": results, "total": len(results), "query": q})


# ============ 刷新接口 ============

@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """触发数据刷新（搜索全网最新动态）"""
    import threading
    refresh_flag = os.path.join(RESULTS_DIR, "_refresh_request.json")
    payload = {
        "requested_at": datetime.now().isoformat(),
        "status": "pending",
        "results": []
    }
    with open(refresh_flag, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    def _do_refresh():
        try:
            import urllib.request, urllib.parse, re, time as _time
            all_results = []
            queries = [
                "鲁力立 华东师范大学 副教授",
                "鲁力立 教育元宇宙 未来课堂",
                "鲁力立 壹幕工作室",
                "鲁力立 智慧教育 产教基地",
            ]
            for q in queries:
                _time.sleep(2)
                try:
                    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}&count=5"
                    req = urllib.request.Request(url, headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Accept-Language": "zh-CN,zh;q=0.9"
                    })
                    resp = urllib.request.urlopen(req, timeout=10)
                    html = resp.read().decode("utf-8", errors="ignore")
                    blocks = re.split(r'class="b_algo"', html)
                    for block in blocks[1:]:
                        urls = re.findall(r'<a[^>]*href="(https?://[^"]+)"', block)
                        url = urls[0] if urls else ""
                        if not url or "bing.com" in url or "microsoft.com" in url:
                            continue
                        titles = re.findall(r'<a[^>]*>(.*?)</a>', block)
                        title = ""
                        for t in titles:
                            clean = re.sub(r"<[^>]+>", "", t).strip()
                            if len(clean) > len(title) and len(clean) > 5:
                                title = clean
                        snippets = re.findall(r'class="b_caption"[^>]*>(.*?)(?:</div>|$)', block)
                        snippet = ""
                        for s in snippets:
                            s = re.sub(r"<[^>]+>", "", s)
                            s = re.sub(r"\s+", " ", s).strip()
                            if len(s) > len(snippet):
                                snippet = s
                        if title and url:
                            all_results.append({"title": title, "url": url, "snippet": snippet[:200], "query": q})
                except Exception:
                    pass

            payload["status"] = "done"
            payload["results"] = all_results
            payload["finished_at"] = datetime.now().isoformat()
            with open(refresh_flag, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            payload["status"] = "error"
            payload["error"] = str(e)
            with open(refresh_flag, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

    t = threading.Thread(target=_do_refresh, daemon=True)
    t.start()
    return jsonify({"status": "started", "message": "后台搜索已启动，请稍候"})


@app.route("/api/refresh/status")
def api_refresh_status():
    """查询刷新状态"""
    refresh_flag = os.path.join(RESULTS_DIR, "_refresh_request.json")
    if os.path.exists(refresh_flag):
        try:
            with open(refresh_flag, "r", encoding="utf-8") as f:
                return jsonify(json.load(f))
        except Exception:
            pass
    return jsonify({"status": "idle"})


# 同时更新 /api/meta 以支持更新时间
@app.route("/api/meta")
def api_meta():
    """返回缓存元信息（含上次更新时间）"""
    meta_path = os.path.join(RESULTS_DIR, "_meta.json")
    meta = {"updated_at": "", "topics": {}}
    latest_ts = 0
    for t in SEARCH_TOPICS:
        fp = os.path.join(RESULTS_DIR, f"{t['id']}.json")
        if os.path.exists(fp):
            ts = os.path.getmtime(fp)
            if ts > latest_ts:
                latest_ts = ts
            meta["topics"][t["id"]] = {
                "updated_at": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M"),
                "total": (_mem_cache.get(t["id"], {}).get("total", 0) if _mem_cache else 0)
            }
    if latest_ts > 0:
        meta["updated_at"] = datetime.fromtimestamp(latest_ts).strftime("%Y-%m-%d %H:%M")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if saved.get("updated_at", "") > meta["updated_at"]:
                    meta["updated_at"] = saved["updated_at"]
        except Exception:
            pass
    return jsonify(meta)


# ============ AI 对话代理 ============

# 密钥从环境变量读取（也可写在同目录的 .env 文件里），不要把真实 Key 提交进仓库
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.environ.get("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """代理 DeepSeek API 请求，绕过浏览器 CORS 限制"""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": {"message": "无效的请求体"}}), 400

    if not DEEPSEEK_API_KEY:
        return jsonify({"error": {"message": "未配置 DEEPSEEK_API_KEY，请在环境变量或 .env 中设置"}}), 500

    # 构建请求体
    payload = {
        "model": "deepseek-chat",
        "messages": data.get("messages", []),
        "temperature": data.get("temperature", 0.3),
        "max_tokens": data.get("max_tokens", 2000)
    }

    req = urllib.request.Request(
        DEEPSEEK_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
    )

    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode("utf-8"))
        return jsonify(result)
    except urllib.error.HTTPError as e:
        error_body = {}
        try:
            error_body = json.loads(e.read().decode("utf-8"))
        except Exception:
            error_body = {"message": f"HTTP {e.code}: {e.reason}"}
        return jsonify({"error": error_body, "http_status": e.code}), e.code
    except Exception as e:
        return jsonify({"error": {"message": f"网络错误: {str(e)}"}}), 500


@app.after_request
def disable_cache(response):
    """禁止浏览器缓存所有响应，确保每次都是最新数据"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ============ 启动 ============
if __name__ == "__main__":
    print("=" * 62)
    print("   学术动态监控系统  v2.0")
    print("   监控：鲁力立 | 教育元宇宙未来课堂 | 智慧教育产教基地")
    print("=" * 62)

    # 启动时加载缓存
    _load_all_cache()
    total = sum(v.get("total", 0) for v in _mem_cache.values())
    topics_loaded = len(_mem_cache)

    for t in SEARCH_TOPICS:
        count = _mem_cache.get(t["id"], {}).get("total", 0)
        bar = "#" * min(count, 20)
        print(f"   {t['icon']} {t['name']:16s} {count:3d} 条  {bar}")

    print(f"\n   缓存已加载：{topics_loaded}/6 个主题，共 {total} 条记录")
    print(f"   访问地址：http://localhost:8890")
    print("=" * 62)

    app.run(host="0.0.0.0", port=8890, debug=False)
