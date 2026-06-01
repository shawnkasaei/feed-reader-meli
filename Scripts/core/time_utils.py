from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Optional, Union

TEHRAN_TZ = timezone(timedelta(hours=3, minutes=30))


class TimeUtils:

    @staticmethod
    def normalize(
        value: Union[str, int, float, datetime],
        to_tz: timezone = TEHRAN_TZ,
        fmt: Optional[str] = None
    ) -> datetime:

        dt = TimeUtils._to_datetime(value, fmt)
        dt_utc = TimeUtils._to_utc(dt)
        return dt_utc.astimezone(to_tz)

    @staticmethod
    def _to_datetime(
        value: Union[str, int, float, datetime],
        fmt: Optional[str] = None
    ) -> datetime:

        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc)

        if isinstance(value, str):
            value = value.strip()

            if fmt:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    pass

            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass

            try:
                return parsedate_to_datetime(value)
            except Exception:
                pass

        raise ValueError(f"Unsupported time format: {value}")

    @staticmethod
    def _to_utc(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def to_string(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        return dt.strftime(fmt)

    @staticmethod
    def now(to_tz: timezone = TEHRAN_TZ) -> datetime:
        return datetime.now(timezone.utc).astimezone(to_tz)