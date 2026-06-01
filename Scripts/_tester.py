from core.fetcher import Fetcher
from core.parsers.website import Website


fetcher = Fetcher()
html = fetcher.get_text_by_selenium("https://www3.nhk.or.jp/nhkworld/fa/news/list/", "div.c-item__texts > div.c-item__title > a")
parser = Website()
data = parser.parse(
            html=html,
            scraping_rules='''{
                "container": "body > div.l-wrapper.-show > div > div > div > div.c-list.-type01 > ul > li",
                "title": "div.c-item__texts > div.c-item__title > a",
                "description": null,
                "date": "div.c-item__texts > div.c-item__info > span",
                "date_format": null,
                "url_base": "https://www3.nhk.or.jp",
                "url": "div.c-item__texts > div.c-item__title > a"
            }''')

print(data)