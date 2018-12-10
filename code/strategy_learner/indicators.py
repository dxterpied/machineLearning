import pandas as pd
import numpy as np
import datetime as dt
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from util import get_data, plot_data


def movingAverage (prices, lookback):
    return prices.rolling(lookback).mean()

def sma_index (prices,lookback):
    rm = prices.rolling(lookback).mean()
    index = (prices - rm)/rm
    return index



def movingStd (prices, lookback):
    return prices.rolling(lookback).std()

def bandsValue (moving_Mean, moving_Std):
    upper = moving_Mean + 2*moving_Std
    lower = moving_Mean - 2*moving_Std
    return upper, lower

def bolling_bands (target_price, window):
    normed_price = target_price / target_price.iloc[0,]
    moving_Mean = movingAverage(normed_price, window)
    moving_Std = movingStd(normed_price,window)
    result = (normed_price-moving_Mean)/(2 * moving_Std)
    return result


def ema(target_price, window):
    normed_price = target_price / target_price.iloc[0,]
    ema = normed_price.copy()
    ema[window] = np.mean(ema[0:window]-1)
    weight_factor = 2.0 / (window + 1)
    for i in range(window+1, len(ema)):
        ema[i] = ema[i - 1] + weight_factor * (normed_price[i] - ema[i - 1])
    ema_index = (normed_price - ema) / ema
    return ema_index


def momentum (target_price, window):
    result = target_price/target_price.shift(window) - 1
    return result


if __name__ == "__main__":
    # get the normed JPM data
    sd = dt.date(2008,1,1)
    ed = dt.date(2009,12,31)
    dates = pd.date_range(sd, ed)
    lookback = 15
    prices = get_data(['JPM'],dates)
    JPM_price = prices['JPM']
    normed_Price = JPM_price/JPM_price.iloc[0,]

    print bolling_bands(normed_Price,10)





