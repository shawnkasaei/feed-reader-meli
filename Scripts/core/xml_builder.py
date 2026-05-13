import xml.etree.ElementTree as ET
from core.time_utils import TimeUtils
from core.text_id_generator import TextIDGenerator

class XMLBuilder:

    def build(self, items, title: str, feed_name: str):

        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")

        ET.SubElement(channel, "title").text = title

        base_url = (
            "https://htmlpreview.github.io/?"
            "https://raw.githubusercontent.com/"
            "shawnkasaei/news-reader-meli/"
            "refs/heads/main/Feeds/view/index.html"
        )

        for item in items:

            anchor_id = f"{TextIDGenerator.generate(item.date+item.title)}"

            node = ET.SubElement(channel, "item")

            ET.SubElement(node, "title").text = item.title
            ET.SubElement(node, "pubDate").text = item.date
            ET.SubElement(node, "link").text = (
                f"{base_url}#{anchor_id}"
            )

        return ET.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True
        )