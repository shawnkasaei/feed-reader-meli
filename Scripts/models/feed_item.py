from dataclasses import dataclass
from datetime import datetime


@dataclass
class FeedItem:
    source: str
    title: str
    link: str
    timestamp: datetime
    relative_time: str
