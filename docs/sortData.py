__author__ = 'Wessel Klijnsma'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data_agg_full.csv")
df.sort_values(by='date').to_csv('data_agg_full.csv')