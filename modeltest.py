import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from instrument import Priceable
from instrument import Instrument
import series_algebra as algebra

lead = Priceable(Instrument(type='stock', name_symbol='XOM'))
mid = Priceable(Instrument(type='stock', name_symbol='PSX'))

period, interval = '1d', '1m'
lead_prices = lead.get_price_history(price_timing='Open', period=period, interval=interval)
mid_prices = mid.get_price_history(price_timing='Open', period=period, interval=interval)

lead_normalized = (lead_prices-lead_prices.min())/(lead_prices.max()-lead_prices.min())
mid_normalized = (mid_prices-mid_prices.min())/(mid_prices.max()-mid_prices.min())

# momentum signs ([-1, 1, 1, 1]) for loss, gain, gain, gain between price[i] and price[j]
lead_momentum = algebra.value_signs_diff(lead_prices)
mid_momentum = algebra.value_signs_diff(mid_prices)
# goal to plot this as a 2D walk
lead_walk, mid_walk = [0], [0]
walk_loc = 0
for x in lead_momentum:
    walk_loc += x
    lead_walk.append(walk_loc)

walk_loc=0
for x in mid_momentum:
    walk_loc += x
    mid_walk.append(walk_loc)

fig, sz = plt.subplots(3)
# plot normalized prices on [0,1] in plot_0
sz[0].plot(lead_normalized, color='blue')
sz[0].plot(mid_normalized, color='green')
# plot prices in plot_1
sz[1].plot(lead_prices, color='blue')
sz[1].plot(mid_prices, color='green')

sz[2].plot(lead_walk, color='blue', marker='o')
sz[2].plot(mid_walk, color='green', marker='o')
#plt.ylim(min(lead_prices.min(), mid_prices.min()), max(lead_prices.max(), mid_prices.max()))
plt.show()

