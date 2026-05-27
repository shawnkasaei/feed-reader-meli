import re
from models.feed_item import FeedItem
from core.time_utils import TimeUtils


class Parser:

    def parse_telegram(self, html: str):
        blocks = re.findall(
            r'tgme_widget_message_bubble[\s\S]*?</div>\s*</div>',
            html
        )

        items = []

        for b in blocks:

            text = re.search(
                r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>',
                b
            )

            time = re.search(
                r'<time[^>]*datetime="([^"]+)"',
                b
            )

            if not text or not time:
                continue

            try:
                dt = TimeUtils.parse_telegram(time.group(1))

                items.insert(0,
                    FeedItem(
                        title=re.sub(r"<[^>]+>", "", text.group(1)).strip(),
                        content="",
                        date=TimeUtils.to_string(dt)
                    )
                )

            except:
                continue

        return items

    def parse_rss(self, xml: str):
        items = []

        for item in re.findall(r"<item>([\s\S]*?)<\/item>", xml):

            t = re.search(r"<title>([\s\S]*?)<\/title>", item)
            d = re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", item)

            if not t or not d:
                continue

            try:
                dt = TimeUtils.parse_rss(d.group(1))

                items.append(
                    FeedItem(
                        title=re.sub(r"<[^>]+>", "", t.group(1)).strip(),
                        content="",
                        date=TimeUtils.to_string(dt)
                    )
                )

            except:
                continue

        return items