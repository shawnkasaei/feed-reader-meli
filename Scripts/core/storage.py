from pathlib import Path


class Storage:

    def __init__(self, base_path):
        self.base = Path(base_path)

        self.feeds = self.base / "Feeds"

        self.view = self.feeds / "view"

    def save_xml(self, name: str, data: bytes):
        self.feeds.mkdir(parents=True, exist_ok=True)
        (self.feeds / f"{name}.xml").write_bytes(data)

    def save_html(self, html: str):
        self.view.mkdir(parents=True, exist_ok=True)
        (self.view / "index.html").write_text(html, encoding="utf-8")

    def save_css(self, css: str):
        self.view.mkdir(parents=True, exist_ok=True)
        (self.view / "style.css").write_text(css, encoding="utf-8")