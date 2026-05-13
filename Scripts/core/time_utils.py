from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

TEHRAN = timezone(timedelta(hours=3, minutes=30))
UTC = timezone.utc


class TimeUtils:

    @staticmethod
    def now() -> datetime:
        return datetime.now(TEHRAN)

    @staticmethod
    def to_tehran(dt: datetime) -> str:
        return dt.astimezone(TEHRAN).strftime(
            "%a, %d %b %Y %H:%M:%S +0330"
        )

    @staticmethod
    def parse_rss(date_str: str):
        try:
            return parsedate_to_datetime(date_str)
        except:
            return TimeUtils.now()

    @staticmethod
    def _normalize(dt):
        if isinstance(dt, str):
            try:
                dt = datetime.strptime(dt, "%a, %d %b %Y %H:%M:%S +0330")
                dt = dt.replace(tzinfo=TEHRAN)
            except:
                dt = parsedate_to_datetime(dt)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)

        return dt

    @staticmethod
    def relative(dt) -> str:
        now = TimeUtils.now()

        dt = TimeUtils._normalize(dt)
        dt_tehran = dt.astimezone(TEHRAN)

        diff = now - dt_tehran
        seconds = int(diff.total_seconds())

        if seconds < 60:
            return "چند ثانیه پیش"
        elif seconds < 3600:
            return f"{seconds // 60} دقیقه پیش"
        elif seconds < 86400:
            return f"{seconds // 3600} ساعت پیش"
        elif seconds < 2592000:
            return f"{seconds // 86400} روز پیش"
        else:
            return f"{seconds // 2592000} ماه پیش"