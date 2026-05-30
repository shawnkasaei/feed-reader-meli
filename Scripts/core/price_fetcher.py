from core.time_utils import TimeUtils
from core.fetcher import Fetcher
import yfinance # Add this to requirements.txt
from tvDatafeed import TvDatafeed, Interval

class PriceFetcher:
    def __init__(self, timeout=5):
        pass

    def _get(self, url):
        try:
            fetcher = Fetcher()
            return fetcher.get_json(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def binance(self, symbol: str):
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        data = self._get(url)

        if not data:
            return None

        return {
            "symbol": symbol,
            "price": float(data["lastPrice"]),
            "change_percent": float(data["priceChangePercent"]),
            "source": "binance"
        }

    def yahoo(self, symbol: str):
        ticker = yfinance.Ticker(symbol)
        data = ticker.info

        if not data:
            return None

        try:
            return {
                "symbol": symbol,
                "change_percent": data.get("regularMarketChangePercent"),
                "source": "yfinance/yahoo"
            }
        except:
            return None
        
    def tradingview(self, symbol: str):
        ticker = yfinance.Ticker(symbol)
        data = ticker.info

        if not data:
            return None

        try:
            return {
                "symbol": symbol,
                "price": data.get("regularMarketPrice"),
                "change_percent": data.get("regularMarketChangePercent"),
                "source": "yfinance/yahoo"
            }
        except:
            return None

    def iran_placeholder(self, name: str):
        # چون API رسمی نیست، اینجا بعداً scrape اضافه می‌کنی
        return {
            "symbol": name,
            "price": None,
            "change_percent": None,
            "source": "iran_placeholder"
        }

    def get_crypto(self, symbol):
        return self.binance(symbol)

    def get_index(self, symbol):
        return self.yahoo(symbol)

    def get_commodity(self, symbol):
        return self.yahoo(symbol)

    def get_forex(self, symbol):
        return None

    def collect(self):
        return {
            "timestamp": TimeUtils.now(),

            "crypto": [
                self.get_crypto("BTCUSD"),
                self.get_crypto("BTCUSDT"),
            ],

            "indices": [
                self.get_index("%5ESPX"),  # S&P 500
                self.get_index("DX-Y.NYB")  # US Dollar Index
            ],

            "commodities": [
                self.get_commodity("GC=F"),  # gold
                self.get_commodity("CL=F")   # oil
            ],

            "forex": [
                self.get_forex("eurusd"),
            ],

            "iran": [
                self.iran_placeholder("USD_IRR"),
                self.iran_placeholder("AED_IRR"),
                self.iran_placeholder("XAU_IRR"),
                self.iran_placeholder("COIN_IRR")
            ]
        }


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    price_fetcher = PriceFetcher(timeout=5)
    print(price_fetcher.collect())