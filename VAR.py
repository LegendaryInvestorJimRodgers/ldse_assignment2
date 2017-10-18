import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.api import VAR

brentprices = pd.DataFrame.from_csv('BrentData.csv')
brentprices = brentprices.shift(periods = -3)
wtiprices = pd.DataFrame.from_csv('WTIData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_full.csv')
data_agg = data_agg.sort_index()#.shift(periods = -2)

brent_returns = 100 * brentprices['Returns']
brent_prices = brentprices['Adjusted Price']#.shift(periods = -1)
data = pd.concat([brent_prices, data_agg], axis=1, join_axes=[data_agg.index])
data = data.dropna(axis =0)

model = VAR(data[['Adjusted Price', 'slow_count', 'fast_count', 'avg(avg(sog))']])
res = model.fit(1)
res.plot_acorr()
plt.xlabel('August Price')
plt.ylabel('Slow Count')
plt.show()
print(res.summary())
