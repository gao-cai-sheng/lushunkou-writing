"""
抓取临高启明 wiki 元老人物分类页，含分页处理。
每个人物抓取：姓名、wiki链接、简介首段、信息框关键字段。
输出：characters.json + characters.md
"""

import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://lgqm.huijiwiki.com"
START_URL = "https://lgqm.huijiwiki.com/wiki/%E5%88%86%E7%B1%BB:%E5%85%83%E8%80%81"
OUTPUT_DIR = "/Users/gao/Desktop/临高人物库"

INFOBOX_FIELDS = [
    "职务", "职位", "专业", "专长", "出身", "性别", "派系",
    "现任", "军衔", "部门", "单位", "籍贯", "旧时空身份"
]

def get_all_category_links(page):
    """处理分页，收集所有人物链接。"""
    links = []
    current_url = START_URL
    while True:
        page.goto(current_url, wait_until="networkidle")
        anchors = page.query_selector_all(".mw-category a, .mw-category-group a")
        for a in anchors:
            name = a.inner_text().strip()
            href = a.get_attribute("href")
            if href and name:
                links.append({"name": name, "url": BASE_URL + href})
        next_btn = page.query_selector("a:has-text('下一页')")
        if not next_btn:
            break
        next_href = next_btn.get_attribute("href")
        if not next_href:
            break
        current_url = BASE_URL + next_href
        time.sleep(0.5)
    return links

def scrape_character(page, char):
    """访问单个人物页面，提取简介和信息框。"""
    try:
        page.goto(char["url"], wait_until="domcontentloaded", timeout=15000)
    except Exception as e:
        char["error"] = str(e)
        return char

    infobox = {}
    rows = page.query_selector_all(".infobox tr, .wikitable tr, table.infobox tr")
    for row in rows:
        tds = row.query_selector_all("th, td")
        if len(tds) >= 2:
            key = tds[0].inner_text().strip().rstrip("：:")
            val = tds[1].inner_text().strip()
            if key in INFOBOX_FIELDS and val:
                infobox[key] = val

    intro = ""
    paras = page.query_selector_all("#mw-content-text .mw-parser-output > p")
    for p in paras:
        text = p.inner_text().strip()
        if text:
            intro = text
            break

    char["infobox"] = infobox
    char["intro"] = intro
    return char

def to_markdown(characters):
    lines = ["# 临高启明·元老人物库\n",
             f"共 {len(characters)} 名元老\n",
             "---\n"]
    for c in characters:
        lines.append(f"## {c['name']}")
        if c.get("infobox"):
            for k, v in c["infobox"].items():
                lines.append(f"- **{k}**：{v}")
        if c.get("intro"):
            lines.append(f"\n> {c['intro'][:300]}")
        if c.get("error"):
            lines.append(f"⚠️ 抓取失败：{c['error']}")
        lines.append("")
    return "\n".join(lines)

def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
        )
        page = context.new_page()
        page.route("**/*.{png,jpg,jpeg,gif,svg,webp}", lambda r: r.abort())

        print("正在抓取分类页...")
        chars = get_all_category_links(page)
        print(f"找到 {len(chars)} 名元老，开始逐一抓取...")

        for i, c in enumerate(chars, 1):
            print(f"  [{i}/{len(chars)}] {c['name']}")
            scrape_character(page, c)
            time.sleep(0.3)

        browser.close()

    json_path = f"{OUTPUT_DIR}/characters.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(chars, f, ensure_ascii=False, indent=2)

    md_path = f"{OUTPUT_DIR}/characters.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(to_markdown(chars))

    print(f"\n完成！共 {len(chars)} 名元老")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")

if __name__ == "__main__":
    main()
