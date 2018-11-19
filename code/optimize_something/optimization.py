		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as spo


	   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1),
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    prices = prices.fillna(method="ffill", )
    prices = prices.fillna(method="bfill")


    # find the allocations for the optimal portfolio
    size = len(syms)
    allocsGuess = np.ones(size)/size
    bds = tuple((0,1) for i in range(size))
    cons = ({'type' : 'eq', 'fun': lambda inputs:1 - np.sum(inputs)})

    def assess_portfolio(prices, allocs):
        # Assess a portfolio
        sv = 1000000
        sf = 252
        rfr = 0
        normedPrices = prices / prices.iloc[0, :]
        normedAllocated = normedPrices * allocs * sv
        port_val = normedAllocated.sum(axis=1)
        cr = port_val[-1] / port_val[0] - 1  # cumulative return
        dailyReturn = port_val / port_val.shift() - 1
        dailyReturn = dailyReturn[1:]
        adr = dailyReturn.mean()  # average daily return
        sddr = dailyReturn.std()  # daily return standard deviation
        sr = math.sqrt(sf) * (dailyReturn - rfr).mean() / sddr  # sharpe ratio
        return [sr, sddr, adr, cr]

    def neg_sharpeRatio(allocs):
        a = (-1) * assess_portfolio(prices, allocs)[0]
        return a

    res = spo.minimize(neg_sharpeRatio, allocsGuess, method= 'SLSQP', bounds=bds,constraints=cons)
    allocs = res.x
    [sr, sddr, adr, cr] = assess_portfolio(prices,allocs)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        normedPrices = prices / prices.iloc[0, :]
        normedAllocated = normedPrices * allocs
        port_val = normedAllocated.sum(axis=1)
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df_temp / df_temp.iloc[0, :]
        plot_data(df_temp, title="Daily Portforlio Value and SPY", xlabel="Date", ylabel="Normalized price")
        pass

    return [allocs,cr,adr, sddr, sr]
  		   	  			    		  		  		    	 		 		   		 		  

  		   	  			    		  		  		    	 		 		   		 		  



def test_code():		   	  			    		  		  		    	 		 		   		 		 
    allocs, cr, adr, sddr, sr = \
    optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),
                         syms=['GOOG', 'AAPL', 'GLD', 'XOM'], gen_plot=False)
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']
    optimize_portfolio(sd=start_date, ed=end_date,
                       syms=['IBM', 'X', 'GLD', 'JPM'], gen_plot=True)

    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", allocs
    print "Sharpe Ratio:", sr  		   	  			    		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return:", adr  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return:", cr  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  	   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
