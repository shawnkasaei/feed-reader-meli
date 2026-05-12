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
    r = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }
    )

    r.raise_for_status()

    return r.text


# ---------- CLEAN HTML ----------
def clean_html(text):

    text = re.sub(r"<br\s*\/?>", "\n", text)

    text = re.sub(r"<[^>]+>", "", text)

    text = (
        text
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )

    return text.strip()


# ---------- DATE FORMAT ----------
def to_tehran_rss(dt):

    return dt.astimezone(
        TEHRAN_TZ
    ).strftime(
        "%a, %d %b %Y %H:%M:%S +0330"
    )


# ---------- DATE NORMALIZER ----------
def normalize_date(d):

    try:
        return parsedate_to_datetime(d)

    except:
        return datetime.datetime.now(
            TEHRAN_TZ
        )


# ---------- TELEGRAM PARSER ----------
def parse_telegram(html):

    blocks = re.findall(
        r'tgme_widget_message_bubble[\s\S]*?<\/div>\s*<\/div>',
        html
    )

    items = []

    for block in blocks:

        text_match = re.search(
            r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>',
            block
        )

        time_match = re.search(
            r'<time[^>]*datetime="([^"]+)"',
            block
        )

        if not text_match or not time_match:
            continue

        try:

            text = clean_html(
                text_match.group(1)
            )

            if not text:
                continue

            utc_dt = datetime.datetime.fromisoformat(
                time_match.group(1)
            )

            items.append({
                "title": text,
                "date": to_tehran_rss(utc_dt)
            })

        except:
            pass

    return items


# ---------- RSS PARSER ----------
def parse_rss(xml_content):

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

            title = clean_html(
                title_match.group(1)
            )

            if not title:
                continue

            utc_dt = parsedate_to_datetime(
                date_match.group(1).strip()
            )

            items.append({
                "title": title,
                "date": to_tehran_rss(utc_dt)
            })

        except:
            pass

    return items


# ---------- BUILD XML ----------
def build_xml(items, feed_title):

    root = ET.Element(
        "rss",
        version="2.0"
    )

    channel = ET.SubElement(
        root,
        "channel"
    )

    channel_title = ET.SubElement(
        channel,
        "title"
    )

    channel_title.text = feed_title

    for i in items:

        item = ET.SubElement(
            channel,
            "item"
        )

        title_elem = ET.SubElement(
            item,
            "title"
        )

        title_elem.text = i["title"]

        date_elem = ET.SubElement(
            item,
            "pubDate"
        )

        date_elem.text = i["date"]

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )


# ---------- SAVE XML ----------
def save_feed(filename, xml_data):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = OUTPUT_DIR / f"{filename}.xml"

    if not output_path.exists():
        output_path.touch()

    output_path.write_bytes(
        xml_data
    )


# ---------- PROCESS TELEGRAM ----------
def process_telegram(source):

    html = fetch(
        source["url"]
    )

    items = parse_telegram(
        html
    )

    items.sort(
        key=lambda x: normalize_date(
            x["date"]
        ),
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

    print(
        f"Telegram OK -> "
        f"{source['dir_name']}.xml "
        f"({len(items)} items)"
    )


# ---------- PROCESS RSS ----------
def process_rss(source):

    xml_content = fetch(
        source["url"]
    )

    items = parse_rss(
        xml_content
    )

    items.sort(
        key=lambda x: normalize_date(
            x["date"]
        ),
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

    print(
        f"RSS OK -> "
        f"{source['dir_name']}.xml "
        f"({len(items)} items)"
    )


# ---------- MAIN ----------
def main():

    config = json.loads(
        CONFIG_PATH.read_text(
            encoding="utf-8"
        )
    )

    for source in config.get(
        "telegram",
        []
    ):

        try:
            process_telegram(
                source
            )

        except Exception as e:

            print(
                f"Telegram ERROR -> "
                f"{source['title']}"
            )

            print(e)

    for source in config.get(
        "rss",
        []
    ):

        try:
            process_rss(
                source
            )

        except Exception as e:

            print(
                f"RSS ERROR -> "
                f"{source['title']}"
            )

            print(e)


if __name__ == "__main__":
    main()