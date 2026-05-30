import requests

class Fetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get(self, url: str) -> str:
        r = requests.get(url, headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.text
    
    def get_json(self, url: str) -> dict:
        r = requests.get(url, headers=self.headers, timeout=15)
        r.raise_for_status()
        return r.json()