import xml.etree.ElementTree as ET


class XMLBuilder:

    def build(self, items, title: str, feed_name: str):

        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")

        ET.SubElement(channel, "title").text = title

        base_url = (
            "https://html-preview.github.io/"
            "?url=raw.githubusercontent.com/"
            "shawnkasaei/news-reader-meli/"
            "refs/heads/main/Feeds/view/index.html"
        )

        for i, item in enumerate(items, 1):

            anchor_id = f"{feed_name}-{i}"

            node = ET.SubElement(channel, "item")

            ET.SubElement(node, "title").text = item.title
            ET.SubElement(node, "pubDate").text = item.date

            # 🔥 لینک دقیق و sync با HTML
            ET.SubElement(node, "link").text = (
                f"{base_url}#{anchor_id}"
            )

        return ET.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True
        )