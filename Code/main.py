import json
import re
import requests
import datetime
import xml.etree.ElementTree as ET
from pathlib import Path
from email.utils import parsedate_to_datetime

BASE = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE / "Config" / "sources.json"
OUTPUT_XML = BASE / "Content" / "feed.xml"

TEHRAN_TZ = datetime.timezone(datetime.timedelta(hours=3, minutes=30))


# ---------- FETCH ----------
def fetch(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text


# ---------- DATE FORMATTER ----------
def to_tehran_rss(dt):
    return dt.astimezone(TEHRAN_TZ).strftime("%a, %d %b %Y %H:%M:%S +0330")


# ---------- TELEGRAM PARSER ----------
def parse_telegram(html, title):
    blocks = re.findall(
        r'tgme_widget_message_bubble[\s\S]*?<\/div>\s*<\/div>',
        html
    )

    items = []

    for b in blocks:
        text_match = re.search(
            r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>',
            b
        )

        time_match = re.search(
            r'<time[^>]*datetime="([^"]+)"',
            b
        )

        if text_match and time_match:
            text = re.sub(r"<[^>]+>", "", text_match.group(1)).strip()

            utc_dt = datetime.datetime.fromisoformat(
                time_match.group(1)
            )

            tehran_date = to_tehran_rss(utc_dt)

            items.append({
                "title": f"{title} - {text}",
                "date": tehran_date
            })

    return items


# ---------- SIMPLE RSS PARSER ----------
def parse_rss(xml_content, title):
    items = []

    for item in re.findall(r"<item>([\s\S]*?)<\/item>", xml_content):
        t = re.search(r"<title>([\s\S]*?)<\/title>", item)
        d = re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", item)

        if t and d:
            try:
                utc_dt = parsedate_to_datetime(d.group(1).strip())

                tehran_date = to_tehran_rss(utc_dt)

                items.append({
                    "title": f"{title} - {t.group(1).strip()}",
                    "date": tehran_date
                })

            except:
                pass

    return items


# ---------- DATE NORMALIZER ----------
def normalize_date(d):
    try:
        return parsedate_to_datetime(d)
    except:
        return datetime.datetime.now(TEHRAN_TZ)


# ---------- BUILD XML ----------
def build_xml(items):
    root = ET.Element("rss")
    channel = ET.SubElement(root, "channel")

    for i in items:
        item = ET.SubElement(channel, "item")

        title_elem = ET.SubElement(item, "title")
        title_elem.text = i["title"]

        date_elem = ET.SubElement(item, "pubDate")
        date_elem.text = i["date"]

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )


# ---------- MAIN ----------
def main():
    config = json.loads(CONFIG_PATH.read_text())

    all_items = []

    # Telegram sources
    for t in config.get("telegram", []):
        html = fetch(t["url"])
        all_items += parse_telegram(html, t["title"])

    # RSS sources
    for r in config.get("rss", []):
        xml_content = fetch(r["url"])
        all_items += parse_rss(xml_content, r["title"])

    # Sort and keep latest 9
    sorted_items = sorted(
        all_items,
        key=lambda x: normalize_date(x["date"]),
        reverse=True
    )

    latest_items = sorted_items[:9]

    # Build XML
    xml_data = build_xml(latest_items)

    OUTPUT_XML.write_bytes(xml_data)


if __name__ == "__main__":
    main()