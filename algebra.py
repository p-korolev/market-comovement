import math
import pandas as pd
import numpy as np

from numbers import Real
from typing import Union, List, Optional

def rolling_volatility(close_prices: pd.Series, window: Optional[int] = 21) -> pd.Series:
    return close_prices.pct_change().rolling(window=window).std()*np.sqrt(252)

def log(series: pd.Series) -> pd.Series:
    return np.log(series)

def avg(series: pd.Series) -> np.float64:
    return series.mean()

def rolling_avg(series: pd.Series, window: Optional[int] = 7) -> pd.Series:
    return series.rolling(window=window).mean()

def rolling_var(close_prices: pd.Series, window: Optional[int] = 21) -> pd.Series:
    return close_prices.pct_change().rolling(window=window).var()

def add_timerespective(first: pd.Series, second: Union[pd.Series, Real]) -> pd.Series:
    if isinstance(second, pd.Series):
        if second.index==first.index:
            return first+second
        else:
            raise ValueError("Indices do not match.")
    return first+second

def add(primary: pd.Series, secondary: pd.Series) -> pd.Series:
    secondary_values = secondary.values
    for i in range(len(secondary_values)):
        if i>len(primary):
            return primary
        primary.iloc[i] += secondary_values[i]
    return primary

def subtract(first: pd.Series, second: Union[pd.Series, Real]) -> pd.Series:
    if isinstance(second, pd.Series):
        if second.index==first.index:
            return first-second
        else:
            raise ValueError("Indices do not match.")
    return first-second

# todo: return series
def value_signs_diff(series: pd.Series) -> List[int]:
    signs = []
    vals = series.values
    for i in range(1, len(vals)):
        if vals[i]-vals[i-1]>0:
            signs.append(1)
        else:
            signs.append(-1)
    return signs

# todo: return series
def value_diff(series: pd.Series) -> List[int]:
    diff = []
    vals = series.values 
    for i in range(1, len(vals)):
        diff.append(vals[i]-vals[i-1])
    return diff

def normalize(series: pd.Series) -> pd.Series:
    return (series-series.min())/(series.max()-series.min())


