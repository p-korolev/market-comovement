import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from typing import Union, Any
from numbers import Real 

import stats
import algebra
from instrument import Priceable

# base linear plot class
class Plot:
    def __init__(self, *series: pd.Series):
        for s in series:
            plt.plot(s)
    
    def show(self) -> None:
        plt.legend()
        return plt.show()

class PricePlot:
    def __init__(self, 
                 *ticks: str, 
                 price_timing: str = 'Open',
                 period: str = '1d',
                 interval: str = '1m'):
        self.price_series = []
        for tick in ticks:
            self.price_series.append(
                Priceable(type='stock', name_symbol=tick).get_price_history(price_timing=price_timing, period=period, interval=interval)
                )
        i=0
        for s in self.price_series:
            plt.plot(s, label=ticks[i])
            i+=1
    
    def show(self) -> None:
        plt.legend()
        plt.show()

class ScaledPricePlot():
    def __init__(self, 
                 *ticks: str, 
                 price_timing: str = 'Open',
                 period: str = '1d',
                 interval: str = '1m',
                 scale_start: Real = 100):
        self.price_series = []
        for tick in ticks:
            self.price_series.append(algebra.scale(
                Priceable(type='stock', name_symbol=tick).get_price_history(price_timing=price_timing, period=period, interval=interval),
                initial=scale_start)
                )
        i=0
        for s in self.price_series:
            plt.plot(s, label=ticks[i])
            i+=1
    
    def show(self) -> None:
        plt.legend()
        plt.show()

p = ScaledPricePlot('XOM', 'CVX', 'AAPL')
p.show()

        
