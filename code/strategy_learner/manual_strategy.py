
import pandas as pd
import numpy as np
import datetime as dt
import os
from marketsim import compute_portvals
from marketsim import calculateStatistics
from util import get_data, plot_data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import RTLearner as rt
import BagLearner as bl
import indicators as ind
import util as ut


def testPolicy(symbol, sd, ed, sv=100000):
    window = 15
    leaf_size = 5
    N = 10
    prices = ut.get_data([symbol], pd.date_range(sd, ed))
    target_price = prices[symbol]
    x_bb = ind.bolling_bands(target_price, window).values
    x_ema = ind.ema(target_price, window).values
    x_mm = ind.momentum(target_price, window).values
    pd_traders = target_price.copy()
    pd_traders[:] = 0.0


    holding = 0
    for i in range(window, len(target_price)):
        if (x_bb[i] > 1) or (x_mm[i] < -0.07) or (x_ema[i] > 0.1):
            pd_traders.values[i] = -1000 - holding
            holding = -1000
            # print holding
        elif (x_bb[i] < -1) or (x_mm[i] > 0.014) or (x_ema[i] < -0.1):
            pd_traders.values[i] = 1000 - holding
            holding = 1000
    return pd_traders





if __name__ == "__main__":
    sd = dt.date(2008, 1, 1)
    ed = dt.date(2009, 12, 31)
    pdd = testPolicy(symbol='JPM', sd = sd, ed = ed, sv = 100000)

    portvals = compute_portvals(pdd,symbol='JPM',start_val=100000, commission=0.0, impact=0.0)





