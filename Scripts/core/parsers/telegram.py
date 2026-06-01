import re
from core.string_utils import StringUtils
from core.time_utils import TimeUtils
from models.feed_item import FeedItem


class Telegram:

    def __init__(self, allow_duplicates: bool = True, items_limit: int = 0, reverse_items: bool = False):
        
        self.allow_duplicates = allow_duplicates
        self.items_limit = items_limit
        self.reverse_items = reverse_items

    def parse(self, html: str, title_char_limit:int = 60):
        
        blocks = re.findall(
            r'(<div class="tgme_widget_message[^"]*"[^>]*data-post="([^"]+)"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>)',
            html
        )

        items = []
        count = 0

        for full_block, data_post in blocks:

            if self.items_limit != 0:
                count += 1
                if self.items_limit < count:
                    break

            text = re.search(
                r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>',
                full_block
            )

            time = re.search(
                r'<time[^>]*datetime="([^"]+)"',
                full_block
            )

            try:
                c = text.group(1).strip()
                c = StringUtils.remove_html_shenanegans(c)

                t = StringUtils.truncate_text_char(c, title_char_limit)

                dt = TimeUtils.normalize(time.group(1))
                dt = TimeUtils.to_string(dt)
                
                link = f"https://t.me/{data_post}"

                if (list(filter(lambda x: x.title == t, items))) and not self.allow_duplicates:
                    continue

                items.append(
                    FeedItem(
                        title=t,
                        content=c,
                        date=dt,
                        link=link
                    )
                )

            except:
                continue

        return items if not self.reverse_items else items[::-1]
