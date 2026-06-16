"""抓取穿越者和意外穿越者两个分类"""
import json, time
from playwright.sync_api import sync_playwright

BASE_URL = "https://lgqm.huijiwiki.com"
OUTPUT_DIR = "/Users/gao/Desktop/临高人物库"

INFOBOX_FIELDS = ["职务","职位","专业","专长","出身","性别","派系","现任","军衔","部门","单位","籍贯","旧时空身份"]

CATEGORIES = [
    ("穿越者", "https://lgqm.huijiwiki.com/wiki/%E5%88%86%E7%B1%BB:%E7%A9%BF%E8%B6%8A%E8%80%85", "travellers"),
    ("意外穿越者", "https://lgqm.huijiwiki.com/wiki/%E5%88%86%E7%B1%BB:%E6%84%8F%E5%A4%96%E7%A9%BF%E8%B6%8A%E8%80%85", "accidental_travellers"),
]

def get_links(page, start_url):
    links = []
    current = start_url
    while True:
        page.goto(current, wait_until="networkidle")
        for a in page.query_selector_all(".mw-category a, .mw-category-group a"):
            name = a.inner_text().strip()
            href = a.get_attribute("href")
            if href and name:
                links.append({"name": name, "url": BASE_URL + href})
        nxt = page.query_selector("a:has-text('下一页')")
        if not nxt:
            break
        nh = nxt.get_attribute("href")
        if not nh:
            break
        current = BASE_URL + nh
        time.sleep(0.5)
    return links

def scrape_one(page, char):
    try:
        page.goto(char["url"], wait_until="domcontentloaded", timeout=15000)
    except Exception as e:
        char["error"] = str(e); return char
    infobox = {}
    for row in page.query_selector_all(".infobox tr, .wikitable tr, table.infobox tr"):
        tds = row.query_selector_all("th, td")
        if len(tds) >= 2:
            k = tds[0].inner_text().strip().rstrip("：:")
            v = tds[1].inner_text().strip()
            if k in INFOBOX_FIELDS and v:
                infobox[k] = v
    intro = ""
    for p in page.query_selector_all("#mw-content-text .mw-parser-output > p"):
        t = p.inner_text().strip()
        if t:
            intro = t; break
    char["infobox"] = infobox
    char["intro"] = intro
    return char

def to_md(chars, title):
    lines = [f"# {title}\n", f"共 {len(chars)} 人\n", "---\n"]
    for c in chars:
        lines.append(f"## {c['name']}")
        for k, v in c.get("infobox", {}).items():
            lines.append(f"- **{k}**：{v}")
        if c.get("intro"):
            lines.append(f"\n> {c['intro'][:300]}")
        lines.append("")
    return "\n".join(lines)

def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="zh-CN")
        page = ctx.new_page()
        page.route("**/*.{png,jpg,jpeg,gif,svg,webp}", lambda r: r.abort())

        for cname, url, fname in CATEGORIES:
            print(f"抓取{cname}...")
            chars = get_links(page, url)
            print(f"找到 {len(chars)} 人，抓取中...")
            for i, c in enumerate(chars, 1):
                print(f"  [{i}/{len(chars)}] {c['name']}")
                scrape_one(page, c)
                time.sleep(0.3)
            with open(f"{OUTPUT_DIR}/{fname}.json", "w", encoding="utf-8") as f:
                json.dump(chars, f, ensure_ascii=False, indent=2)
            with open(f"{OUTPUT_DIR}/{fname}.md", "w", encoding="utf-8") as f:
                f.write(to_md(chars, f"临高启明·{cname}"))
            print(f"完成！{cname} {len(chars)} 人 → {fname}.json/md")

        browser.close()

if __name__ == "__main__":
    main()
