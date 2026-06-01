import re
from core.string_utils import StringUtils
from core.time_utils import TimeUtils
from models.feed_item import FeedItem


class RSS:

    def __init__(self, allow_duplicates: bool = True, reverse_items: bool = False):
        
        self.allow_duplicates = allow_duplicates
        self.reverse_items = reverse_items

    def parse(self, xml: str, title_char_limit:int = 60):

        items = []

        for item in re.findall(r"<item>([\s\S]*?)<\/item>", xml):

            t = re.search(r"<title>([\s\S]*?)<\/title>", item).group(1).strip()
            t = StringUtils.truncate_text_char(t, title_char_limit)

            c = re.search(r"<description>([\s\S]*?)<\/description>", item).group(1).strip()
            c = StringUtils.remove_html_shenanigans(c)
            
            d = re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", item).group(1).strip()
            
            l = re.search(r"<link>([\s\S]*?)<\/link>", item).group(1).strip()

            try:
                dt = TimeUtils.normalize(d)
                dt = TimeUtils.to_string(dt)

                if (list(filter(lambda x: x.title == t, items))) and not self.allow_duplicates:
                    continue

                items.append(
                    FeedItem(
                        title=t,
                        content=c,
                        date=dt,
                        link=l
                    )
                )

            except:
                continue

        return items if not self.reverse_items else items[::-1]