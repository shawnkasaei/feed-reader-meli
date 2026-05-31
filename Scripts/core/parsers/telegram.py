import re
from core.string_utils import StringUtils
from core.time_utils import TimeUtils
from models.feed_item import FeedItem


class Telegram:

    def parse(self, html: str, title_word_limit:int = 12):
        blocks = re.findall(
            r'(<div class="tgme_widget_message[^"]*"[^>]*data-post="([^"]+)"[\s\S]*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>)',
            html
        )

        items = []

        for full_block, data_post in blocks:

            text = re.search(
                r'tgme_widget_message_text[^>]*>([\s\S]*?)<\/div>',
                full_block
            )

            time = re.search(
                r'<time[^>]*datetime="([^"]+)"',
                full_block
            )

            if not text or not time:
                continue

            try:
                c = text.group(1).strip()
                c = StringUtils.remove_html_shenanegans(c)

                dt = TimeUtils.parse_telegram(time.group(1))

                link = f"https://t.me/{data_post}"

                items.insert(0,
                    FeedItem(
                        title=StringUtils.truncate_text(c, title_word_limit),
                        content=c,
                        date=TimeUtils.to_string(dt),
                        link=link
                    )
                )

            except:
                continue

        return items
