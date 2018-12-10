
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import manual_strategy as m_str
import marketsim as m_sim
import StrategyLearner as str_l


def gtid():
	return 903369999

def experiment1():
    np.random.seed(gtid())
    sd = dt.date(2008, 1, 1)
    ed = dt.date(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    symbol = "AAPL"
    sv = 100000

    # manual strategy
    manual_trader = m_str.testPolicy(symbol, sd, ed, sv)
    manual_portvals = m_sim.compute_portvals(manual_trader, symbol, sv, commission=0.0, impact=0.0)



    #machine learning based strategy
    testLearner = str_l.StrategyLearner(verbose=False, impact=0.0)
    testLearner.addEvidence(symbol, sd, ed, sv)
    randomL_trader = testLearner.testPolicy(symbol, sd, ed, sv)
    randomL_trader = randomL_trader.iloc[:,0]
    randomL_portvals = m_sim.compute_portvals(randomL_trader,symbol, sv, commission = 0.0,impact =0.0)

    # print manual_trader.shape, type(manual_trader)
    # print randomL_trader.shape, type(randomL_trader)
    # import pdb
    # pdb.set_trace()
    # plot the manual and random_learning based fig
    experiment1Fig = manual_portvals.plot(title = 'experiment 1', label = 'manual strategy')
    randomL_portvals.plot(label= 'learning strategy', ax = experiment1Fig )

    experiment1Fig.set_xlabel('Date')
    experiment1Fig.set_ylabel('portvals')
    experiment1Fig.legend(loc = 'lower right')
    plt.savefig('experiment_1.png')
    plt.clf()







if __name__ == "__main__":
    experiment1()




