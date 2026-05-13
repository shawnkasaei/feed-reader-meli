import json
from pathlib import Path

from core.fetcher import Fetcher
from core.parser import Parser
from core.xml_builder import XMLBuilder
from core.html_builder import HTMLBuilder
from core.storage import Storage


BASE = Path(__file__).resolve().parents[1]


class App:

    def __init__(self):

        # ---------- CONFIG ----------
        self.config = json.loads(
            (BASE / "Config" / "sources.json").read_text(
                encoding="utf-8"
            )
        )

        # ---------- CORE SERVICES ----------
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.xml_builder = XMLBuilder()
        self.html_builder = HTMLBuilder()
        self.storage = Storage(BASE)

    def run(self):

        feeds = []

        # =========================================================
        # TELEGRAM SOURCES
        # =========================================================
        for source in self.config.get("telegram", []):

            try:

                html = self.fetcher.get(source["url"])

                items = self.parser.parse_telegram(html)

                if not items:
                    print(f"⚠ No telegram items -> {source['title']}")
                    continue

                # ---------- BUILD XML ----------
                xml_data = self.xml_builder.build(
                    items,
                    source["title"],
                    source["dir_name"]
                )

                # ---------- SAVE XML ----------
                self.storage.save_xml(
                    source["dir_name"],
                    xml_data
                )

                # ---------- APPEND TO UI FEEDS ----------
                feeds.append({
                    "source": source["title"],
                    "file": source["dir_name"],
                    "platform": "telegram",
                    "items": items
                })

                print(
                    f"✔ Telegram -> "
                    f"{source['dir_name']} "
                    f"({len(items)} items)"
                )

            except Exception as e:

                print(
                    f"❌ Telegram error -> "
                    f"{source['title']}"
                )

                print(e)

        # =========================================================
        # RSS SOURCES
        # =========================================================
        for source in self.config.get("rss", []):

            try:

                xml = self.fetcher.get(source["url"])

                items = self.parser.parse_rss(xml)

                if not items:
                    print(f"⚠ No rss items -> {source['title']}")
                    continue

                # ---------- BUILD XML ----------
                xml_data = self.xml_builder.build(
                    items,
                    source["title"],
                    source["dir_name"]
                )

                # ---------- SAVE XML ----------
                self.storage.save_xml(
                    source["dir_name"],
                    xml_data
                )

                # ---------- APPEND TO UI FEEDS ----------
                feeds.append({
                    "source": source["title"],
                    "file": source["dir_name"],
                    "platform": "rss",
                    "items": items
                })

                print(
                    f"✔ RSS -> "
                    f"{source['dir_name']} "
                    f"({len(items)} items)"
                )

            except Exception as e:

                print(
                    f"❌ RSS error -> "
                    f"{source['title']}"
                )

                print(e)

        # =========================================================
        # SORT ALL ITEMS FOR LATEST SECTION
        # =========================================================
        all_items = []

        for feed in feeds:

            for item in feed["items"]:

                item.source = feed["source"]

                all_items.append(item)

        try:

            all_items.sort(
                key=lambda x: getattr(x, "timestamp", 0),
                reverse=True
            )

        except Exception:
            pass

        # =========================================================
        # BUILD HTML UI
        # =========================================================
        html = self.html_builder.build(
            feeds=feeds,
            latest_items=all_items[:50]
        )

        # =========================================================
        # SAVE HTML
        # =========================================================
        self.storage.save_html(html)

        print(
            "✔ index.html generated successfully "
            "in Feeds/view/"
        )


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == "__main__":
    App().run()