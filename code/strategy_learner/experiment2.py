
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

def experiment2():
    np.random.seed(gtid())
    sd = dt.date(2008, 1, 1)
    ed = dt.date(2009, 12, 31)
    dates = pd.date_range(sd, ed)
    symbol = "JPM"
    sv = 100000
    impact_list = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, \
                   0.22, 0.24, 0.26, 0.28, 0.3]
    trader_time = []
    normed_final_portval = []
    for impact in impact_list:
        testLearner = str_l.StrategyLearner(verbose=False, impact=impact)
        testLearner.addEvidence(symbol, sd, ed, sv)
        randomL_trader = testLearner.testPolicy(symbol, sd, ed, sv)
        randomL_trader = randomL_trader.iloc[:,0]
        trader_time.append(np.count_nonzero(randomL_trader))
        randomL_portvals = m_sim.compute_portvals(randomL_trader,symbol, sv, commission = 0.0,impact = impact)
        finalReturn = randomL_portvals[-1]/randomL_portvals[0]
        normed_final_portval.append(finalReturn)

    plt.xlabel('impact value')
    plt.ylabel('trade time')
    plt.xticks(np.arange(20), impact_list)
    plt.plot(trader_time)
    plt.savefig('experiment_2a.png')
    plt.clf()

    plt.xlabel('impact value')
    plt.ylabel('normed_portval_return')
    plt.xticks(np.arange(20), impact_list)
    plt.plot(normed_final_portval)
    plt.savefig('experiment_2b.png')
    plt.clf()





if __name__ == "__main__":
    experiment2()
