import yfinance as yf
import pandas as pd
import numpy as np

from enum import Enum
from typing import Optional, Union

from quoteables import LOADABLE 

class Instrument:
    def __init__(self, type: str, name_symbol: Optional[str]):
        self.type = type
        self.symbol = name_symbol
    
    def load_instrument_data(self) -> None:
        if self.type in LOADABLE:
            try:
                self.load = yf.Ticker(self.symbol)
                self.loaded = True
            except:
                raise Exception(
                    "Instrument could not be loaded using internal libraries or is not priceable."  
                )
            
class Priceable(Instrument):
    def __init__(self, type: str, name_symbol: str):
        if type not in LOADABLE:
            raise ValueError("Expected priceable instrument type. ie: stock, option, exchange.")
        else: 
            super().__init__(type=type, name_symbol=name_symbol)
            self.load_instrument_data()
        
    def get_price_history(self, price_timing: str, period: str, interval: str = None) -> pd.Series:
        '''
        Returns price history as time series.

        :param price_timing: Open, Close, High, Low
        :param period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        :param interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo

        **Usage**

        Pull price time series data for modelling.

        **Examples**

        >>> aapl_stock = Priceable(type='stock', name_symbole='AAPL')
        >>> aapl_stock.get_price_history(price_timing='Open', period='3mo', interval='1d')
        >>> 
        Date
        2025-05-09 00:00:00-04:00    198.739390
        2025-05-12 00:00:00-04:00    210.970001
        2025-05-13 00:00:00-04:00    210.429993
        2025-05-14 00:00:00-04:00    212.429993
        2025-05-15 00:00:00-04:00    210.949997
            ...
        2025-08-04 00:00:00-04:00    204.509995
        2025-08-05 00:00:00-04:00    203.399994
        2025-08-06 00:00:00-04:00    205.630005
        2025-08-07 00:00:00-04:00    218.880005
        2025-08-08 00:00:00-04:00    220.830002
        Name: Open, Length: 63, dtype: float64
        '''
        if interval==None:
            return self.load.history(period = period)[price_timing]
        return self.load.history(period = period, interval = interval)[price_timing].astype(np.float64)

    def get_volume_history(self, period: str, interval: str = None) -> pd.Series:
        '''
        Returns volume history as time series.

        :param period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        :param interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo

        **Usage**

        Pull volume time series data for modelling.

        **Examples**

        >>> aapl_stock = Priceable(type='stock', name_symbole='AAPL')
        >>> aapl_stock.get_volume_history(period='3mo')
        >>> 
        Date
        2025-05-09 00:00:00-04:00     36453900
        2025-05-09 00:00:00-04:00     36453900
        2025-05-12 00:00:00-04:00     63775800
        2025-05-13 00:00:00-04:00     51909300
        2025-05-14 00:00:00-04:00     49325800
        2025-05-15 00:00:00-04:00     45029500
                                       ...
        2025-08-04 00:00:00-04:00     75109300
        2025-08-05 00:00:00-04:00     44155100
        2025-08-06 00:00:00-04:00    108483100
        2025-08-07 00:00:00-04:00     90224800
        2025-08-08 00:00:00-04:00    113696100
        Name: Volume, Length: 63, dtype: int64
        '''
        if interval==None:
            return self.load.history(period = period)['Volume']
        return self.load.history(period = period, interval = interval)['Volume'].astype(np.float64)


