# Module to store formalized sector ticker/names trackers #

from enum import Enum

class SectorTick(str, Enum):
    # tickers for S&P sector trackers
    ENERGY = 'XLE'
    TECH = 'XLK'
    HEALTH = 'XLV'
    FINANCE = 'XLF'
    IND = 'XLI'
    MAT = 'XLB'
    UTIL = 'XLU'
    COMM = 'XLC'
    RSTATE = 'XLRE'
    CONDIS = 'XLY'
    CONSTP = 'XLP'

class SectorName(str, Enum):
    ENERGY = 'Energy'
    TECH = 'Technology'
    HEALTH = 'Healthcare'
    FINANCE = 'Financials'
    IND = 'Indurials'
    MAT = 'Materials'
    UTIL = 'Utilities'
    COMM = 'Communication'
    RSTATE = 'Real Estate'
    CONDIS = 'Consumer Discretionary'
    CONSTP = 'Consumer Staples'