import datetime
from dataclasses import dataclass

@dataclass
class FeedItem:
    title: str
    date: datetime.datetime