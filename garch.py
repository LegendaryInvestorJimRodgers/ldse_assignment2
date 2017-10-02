import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt
# from arch.univariate import ARX, EGARCH

brentprices = pd.DataFrame.from_csv('BrentData.csv')
wtiprices = pd.DataFrame.from_csv('WTIData.csv')

brent_returns = 100 * brentprices['Returns']

am = arch_model(brent_returns, mean = 'ARX', lags = 2, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')

split_date = dt.datetime(2014,1,1)
res = am.fit(last_obs = split_date)
print(res.summary())
forecasts = res.forecast(horizon = 1, start = split_date)
forecasts.variance[split_date:].plot()
forecasts.mean[split_date:].plot()
plt.show()
