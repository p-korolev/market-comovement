# Hidden markov model for projections and hidden parameter collection

import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np
import ta
from hmmlearn.hmm import GaussianHMM
from typing import Union
from numbers import Real

import algebra
from instrument import Priceable
from static_types.quoteables import LOADABLE
from static_types.quote_timing import QuoteTiming
from static_types.time_range import Period, Interval

class HMM:
    '''
    Sorts price movement into Hidden_State events based on given amount of hidden_states, training params, and other priceables.

    Includes display() method that displays prices against market state.

    **General dataframe object**

    >>> from model import HMM
    >>> from static_types.time_range import Period, Interval
    >>> makov_mod = HMM('CVX', 'XOM', hidden_states = 3, data_period=Period.DAY, quote_interval=Interval.MINUTE)
    >>> markov_mod.frame
                                CVX QuoteTiming.CLOSE  XOM QuoteTiming.CLOSE  Return CVX  Return XOM  Hidden_State
    Datetime
    2025-08-25 09:30:00-04:00             157.710007             110.760002    0.000000    0.000000             2
    2025-08-25 09:31:00-04:00             157.805603             110.940002    0.000606    0.001625             1
    2025-08-25 09:32:00-04:00             157.710007             110.989998   -0.000606    0.000451             2
    2025-08-25 09:33:00-04:00             157.669998             110.775002   -0.000254   -0.001937             1
    2025-08-25 09:34:00-04:00             157.740005             111.000000    0.000444    0.002031             2
    ...
    2025-08-25 10:32:00-04:00             157.470001             111.209999    0.000032   -0.000090             1
    2025-08-25 10:33:00-04:00             157.419998             111.214996   -0.000318    0.000045             2
    2025-08-25 10:34:00-04:00             157.440002             111.239998    0.000127    0.000225             1
    2025-08-25 10:35:00-04:00             157.365005             111.190002   -0.000476   -0.000449             2
    2025-08-25 10:36:00-04:00             157.360001             111.169998   -0.000032   -0.000180             1
    [67 rows x 5 columns]


    '''
    def __init__(self,
                 *ticks_dependent: str,
                 hidden_states: int,
                 covariance_type: str = "full",
                 iter: int = 1000,
                 quote_timing: Union[QuoteTiming, str] = QuoteTiming.CLOSE, 
                 data_period: Union[Period, str] = Period.DAY, 
                 quote_interval: Union[Interval, str] = Interval.MINUTE
                ) -> None:
        '''
        Initiate Hidden Markov Model.

        :param ticks_dependent: correlated tickers of priceables as string
        :param hidden_states: number of hidden states for model
        :param covariance_type: diag or full
        :param iter: number of iterations for learning
        :param quote_timing: Open, Close, High, Low
        :param data_period: period for data lookback
        :param quote_interval: interval between quotes during lookback period
        '''
        if hidden_states<1:
            raise ValueError(
                "Model requires at least 1 hidden state for fitting."
                )
        self.primary_tick = ticks_dependent[0]
        self.states_amt = hidden_states
        self.cov_type = covariance_type
        self.iter_amt = iter

        priceables = [Priceable(type=LOADABLE.STOCK, name_symbol=tick) for tick in ticks_dependent]
        price_series = [p.get_price_history(period=data_period, interval=quote_interval, price_timing=quote_timing) for p in priceables]
        self.frame = pd.concat(price_series, axis=1)
        for i in range(len(ticks_dependent)):
            self.frame[f'Return {ticks_dependent[i]}'] = price_series[i].pct_change().fillna(0)
        
        self.features = self.frame.filter(like="Return").values
    
    def fit_priceables(self) -> None:
        self.model = GaussianHMM(n_components=self.states_amt, covariance_type=self.cov_type, n_iter = self.iter_amt)
        self.model.fit(self.features)
        self.frame['Hidden_State'] = self.model.predict(self.features)
    
    def infer_states(self) -> None:
        pass

    def display(self):
        '''
        Plot show method that displays prices and hidden states.
        '''
        for i in range(self.model.n_components):
            state_data = self.frame[self.frame['Hidden_State']==i]
            plt.plot(state_data.index, state_data.iloc[:, 0], '.', label=f"State {i}")
        plt.plot(self.frame.index, self.frame.iloc[:, 0], label='Prices')
        plt.title(f"{self.primary_tick} Price Colored by Inferred Regimes")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

        


