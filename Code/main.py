import json
import re
import requests
import datetime
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE / "Config" / "sources.json"
KEY_FILE = BASE / "Config" / "favicon.png"
OUTPUT_XML = BASE / "Content" / "feed.xml"


# ---------- KEY LOADER ----------
def load_key():
    data = KEY_FILE.read_bytes()
    match = re.search(rb"IDEAS ARE BULLET PROOF", data)
    if not match:
        raise Exception("Key not found")
    return match.group().decode()


KEY = load_key()


# ---------- XOR ENCRYPT ----------
def xor_encrypt(text: str, key: str) -> str:
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))


# ---------- FETCH ----------
def fetch(url):
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text


# ---------- TELEGRAM PARSER ----------
def parse_telegram(html, title):
    blocks = re.findall(r'tgme_widget_message_bubble[\s\S]*?<\/div>\s*<\/div>', html)
    items = []

    for b in blocks:
        text_match = re.search(r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>', b)
        time_match = re.search(r'<time[^>]*class="time"[^>]*>([\s\S]*?)<\/time>', b)

        if text_match and time_match:
            text = re.sub(r"<[^>]+>", "", text_match.group(1)).strip()
            date = time_match.group(1).strip()
            items.append({
                "title": f"{title} - {text}",
                "date": date
            })
    return items


# ---------- SIMPLE RSS PARSER ----------
def parse_rss(xml_content, title):
    items = []
    for item in re.findall(r"<item>([\s\S]*?)<\/item>", xml_content):
        t = re.search(r"<title>([\s\S]*?)<\/title>", item)
        d = re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", item)
        if t and d:
            items.append({
                "title": f"{title} - {t.group(1).strip()}",
                "date": d.group(1).strip()
            })
    return items


# ---------- DATE NORMALIZER ----------
def normalize_date(d):
    try:
        # اگر فرمت RSS استاندارد باشد
        return datetime.datetime.strptime(d[:25], "%a, %d %b %Y %H:%M:%S")
    except:
        # fallback به زمان فعلی
        return datetime.datetime.utcnow()


# ---------- BUILD XML WITHOUT SORT ----------
def build_xml(items):
    root = ET.Element("rss")
    channel = ET.SubElement(root, "channel")

    for i in items:
        item = ET.SubElement(channel, "item")

        title_elem = ET.SubElement(item, "title")
        title_elem.text = xor_encrypt(i["title"], KEY)

        date_elem = ET.SubElement(item, "pubDate")
        date_elem.text = xor_encrypt(i["date"], KEY)

    return ET.tostring(root, encoding="utf-8")


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

    # Sort once and take only 9 newest
    sorted_items = sorted(all_items, key=lambda x: normalize_date(x["date"]), reverse=True)
    latest_items = sorted_items[:9]

    # Build XML
    xml_data = build_xml(latest_items)
    OUTPUT_XML.write_bytes(xml_data)


if __name__ == "__main__":
    main()