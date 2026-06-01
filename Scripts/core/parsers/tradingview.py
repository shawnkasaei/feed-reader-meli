import tradingview_screener

class TradingView:

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
        return None

    def get_commodity(self, symbol):
        return None

    def get_forex(self, symbol):
        return None