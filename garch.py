import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
from arch.univariate import ARX, EGARCH, base


#1. GARCH Model for slow count
#a. getting data and putting it into different variables
brentprices = pd.DataFrame.from_csv('BrentData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
data_agg = data_agg.sort_index()
slow_count = data_agg[['slow_count']]
fast_count = data_agg[['fast_count']].shift(periods = -1)
avg_speed = data_agg[['avg(avg(sog))']].shift(periods = -1)
brent_prices = brentprices['Adjusted Price'].shift(periods = -10)
data = pd.concat([brent_prices, data_agg, slow_count, fast_count], axis=1, join_axes=[brent_prices.index])
data = data.dropna(axis =0)

#b. run the garch model for slow count
am = arch_model(y = data[['slow_count']],x = data[['avg(avg(sog))', 'Adjusted Price']],mean = 'ARX', lags = 1, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')
res = am.fit()
print(res.summary())
#print(res.params[0:6])
#
# #2. GARCH Model for fast count
# #a. getting data and putting it into different variables
# brentprices = pd.DataFrame.from_csv('BrentData.csv')
# data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
# data_agg = data_agg.sort_index()
# slow_count = data_agg[['slow_count']].shift(periods = -1)
# fast_count = data_agg[['fast_count']]
# avg_speed = data_agg[['avg(avg(sog))']].shift(periods = -1)
# brent_prices = brentprices['Adjusted Price'].shift(periods = -10)
# data = pd.concat([brent_prices, slow_count, fast_count, avg_speed], axis=1, join_axes=[data_agg.index])
# data = data.dropna(axis =0)
#
# #b. run the garch model for slow count
# am = arch_model(y = data[['fast_count']],x = data[['avg(avg(sog))', 'Adjusted Price']],mean = 'ARX', lags = 1, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')
# res = am.fit()
# print(res.summary())
# #print(res.params[0:6])

# #3. GARCH Model for average speed
# #a. getting data and putting it into different variables
# brentprices = pd.DataFrame.from_csv('BrentData.csv')
# data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
# data_agg = data_agg.sort_index()
# slow_count = data_agg[['slow_count']].shift(periods = -1)
# fast_count = data_agg[['fast_count']].shift(periods = -1)
# avg_speed = data_agg[['avg(avg(sog))']]
# brent_prices = brentprices['Adjusted Price'].shift(periods = -1)
# data = pd.concat([brent_prices, slow_count, fast_count, avg_speed], axis=1, join_axes=[data_agg.index])
# data = data.dropna(axis =0)
#
# #b. run the garch model for slow count
# am = arch_model(y = data[['avg(avg(sog))']],x = data[['fast_count','slow_count', 'Adjusted Price']],mean = 'ARX', lags = 1, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')
# res = am.fit()
# print(res.summary())
# #print(res.params[0:6])
