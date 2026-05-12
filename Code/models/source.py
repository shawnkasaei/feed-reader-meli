from dataclasses import dataclass

@dataclass
class Source:
    title: str
    dir_name: str
    url: str
    type: str  # telegram | rss