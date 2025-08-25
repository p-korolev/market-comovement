# Module for various analytic plot displays #

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from typing import Union, Any
from numbers import Real 

import stats
import algebra
from instrument import Priceable
from static_types.quoteables import LOADABLE
from static_types.quote_timing import QuoteTiming
from static_types.time_range import Interval, Period

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
                 price_timing: Union[QuoteTiming, str] = QuoteTiming.OPEN,
                 period: Union[Period, str] = Period.DAY,
                 interval: Union[Interval, str] = Interval.MINUTE):
    '''
    Plot display class to plot price time series of priceables (*ticks) against one another - NOT SCALED.

    **Usage**

    Display prices as time series of stock S.

    **Examples**

    >>> enb_price = PricePlot('ENB', price_timing=QuoteTiming.CLOSE, period=Period.FIVE_DAY, interval=Interval.HOUR)
    >>> enb_price.show() #displays time series chart

    >>> enb_cvx_prices_day_seconds = PricePlot('ENB', 'CVX', price_timing=QuoteTiming.OPEN)
    >>> enb_cvx_prices_day_seconds.show() #displays ENB raw prices against CVX for last day, by seconds
    '''
        self.price_series = []
        for tick in ticks:
            self.price_series.append(
                Priceable(type=LOADABLE.STOCK, name_symbol=tick).get_price_history(price_timing=price_timing, period=period, interval=interval)
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
                 price_timing: Union[QuoteTming, str] = QuoteTiming.OPEN,
                 period: Union[Period, str] = Period.DAY,
                 interval: Union[Interval, str] = Interval.MINUTE,
                 scale_start: Real = 100):
        '''
        Plot display class to plot prices scaled to *scale_start* as time series of priceables (*ticks).

        **Usage**
    
        Compare prices of stock X_1 against stock X_2. See differential between two or more priceables instruments.
    
        **Examples**
    
        >>> enb_cvx_prices_scaled = ScaledPricePlot('ENB', 'CVX', price_timing=QuoteTiming.CLOSE, period=Period.FIVE_DAY, interval=Interval.HOUR)
        >>> enb_cvx_prices_scaled.show()
        '''
        self.price_series = []
        for tick in ticks:
            self.price_series.append(
                algebra.scale(
                Priceable(type=LOADABLE.STOCK, name_symbol=tick).get_price_history(price_timing=price_timing, period=period, interval=interval),
                initial=scale_start)
                )
        i=0
        for s in self.price_series:
            plt.plot(s, label=ticks[i])
            i+=1
    
    def show(self) -> None:
        plt.legend()
        plt.show()




