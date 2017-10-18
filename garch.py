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
fast_count = data_agg[['fast_count']].shift(periods = -2)
avg_speed = data_agg[['avg(avg(sog))']].shift(periods = -1)
brent_prices = brentprices['Adjusted Price'].shift(periods = -5)
data = pd.concat([brent_prices, avg_speed, slow_count, fast_count], axis=1, join_axes=[brent_prices.index])
data = data.dropna(axis =0)

#b. run the garch model for slow count
am = arch_model(y = data[['slow_count']],x = data[['avg(avg(sog))', 'Adjusted Price', 'fast_count']],mean = 'ARX', lags = 1, vol = 'EGARCH', p = 1, o = 1, q = 1, power = 2, dist = 'Normal')
res = am.fit()
print(res.summary())

#c. generate the forecasts for the mean
data['intercept'] = np.ones(len(data))
slow_count_lagged = slow_count.shift(periods = -1) #autoregressive term here
data = pd.concat([slow_count_lagged, data], axis=1, join_axes = [slow_count.index])
data.columns.values[0] = "slow_count_lagged"
data = data.dropna(axis = 0)
forecast = res.params[0] * data['intercept'] + res.params[1] * data['slow_count_lagged'] +  res.params[2] * data['avg(avg(sog))'] + res.params[3] * data['Adjusted Price'] + res.params[4] * data['fast_count']
forecast = forecast.shift(periods = +1)

#d. generate the forecasts for the volatility
volatility = data[['Adjusted Price']].rolling(100).var()
volatility_data = pd.concat([volatility, res.resid], axis=1, join_axes = [volatility.index])
volatility_data = volatility_data.dropna(axis = 0)
e = volatility_data['resid'] / volatility_data['Adjusted Price']
forecast_vol = np.exp(res.params[5] + res.params[6] * (abs(e) - np.sqrt(2/np.pi)) + res.params[7] * abs(e) + res.params[8] * np.log(volatility['Adjusted Price']))
forecast_vol = forecast_vol.shift(periods = +1)

forecast_final = pd.concat([forecast, forecast_vol], axis = 1, join_axes = [forecast.index])
forecast_final = forecast_final.dropna(axis = 0)
forecast_final.to_csv('forecast_final_slowcount.csv')
