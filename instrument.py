import yfinance as yf
import pandas as pd

from typing import Optional, Union

PRICEABLE_LOOKUP = ['stock', 'currency', 'exchange', 'fx']

class Instrument:
    def __init__(self, type: str, name_symbol: Optional[str]):
        self.type = type
        self.symbol = name_symbol
        if self.type in PRICEABLE_LOOKUP:
            try:
                self.load = yf.Ticker(self.symbol)
                self.loaded = True
            except:
                raise Exception(
                    "Instrument could not be loaded using internal libraries or is not priceable."  
                )

class Priceable(Instrument):
    def __init__(self, type: str, name_symbol: str):
        super().__init__(type=type, name_symbol=name_symbol)
        self.priceable = True

    def get_price_history(self, price_timing: str, period: str, interval: str = None) -> pd.Series:
        '''
        Returns price history as time series.

        :param price_timing: Open, Close, High, Low
        :param period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        :param interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo
        '''
        if interval==None:
            return self.load.history(period = period)[price_timing]
        return self.load.history(period = period, interval = interval)[price_timing]

    def get_volume_history(self, period: str, interval: str = None) -> pd.Series:
        if interval==None:
            return self.load.history(period = period)['Volume']
        return self.load.history(period = period, interval = interval)['Volume']

