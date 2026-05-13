import json
import time
from pathlib import Path

from core.fetcher import Fetcher
from core.parser import Parser
from core.xml_builder import XMLBuilder
from core.html_builder import HTMLBuilder
from core.storage import Storage


BASE = Path(__file__).resolve().parents[1]


class App:

    def __init__(self):

        # config
        self.config = json.loads(
            (BASE / "Config" / "sources.json").read_text(encoding="utf-8")
        )

        # core services
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.xml_builder = XMLBuilder()
        self.html_builder = HTMLBuilder()
        self.storage = Storage(BASE)

    def run(self):

        feeds = []

        # ---------- TELEGRAM ----------
        for source in self.config.get("telegram", []):

            try:
                html = self.fetcher.get(source["url"])
                items = self.parser.parse_telegram(html)

                # build xml
                xml_data = self.xml_builder.build(
                    items,
                    source["title"],
                    source["dir_name"]
                )

                # save xml
                self.storage.save_xml(
                    source["dir_name"],
                    xml_data
                )

                feeds.append({
                    "source": source["title"],
                    "file": source["dir_name"],
                    "items": items
                })

                print(f"✔ Telegram -> {source['dir_name']}")

            except Exception as e:
                print(f"❌ Telegram error -> {source['title']}")
                print(e)

            time.sleep(1)

        # ---------- RSS ----------
        for source in self.config.get("rss", []):

            try:
                xml = self.fetcher.get(source["url"])
                items = self.parser.parse_rss(xml)

                xml_data = self.xml_builder.build(
                    items,
                    source["title"],
                    source["dir_name"]
                )

                self.storage.save_xml(
                    source["dir_name"],
                    xml_data
                )

                feeds.append({
                    "source": source["title"],
                    "file": source["dir_name"],
                    "items": items
                })

                print(f"✔ RSS -> {source['dir_name']}")

            except Exception as e:
                print(f"❌ RSS error -> {source['title']}")
                print(e)

            time.sleep(1)

        # ---------- BUILD UI ----------
        html = self.html_builder.build(feeds)

        self.storage.save_html(html)

        print("✔ index.html generated in Feeds/view/")


# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    App().run()