import json
from bs4 import BeautifulSoup
from core.string_utils import StringUtils
from core.time_utils import TimeUtils
from models.feed_item import FeedItem


class Website:

    def parse(self, html:str, scraping_rules: str, title_char_limit:int = 60):

        rules = json.loads(scraping_rules)

        soup = BeautifulSoup(html, "html.parser")

        containers = soup.select(rules.get("container"))

        results = []

        for c in containers:
            title_selector = rules.get("title")
            title = c.select_one(title_selector).get_text(strip=True) if title_selector else ""

            description_selector = rules.get("description")
            description = c.select_one(description_selector).get_text(strip=True) if description_selector else "" 

            date_selector = rules.get("date")
            date = c.select_one(date_selector).get_text(strip=True) if date_selector else ""

            date_format = rules.get("date_format")
            
            if date and date_format:
                date = TimeUtils.normalize(date, date_format)
                date = TimeUtils.to_string(date)

            url_selector = rules.get("url")
            url = c.select_one(url_selector).get("href") if url_selector else ""

            url_base = rules.get("url_base")

            if url_base and url:
                url = url_base + url

            results.append(
                    FeedItem(
                        title=StringUtils.truncate_text_char(title, title_char_limit),
                        content=description,
                        date=date,
                        link=url
                    )
                )

        return results