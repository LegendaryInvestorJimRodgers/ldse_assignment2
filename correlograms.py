import pandas as pd
import numpy as np
import scipy as sp
from arch import arch_model
import datetime as dt
import matplotlib.pyplot as plt

brentprices = pd.DataFrame.from_csv('BrentData.csv')
wtiprices = pd.DataFrame.from_csv('WTIData.csv')
data_agg = pd.DataFrame.from_csv('data_agg_full.csv')


#REMEMBER: comment out this section when you run the regression
brent_returns = 100 * brentprices['Returns']
correlation_matrices = []
correlogram_speed = []
correlogram_slow = []
correlogram_fast = []
#correlogram
for offset in range(-30, 0):
    temp = data_agg.sort_index().shift(periods = offset)
    data = pd.concat([brent_returns, temp], axis=1, join_axes=[data_agg.index])
    correlation_matrices.append(np.asarray(data.corr()))

for index in range(0, 30):
    correlogram_speed.append(correlation_matrices[index][0, 1])
    correlogram_slow.append(correlation_matrices[index][0, 2])
    correlogram_fast.append(correlation_matrices[index][0, 3])

correlogram_fast = correlogram_fast[::-1]
correlogram_slow = correlogram_slow[::-1]
correlogram_speed = correlogram_speed[::-1]
