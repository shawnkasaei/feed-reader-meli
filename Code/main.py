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

        self.config = json.loads(
            (BASE / "Config/sources.json").read_text(encoding="utf-8")
        )

        self.fetcher = Fetcher()
        self.parser = Parser()
        self.xml = XMLBuilder()
        self.html = HTMLBuilder()
        self.storage = Storage(BASE)

    def run(self):

        feeds = []

        for s in self.config.get("telegram", []):

            html = self.fetcher.get(s["url"])
            items = self.parser.parse_telegram(html)

            xml = self.xml.build(items, s["title"])
            self.storage.save_xml(s["dir_name"], xml)

            feeds.append({
                "source": s["title"],
                "file": s["dir_name"],
                "items": items
            })

        for s in self.config.get("rss", []):

            xml_raw = self.fetcher.get(s["url"])
            items = self.parser.parse_rss(xml_raw)

            xml = self.xml.build(items, s["title"])
            self.storage.save_xml(s["dir_name"], xml)

            feeds.append({
                "source": s["title"],
                "file": s["dir_name"],
                "items": items
            })

        html = self.html.build(feeds)
        self.storage.save_html(html)


if __name__ == "__main__":
    App().run()