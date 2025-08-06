import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Union, List, Optional

from instrument import Priceable
import series_algebra as algebra

class Display():
    def __init__(self, plotcount: int):
        self.plotcount = plotcount
        self.fig, self.display = plt.subplots(plotcount)
    
    def plot(self, 
             plot_index: int, 
             *data: Union[List, pd.Series], 
             color: Union[List[str], str] = None, 
             linestyle: Union[List[str], str] = None):
        '''
        Plots data into display index passed. Pass multiple pd.Series objects to plot x-axis respective series together.

        :param plot_index: index of plot display to plot data.
        :param data: either x,y data pair lists or 1+ pd.Series objects.
        :param color: color or list of colors if multiple series are being plotted.
        :param linestyle: linestyle or list of linestyles if multiple series are being plotted.
        '''
        # default linestyle
        if linestyle == None: linestyle='-'

        # plot x,y data pair if data has 2 args
        if len(data)==2 and (isinstance(data[0], List) and isinstance(data[1], List)):
            if color==None:
               self.display[plot_index].plot(data[0], data[1], linestyle=linestyle) 
            else:
                self.display[plot_index].plot(data[0], data[1], color=color, linestyle=linestyle)
            return True
        
        plotted = 0
        if len(data)==1 and (isinstance(data[0], pd.Series)):
            if color==None:
                self.display[plot_index].plot(data[0], linestyle=linestyle)
                return True
            else:
                self.display[plot_index].plot(data[0], color=color, linestyle=linestyle)
                return True
    
        # else assume data args are type pd.Series
        i = 0
        for dataset in data:
            # check for no reason
            if isinstance(dataset, pd.Series):
                if color==None:
                    self.display[plot_index].plot(dataset, linestyle=linestyle[i])
                else:
                    self.display[plot_index].plot(dataset, color=color[i], linestyle=linestyle[i])
                plotted+=1
                i+=1
        
        print(f"{plotted}/{len(data)} data series plotted at display index {plot_index}.")
        return True
    
    def show(self):
        self.fig.show()
        input("Press any key to close plot.")

class ComparativeModel(Display):
    def __init__(self, 
                 primary_derivative: Priceable,
                 secondary_derivative: Priceable,
                 date_period: str,
                 time_interval: str,
                 price_timing: str,
                 xy_split: bool = False,
                 momentum_indicators: Optional[bool] = False, 
                 momentum_bias: Optional[int] = None):
        super().__init__(plotcount=3)
        self.der1, self.der2 = primary_derivative, secondary_derivative
        self.period = date_period
        self.interval = time_interval
        self.der1_name, self.der2_name = primary_derivative.symbol, secondary_derivative.symbol

        # populate primary derivative price series
        self.der1_prices = primary_derivative.get_price_history(price_timing=price_timing, period=date_period, interval=time_interval)
        # in case of individual x,y plotting
        if xy_split:
            self.d1x = self.der1_prices.index.tolist()
            self.d1y = self.der1_prices.values.tolist()

        # populate secondary derivative price series
        self.der2_prices = secondary_derivative.get_price_history(price_timing=price_timing, period=date_period, interval=time_interval)
        if xy_split:
            self.d2x = self.der2_prices.index.tolist()
            self.d2y = self.der2_prices.values.tolist()
        
        # get normalized series
        self.der1_prices_normalized = algebra.normalize(self.der1_prices)
        self.der2_prices_normalized = algebra.normalize(self.der2_prices)
        
        if momentum_indicators:
            self.mmt_bias = momentum_bias

        else:
            self.plot()
        




    

        
