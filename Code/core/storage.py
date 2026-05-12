from pathlib import Path


class Storage:

    def __init__(self, base_path):
        self.base = Path(base_path)
        self.content = self.base / "Content"

    def save_xml(self, name: str, data: bytes):
        self.content.mkdir(parents=True, exist_ok=True)
        (self.content / f"{name}.xml").write_bytes(data)

    def save_html(self, html: str):
        (self.content / "index.html").write_text(html, encoding="utf-8")

    def save_css(self, css: str):
        (self.content / "style.css").write_text(css, encoding="utf-8")