from time_utils import TimeUtils # Add core
import tradingview_screener # Add this to requirements.txt - pip install tradingview-screener

class TradingViewFetcher:
    def parse_tuple(self, t:tuple, key:str, type:str="string"):
        if type == "float":
            return float(t[1].get(key)[0])

        return t[1].get(key)[0]

    def get_stock(self, symbol):
        data = (tradingview_screener.Query()
                .select('close', 'change')
                .where(tradingview_screener.col('name') == symbol)
                .get_scanner_data())
        
        return {
            "symbol": symbol,
            "price": self.parse_tuple(data, 'close', 'float'),
            "change": self.parse_tuple(data, 'change', 'float'),
            "source": "tradingview"
        }

    def get_crypto(self, symbol):
        data = (tradingview_screener.crypto()
                .select('close', 'change')
                .where(tradingview_screener.col('name') == symbol)
                .get_scanner_data())
        
        return {
            "symbol": symbol,
            "price": self.parse_tuple(data, 'close', 'float'),
            "change": self.parse_tuple(data, 'change', 'float'),
            "source": "tradingview"
        }

    def get_index(self, symbol):
        data = (tradingview_screener.Query()
                .set_index(symbol)
                .limit(500)
                .get_scanner_data())
        
        return data

        return {
            "symbol": symbol,
            "price": float(data[1].get('close')[0]),
            "change": float(data[1].get('change')[0]),
            "source": "tradingview"
        }

    def get_commodity(self, symbol):
        return self.yahoo(symbol)

    def get_forex(self, symbol):
        return self.tradingview(symbol)

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


if __name__ == "__main__":
    print(TradingViewFetcher().get_index("SYML:SP;SPX"))