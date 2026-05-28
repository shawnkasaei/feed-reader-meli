import re
from core.string_utils import StringUtils
from models.feed_item import FeedItem
from core.time_utils import TimeUtils


class Parser:

    TITLE_WORD_LIMIT = 12

    def parse_telegram(self, html: str):
        blocks = re.findall(
            r'tgme_widget_message_bubble[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>',
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
                c = text.group(1).strip()
                c = StringUtils.remove_html_shenanegans(c)

                items.insert(0,
                    FeedItem(
                        title=StringUtils.truncate_text(c, self.TITLE_WORD_LIMIT),
                        content=c,
                        date=TimeUtils.to_string(dt),
                        link=""
                    )
                )

            except:
                continue

        return items

    def parse_rss(self, xml: str):
        items = []

        for item in re.findall(r"<item>([\s\S]*?)<\/item>", xml):

            t = re.search(r"<title>([\s\S]*?)<\/title>", item).group(1).strip()
            c = re.search(r"<description>([\s\S]*?)<\/description>", item).group(1).strip()
            d = re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", item).group(1).strip()
            l = re.search(r"<link>([\s\S]*?)<\/link>", item).group(1).strip()

            if not t or not d:
                continue

            try:
                dt = TimeUtils.parse_rss(d)

                items.append(
                    FeedItem(
                        title=StringUtils.truncate_text(t, self.TITLE_WORD_LIMIT),
                        content=StringUtils.remove_html_shenanegans(c),
                        date=TimeUtils.to_string(dt),
                        link=l
                    )
                )

            except:
                continue

        return items