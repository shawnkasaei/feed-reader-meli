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

TEHRAN_TZ = datetime.timezone(
    datetime.timedelta(hours=3, minutes=30)
)


# ---------- FETCH ----------
def fetch(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.text


# ---------- DATE FORMATTER ----------
def to_tehran_rss(dt):
    return dt.astimezone(
        TEHRAN_TZ
    ).strftime("%a, %d %b %Y %H:%M:%S +0330")


# ---------- CLEAN HTML ----------
def clean_html(text):
    return re.sub(r"<[^>]+>", "", text).strip()


# ---------- TELEGRAM PARSER ----------
def parse_telegram(html, source_title):
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

        if not text_match or not time_match:
            continue

        try:
            text = clean_html(
                text_match.group(1)
            )

            utc_dt = datetime.datetime.fromisoformat(
                time_match.group(1)
            )

            items.append({
                "title": f"{source_title} - {text}",
                "date": to_tehran_rss(utc_dt)
            })

        except:
            pass

    return items


# ---------- RSS PARSER ----------
def parse_rss(xml_content, source_title):
    items = []

    for block in re.findall(
        r"<item>([\s\S]*?)<\/item>",
        xml_content
    ):

        title_match = re.search(
            r"<title>([\s\S]*?)<\/title>",
            block
        )

        date_match = re.search(
            r"<pubDate>([\s\S]*?)<\/pubDate>",
            block
        )

        if not title_match or not date_match:
            continue

        try:
            utc_dt = parsedate_to_datetime(
                title_match and date_match.group(1).strip()
            )

            items.append({
                "title": f"{source_title} - {clean_html(title_match.group(1))}",
                "date": to_tehran_rss(utc_dt)
            })

        except:
            pass

    return items


# ---------- SORT ----------
def normalize_date(d):
    try:
        return parsedate_to_datetime(d)
    except:
        return datetime.datetime.now(TEHRAN_TZ)


# ---------- BUILD XML ----------
def build_xml(items, source_title):

    root = ET.Element("rss", version="2.0")

    channel = ET.SubElement(root, "channel")

    title_elem = ET.SubElement(channel, "title")
    title_elem.text = source_title

    for i in items:

        item = ET.SubElement(channel, "item")

        item_title = ET.SubElement(item, "title")
        item_title.text = i["title"]

        item_date = ET.SubElement(item, "pubDate")
        item_date.text = i["date"]

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )


# ---------- SAVE ----------
def save_feed(filename, xml_data):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = OUTPUT_DIR / f"{filename}.xml"

    output_path.write_bytes(xml_data)


# ---------- PROCESS TELEGRAM ----------
def process_telegram(source):

    html = fetch(source["url"])

    items = parse_telegram(
        html,
        source["title"]
    )

    items.sort(
        key=lambda x: normalize_date(x["date"]),
        reverse=True
    )

    xml_data = build_xml(
        items,
        source["title"]
    )

    save_feed(
        source["dir_name"],
        xml_data
    )


# ---------- PROCESS RSS ----------
def process_rss(source):

    xml_content = fetch(source["url"])

    items = parse_rss(
        xml_content,
        source["title"]
    )

    items.sort(
        key=lambda x: normalize_date(x["date"]),
        reverse=True
    )

    xml_data = build_xml(
        items,
        source["title"]
    )

    save_feed(
        source["dir_name"],
        xml_data
    )


# ---------- MAIN ----------
def main():

    config = json.loads(
        CONFIG_PATH.read_text(
            encoding="utf-8"
        )
    )

    for source in config.get("telegram", []):
        try:
            process_telegram(source)
            print(f"Telegram OK -> {source['dir_name']}.xml")
        except Exception as e:
            print(f"Telegram ERROR -> {source['title']}")
            print(e)

    for source in config.get("rss", []):
        try:
            process_rss(source)
            print(f"RSS OK -> {source['dir_name']}.xml")
        except Exception as e:
            print(f"RSS ERROR -> {source['title']}")
            print(e)


if __name__ == "__main__":
    main()