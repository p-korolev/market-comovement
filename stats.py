import pandas as pd
import numpy as np

from typing import Union
from numbers import Real 

def covariance(x: Union[pd.Series, np.ndarray], y: Union[pd.Series, np.ndarray]) -> Real:
    '''
    Returns the covariance between two series of data as real.

    :param x: data series of reals
    :param y: data series of reals

    **Examples**

    >>> from instrument import Priceable
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> cvx = Priceable(type='stock', name_symbol='CVX').get_price_history(price_timing='Close', period='1mo')
    >>> covariance(xom, cvx)
    1.6887381204433043
    
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> shel = Priceable(type='stock', name_symbol='SHEL').get_price_history(price_timing='Close', period='1mo')
    >>> covariance(xom, shel)
    0.5991333231946371
    '''
    return np.cov(x, y)[0][1]

def cov_matrix(*x: Union[pd.Series, np.ndarray]) -> np.ndarray[Real]:
    '''
    Returns the covariance matrix of multiple data series of reals.

    :param *x: series of reals

    **Examples**
    
    >>> from instrument import Priceable
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> cvx = Priceable(type='stock', name_symbol='CVX').get_price_history(price_timing='Close', period='1mo')
    >>> shel = Priceable(type='stock', name_symbol='SHEL').get_price_history(price_timing='Close', period='1mo')
    >>> covariance_matrix(xom, cvx, shel)
    [[4.5737686  1.61292396 0.60793976]
     [1.61292396 4.99476267 1.0364035 ]
     [0.60793976 1.0364035  0.38670407]]
    '''
    if len(x)>2:
        return np.cov(np.vstack([series for series in x]))
    return np.cov(*x)

def correlation_matrix(*x: Union[pd.Series, np.ndarray]) -> np.ndarray[Real]:
    '''
    Returns the normalized correlation matrix of multiple data series of reals.

    :param *x: series of reals

    **Examples**

    >>> from instrument import Priceable
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> cvx = Priceable(type='stock', name_symbol='CVX').get_price_history(price_timing='Close', period='1mo')
    >>> shel = Priceable(type='stock', name_symbol='SHEL').get_price_history(price_timing='Close', period='1mo')
    >>> covariance_matrix(xom, cvx, shel)
    [[1.         0.33268224 0.45317276]
     [0.33268224 1.         0.74402584]
     [0.45317276 0.74402584 1.        ]]
    '''
    cov = cov_matrix(*x)
    std_outer = np.outer((np.sqrt(np.diag(cov))), (np.sqrt(np.diag(cov))))
    return cov/std_outer

def correlation(x: Union[pd.Series, np.ndarray], y: Union[pd.Series, np.ndarray]) -> Real:
    '''
    Returns the normalized correlation of two series of reals.

    :param x: series of reals
    :param y: series of reals

    **Examples**

    >>> from instrument import Priceable
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> cvx = Priceable(type='stock', name_symbol='CVX').get_price_history(price_timing='Close', period='1mo')
    >>> correlation(x=xom, y=cvx)
    0.33420128794152715
    '''
    return correlation_matrix(x, y)[0][1]

def variance(x: Union[pd.Series, np.ndarray]) -> Real:
    '''
    Returns the variance of a series of reals.

    :param x: series of reals

    **Examples**

    >>> from instrument import Priceable
    >>> xom = Priceable(type='stock', name_symbol='XOM').get_price_history(price_timing='Close', period='1mo')
    >>> variance(xom)
    4.36387949368984
    '''
    return np.var(x)

