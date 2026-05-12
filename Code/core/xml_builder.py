import xml.etree.ElementTree as ET


class XMLBuilder:

    def build(self, items, title: str):

        root = ET.Element("rss", version="2.0")
        channel = ET.SubElement(root, "channel")

        ET.SubElement(channel, "title").text = title

        for i, item in enumerate(items, 1):

            node = ET.SubElement(channel, "item")

            ET.SubElement(node, "title").text = item.title
            ET.SubElement(node, "pubDate").text = item.date
            ET.SubElement(node, "guid").text = str(i)

        return ET.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True
        )