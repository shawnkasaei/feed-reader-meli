import json
import re
import requests
import datetime
import xml.etree.ElementTree as ET

from pathlib import Path
from email.utils import parsedate_to_datetime


BASE = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE / "Config" / "sources.json"
OUTPUT_DIR = BASE / "Content"

TEHRAN_TZ = datetime.timezone(datetime.timedelta(hours=3, minutes=30))


# ---------- FETCH ----------
def fetch(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


# ---------- CLEAN ----------
def clean_html(text):
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


# ---------- DATE ----------
def to_tehran(dt):
    return dt.astimezone(TEHRAN_TZ).strftime("%a, %d %b %Y %H:%M:%S +0330")


def normalize_date(d):
    try:
        return parsedate_to_datetime(d)
    except:
        return datetime.datetime.now(TEHRAN_TZ)


# ---------- TELEGRAM ----------
def parse_telegram(html):
    blocks = re.findall(r'tgme_widget_message_bubble[\s\S]*?</div>\s*</div>', html)

    items = []

    for b in blocks:
        text_match = re.search(r'tgme_widget_message_text[^>]*>([\s\S]*?)</div>', b)
        time_match = re.search(r'<time[^>]*datetime="([^"]+)"', b)

        if not text_match or not time_match:
            continue

        text = clean_html(text_match.group(1))

        if not text:
            continue

        utc_dt = datetime.datetime.fromisoformat(time_match.group(1))

        items.append({
            "title": text,
            "date": to_tehran(utc_dt)
        })

    return items


# ---------- RSS ----------
def parse_rss(xml):
    items = []

    for item in re.findall(r"<item>([\s\S]*?)</item>", xml):
        t = re.search(r"<title>([\s\S]*?)</title>", item)
        d = re.search(r"<pubDate>([\s\S]*?)</pubDate>", item)

        if not t or not d:
            continue

        try:
            dt = parsedate_to_datetime(d.group(1))
            items.append({
                "title": clean_html(t.group(1)),
                "date": to_tehran(dt)
            })
        except:
            pass

    return items


# ---------- XML ----------
def build_xml(items, title):
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")

    ET.SubElement(channel, "title").text = title

    for i, item in enumerate(items, 1):
        node = ET.SubElement(channel, "item")

        ET.SubElement(node, "title").text = item["title"]
        ET.SubElement(node, "pubDate").text = item["date"]

        ET.SubElement(node, "guid").text = str(i)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


# ---------- SAVE XML ----------
def save_xml(name, data):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"{name}.xml").write_bytes(data)


# ---------- CSS FILE ----------
def write_css():
    css = """
body {
    margin: 0;
    padding: 32px 16px;
    background: #0b0b0d;
    color: white;
    font-family: Vazirmatn, sans-serif;
}

.container {
    max-width: 920px;
    margin: auto;
}

.title {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

.grid {
    display: grid;
    gap: 14px;
}

.card {
    background: #16171c;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.06);
}

.meta {
    display: flex;
    justify-content: space-between;
    opacity: 0.7;
    font-size: 13px;
    margin-bottom: 10px;
}

.content {
    line-height: 1.9;
}

a {
    display: inline-block;
    margin-top: 12px;
    color: white;
    text-decoration: none;
    opacity: 0.7;
}
"""
    (OUTPUT_DIR / "style.css").write_text(css, encoding="utf-8")


# ---------- HTML ----------
def build_index(feeds):
    cards = []

    for f in feeds:
        for i, item in enumerate(f["items"], 1):
            anchor = f"{f['file']}-{i}"

            cards.append(f"""
<div class="card" id="{anchor}">
    <div class="meta">
        <span>{f['source']}</span>
        <span>{item['date']}</span>
    </div>

    <div class="content">{item['title']}</div>

    <a href="#{anchor}">link</a>
</div>
""")

    html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<title>Feed</title>
<link rel="stylesheet" href="style.css">
</head>

<body>
<div class="container">

<div class="title">News Feed</div>

<div class="grid">
{''.join(cards)}
</div>

</div>
</body>
</html>
"""

    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")


# ---------- MAIN ----------
def main():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    feeds = []

    write_css()

    for s in config.get("telegram", []):
        html = fetch(s["url"])
        items = parse_telegram(html)

        items.sort(key=lambda x: normalize_date(x["date"]), reverse=True)

        save_xml(s["dir_name"], build_xml(items, s["title"]))

        feeds.append({
            "source": s["title"],
            "file": s["dir_name"],
            "items": items
        })

    for s in config.get("rss", []):
        xml = fetch(s["url"])
        items = parse_rss(xml)

        items.sort(key=lambda x: normalize_date(x["date"]), reverse=True)

        save_xml(s["dir_name"], build_xml(items, s["title"]))

        feeds.append({
            "source": s["title"],
            "file": s["dir_name"],
            "items": items
        })

    build_index(feeds)


if __name__ == "__main__":
    main()