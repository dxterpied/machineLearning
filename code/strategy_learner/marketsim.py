
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data



def compute_portvals(order, symbol = "AAPL",start_val=1000000, commission=9.95, impact=0.005):
    dates = order.index
    prices = get_data([symbol], dates)  # SPY is added automatically and will be deleted later
    prices = prices[symbol]
    prices = prices.to_frame()
    prices['CASH'] = 1.0
    pd_traders = prices.copy()
    pd_traders[:] = 0.0

    for i in range(order.shape[0]):
        row_date = dates[i]
        row_value = order.loc[row_date]
        pd_traders.loc[row_date, symbol] = pd_traders.loc[row_date, symbol] + row_value
        dailyPrice = prices.loc[row_date, symbol]
        pd_traders.loc[row_date,'CASH'] = (-1) * dailyPrice * row_value + pd_traders.loc[row_date, 'CASH']
        # commission and impact
        pd_traders.loc[row_date, 'CASH'] = pd_traders.loc[row_date, 'CASH'] - (
                    abs(row_value) * dailyPrice * impact + commission)
    #holdings
    pd_holdings = pd_traders.copy()
    start_date = order.index[0]
    pd_holdings.loc[start_date, 'CASH'] = pd_holdings.loc[start_date, 'CASH'] + start_val
    pd_holdings = pd_holdings.cumsum()
    # create dataframe value (same structure as prices)
    pd_values = pd.DataFrame(pd_holdings.values * prices.values, columns=prices.columns, index=prices.index)
    portvals = pd_values.sum(axis=1)
    return portvals




def calculateStatistics(portvals):
    sd = portvals.index[0]
    ed = portvals.index[-1]
    dates = pd.date_range(sd, ed)

    prices = get_data(['JPM'], dates)
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='backfill', inplace=True)
    JPM_price = prices['JPM']
    normed_Price = JPM_price / JPM_price.iloc[0,]
    target_return = normed_Price/normed_Price.shift(1) - 1.0
    target_return = target_return[1:]
    return_cr = normed_Price[-1]/normed_Price[0]-1
    return_std = target_return.std()
    return_mean = target_return.mean()
    print return_cr








if __name__ == "__main__":
    # test_code()
    compute_portvals(orders_file="./orders/orders-02.csv", start_val=1000000, commission=9.95, impact=0.005)
