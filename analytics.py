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
from static_types.sector_tracker import SectorName, SectorTick

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
                 interval: Union[Interval, str] = Interval.MINUTE
                 ):
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

class ScaledPricePlot:
    def __init__(self, 
                 *ticks: str, 
                 price_timing: Union[QuoteTiming, str] = QuoteTiming.OPEN,
                 period: Union[Period, str] = Period.DAY,
                 interval: Union[Interval, str] = Interval.MINUTE,
                 scale_start: Real = 100
                 ):
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

from static_types.quoteables import LOADABLE
class CompareStatDisplay:
    def __init__(self, 
                 leader: str, 
                 follower: str,
                 period: Union[Period, str] = '1d',
                 interval: Union[Interval, str] = '1m',
                 quote_timing: Union[QuoteTiming, str] = QuoteTiming.CLOSE,
                 mal_window: Union[int, None] = None,
                 maf_window: Union[int, None] = None
                 ):
        self.per = period
        self.intr = interval
        self.fig, self.axs = plt.subplots(2,1)

        l_prices_scaled = algebra.scale(
            Priceable(type=LOADABLE.STOCK, name_symbol=leader).get_price_history(period=period, interval=interval, price_timing=quote_timing), 
            initial=100
            )
        f_prices_scaled = algebra.scale(
            Priceable(type=LOADABLE.STOCK, name_symbol=follower).get_price_history(period=period, interval=interval, price_timing=quote_timing), 
            initial=100
            )
        
        self.axs[0].plot(l_prices_scaled, label=f'{leader}', color='mediumblue')
        self.axs[0].plot(f_prices_scaled, label=f'{follower}', color='orange')

        if mal_window != None:
            mal = algebra.rolling_avg(l_prices_scaled, window=mal_window)
            self.axs[0].plot(mal, label=f'{leader} Moving Avg', color='skyblue')
        if maf_window != None:
            maf = algebra.rolling_avg(f_prices_scaled, window=maf_window)
            self.axs[0].plot(maf, label=f'{follower} Moving Avg')
        
        self.axs[1].plot(algebra.difference(l_prices_scaled, f_prices_scaled), label='L - F Diff', color='lightcoral')
        self.axs[1].hlines(y=0, xmin=l_prices_scaled.index[0], xmax=l_prices_scaled.index[-1], color='black', linestyle='-')

    def plot_sector_index(self, sector_index_tick: Union[SectorTick, str], quote_timing: Union[QuoteTiming, str]):
        load = Priceable(type='stock', name_symbol=sector_index_tick)
        price_series = load.get_price_history(period=self.per, interval=self.intr, price_timing=quote_timing)
        self.axs[0].plot(algebra.scale(price_series), color='gray', label='Sector Index Price')


    def show(self):
        self.axs[0].legend()
        self.axs[1].legend()
        plt.show()
