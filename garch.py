import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
# from arch.univariate import ARX, EGARCH

brentprices = pd.DataFrame.from_csv('BrentData.csv')
wtiprices = pd.DataFrame.from_csv('WTIData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
data_agg = pd.concat([data_agg, data_agg['slow_count'] + data_agg['fast_count']], axis = 1)
# data_agg = pd.concat([data_agg, data_agg['slow_count'] / (data_agg['slow_count'] + data_agg['fast_count'])], axis = 1)
data_agg = data_agg.rename(columns={ data_agg.columns[3]: "total_count" })
data_agg = data_agg.sort_index().shift(periods = -2)

brent_returns = 100 * brentprices['Returns']
data = pd.concat([brent_returns, data_agg], axis=1, join_axes=[data_agg.index])
data = data.dropna(axis =0)
#include this for the forecats with variables
# x = data[[ 'avg(avg(sog))', 'slow_count', 'fast_count']],
am = arch_model( y = data['Returns'],  mean = 'ARX', lags = 1, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')

split_date = dt.datetime(2015,6,1)
res = am.fit(last_obs = split_date)
print(res.summary())


forecasts = res.forecast(horizon = 4, start = split_date, method='bootstrap')
sims = forecasts.simulations
lines = plt.plot(sims.residual_variances[-1].T, color='#9cb2d6')
lines[0].set_label('Simulated path')
line = plt.plot(forecasts.variance.iloc[-1].values, color='#002868')
line[0].set_label('Expected variance')
legend = plt.legend()
plt.show()

lines = plt.plot(forecasts.mean)
plt.show()
