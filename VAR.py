import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import acf, pacf

brentprices = pd.DataFrame.from_csv('BrentData.csv')
brentprices = brentprices#.shift(periods = -3)
wtiprices = pd.DataFrame.from_csv('WTIData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_w2017.csv')
data_agg = data_agg.sort_index()#.shift(periods = -2)

brent_returns = 100 * brentprices['Returns']
data_agg = data_agg[['fast_count']]
# brent_prices = brentprices['Adjusted Price']#.shift(periods = -1)
data = pd.concat([brentprices, data_agg], axis=1, join_axes=[data_agg.index])
data = data.dropna(axis =0)

# #autocorrelation and partial autocorrelation for the prices
# plt.plot(acf(data[['Adjusted Price']]))
# plt.plot(pacf(data[['Adjusted Price']]))
# plt.show()
#
# #autocorrelation and partial autocorrelaition for slow_count
# plt.plot(acf(data[['slow_count']]))
# plt.plot(pacf(data[['slow_count']]))
# plt.show()
#
# #autocorrelation and partial autocorrelation for fast_count
# plt.plot(acf(data[['fast_count']]))
# plt.plot(pacf(data[['fast_count']]))
# plt.show()

model = VAR(data[['Adjusted Price',  'fast_count']])
print(acf(brentprices[['Adjusted Price']]))
res = model.fit()
print(res.summary())
