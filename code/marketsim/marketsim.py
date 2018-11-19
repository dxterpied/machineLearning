   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
 		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders-01.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    #1)Read in Orders file, the date is the index
    df_order = pd.read_csv(orders_file,index_col= 'Date', parse_dates= True, na_values=['nan'])
    #2)sort by dates in orders file
    df_order = df_order.sort_index()
    dates = pd.date_range(df_order.index[0], df_order.index[-1])
    symbol_list = df_order['Symbol'].unique().tolist()
    #3)build data frame prices (adjusted close). get all distinct symbols, use get_data and add cash column (all ones)
    prices = get_data(symbol_list, dates)#SPY is added automatically and will be deleted later
    prices.fillna(method='ffill',inplace = True)
    prices.fillna(method='backfill',inplace = True)
    prices = prices[symbol_list]
    prices['CASH'] = 1.0
    # print(type(prices))
    # import pdb
    # pdb.set_trace()
    #4)create data frame traders (same structure as prices)
    pd_traders = prices.copy()
    pd_traders[:] = 0.0
    for row_date, row_value in df_order.iterrows():
        if row_value['Order'] == 'BUY':
            traderShare = 1*row_value['Shares']
        else:
            traderShare = (-1)*row_value['Shares']
        traderStock = row_value['Symbol']
        pd_traders.loc[row_date,traderStock] = pd_traders.loc[row_date,traderStock] + traderShare
        dailyPrice = prices.loc[row_date,traderStock]
        pd_traders.loc[row_date,'CASH'] = (-1)*dailyPrice*traderShare + pd_traders.loc[row_date,'CASH']
        #commission and impact
        pd_traders.loc[row_date,'CASH'] = pd_traders.loc[row_date,'CASH'] - (abs(traderShare)*dailyPrice*impact+commission)
    #5) create data frame holdings (same structure as prices)
    pd_holdings = pd_traders.copy()
    start_date = df_order.index[0]
    pd_holdings.loc[start_date,'CASH'] = pd_holdings.loc[start_date,'CASH'] + start_val
    pd_holdings = pd_holdings.cumsum()
    #6) create dataframe value (same structure as prices)
    pd_values = pd.DataFrame(pd_holdings.values * prices.values,columns=prices.columns, index = prices.index)
    portvals = pd_values.sum(axis = 1)
    return portvals
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    compute_portvals(orders_file="./orders/orders-02.csv", start_val=1000000, commission=9.95, impact=0.005)
