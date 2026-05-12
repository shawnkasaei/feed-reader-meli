import datetime
from email.utils import parsedate_to_datetime

TEHRAN = datetime.timezone(datetime.timedelta(hours=3, minutes=30))


class TimeUtils:

    @staticmethod
    def to_tehran(dt: datetime.datetime) -> str:
        return dt.astimezone(TEHRAN).strftime(
            "%a, %d %b %Y %H:%M:%S +0330"
        )

    @staticmethod
    def parse_rss(date_str: str):
        try:
            return parsedate_to_datetime(date_str)
        except:
            return datetime.datetime.now(TEHRAN)