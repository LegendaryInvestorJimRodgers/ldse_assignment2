import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.api import VAR

brentprices = pd.DataFrame.from_csv('BrentData.csv')
wtiprices = pd.DataFrame.from_csv('WTIData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
# data_agg_lag = data_agg.shift(periods = -1)
# data_agg = data_agg - data_agg_lag
# data_agg = pd.concat([data_agg, data_agg['slow_count'] + data_agg['fast_count']], axis = 1)
# data_agg = pd.concat([data_agg, data_agg['slow_count'] / (data_agg['slow_count'] + data_agg['fast_count'])], axis = 1)
# data_agg = data_agg.rename(columns={ data_agg.columns[3]: "total_count" })
data_agg = data_agg.sort_index()#.shift(periods = -2)

brent_returns = 100 * brentprices['Returns']
brent_prices = brentprices['Adjusted Price']#.shift(periods = -1)
data = pd.concat([brent_prices, data_agg], axis=1, join_axes=[data_agg.index])
data = data.dropna(axis =0)

model = VAR(data[['Adjusted Price', 'slow_count', 'fast_count', 'avg(avg(sog))']])
res = model.fit(10)
res.plot_acorr()
plt.xlabel('August Price')
plt.ylabel('Slow Count')
plt.show()
print(res.summary())
