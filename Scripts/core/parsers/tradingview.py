from core.time_utils import TimeUtils
import tradingview_screener # Add this to requirements.txt - pip install tradingview-screener

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

    def get_index(self, symbol): # Under Construction
        data = (tradingview_screener.Query()
                .set_index(symbol)
                .limit(500)
                .get_scanner_data())
        
        return data

    def get_commodity(self, symbol):
        return None

    def get_forex(self, symbol):
        return None
    
if __name__ == "__main__":
    print(TradingView().get_index("SYML:SP;SPX"))