from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

TEHRAN = timezone(timedelta(hours=3, minutes=30))
UTC = timezone.utc


class TimeUtils:

    @staticmethod
    def now() -> datetime:
        return TimeUtils.to_tehran(datetime.now())

    @staticmethod
    def _normalize(dt):
        if dt is None:
            return TimeUtils.now()

        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S")
                dt = dt.replace(tzinfo=TEHRAN)
            except:
                try:
                    dt = parsedate_to_datetime(dt)
                except:
                    return TimeUtils.now()

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)

        return dt

    @staticmethod
    def to_tehran(dt) -> str:
        dt = TimeUtils._normalize(dt)
        return dt.astimezone(TEHRAN).strftime(
            "%a, %d %b %Y %H:%M:%S"
        )

    @staticmethod
    def parse_rss(date_str: str):
        try:
            return parsedate_to_datetime(date_str)
        except:
            return TimeUtils.now()

    @staticmethod
    def relative(dt) -> str:
        now = TimeUtils.now()
        dt = TimeUtils._normalize(dt)

        diff = now - dt.astimezone(TEHRAN)
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return "چند ثانیه پیش"
        if seconds < 3600:
            return f"{seconds // 60} دقیقه پیش"
        if seconds < 86400:
            return f"{seconds // 3600} ساعت پیش"
        if seconds < 2592000:
            return f"{seconds // 86400} روز پیش"
        return f"{seconds // 2592000} ماه پیش"