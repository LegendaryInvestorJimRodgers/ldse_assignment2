__author__ = 'Wessel Klijnsma'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../pos_agg_full.csv")

df = df[df.date != 'date'].sort_values(by='date')
print(df.to_json('positions.json', orient='records'))
