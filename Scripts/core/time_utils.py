from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))


class TimeUtils:

    @staticmethod
    def parse_telegram(time_str: str) -> datetime:
        # Example: 2026-05-13T14:47:05+00:00
        dt = datetime.fromisoformat(time_str)
        return dt.astimezone(TEHRAN_TZ)

    @staticmethod
    def parse_rss(time_str: str) -> datetime:
        # Example: Wed, 13 May 2026 14:37:11 GMT
        dt = parsedate_to_datetime(time_str)
        return dt.astimezone(TEHRAN_TZ)

    @staticmethod
    def to_tehran(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(TEHRAN_TZ)

    @staticmethod
    def to_string(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(fmt)

    @staticmethod
    def now() -> datetime:
        return datetime.now(TEHRAN_TZ)
