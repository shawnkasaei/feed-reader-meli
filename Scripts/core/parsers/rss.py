import re
from core.string_utils import StringUtils
from core.time_utils import TimeUtils
from models.feed_item import FeedItem


class RSS:

    def parse(self, xml: str, title_char_limit:int = 60):
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
                        title=StringUtils.truncate_text_char(t, title_char_limit),
                        content=StringUtils.remove_html_shenanegans(c),
                        date=TimeUtils.to_string(dt),
                        link=l
                    )
                )

            except:
                continue

        return items