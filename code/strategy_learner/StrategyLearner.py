
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd
import RTLearner as rt
import BagLearner as bl
import indicators as ind
import numpy as np
import util as ut

class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact
        self.leaf_size = 5
        self.window = 15
        self.N = 10
        self.learner = bl.BagLearner(rt.RTLearner, kwargs={"leaf_size": 5, "verbose": False}, bags=20,\
                       boost = False, verbose = False)

  		   	  			    		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "AAPL", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000):
        # add your code to do learning here
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        target_price = prices[symbol]

        x_bb = ind.bolling_bands(target_price,self.window).values
        x_ema = ind.ema(target_price,self.window).values
        x_mm = ind.momentum(target_price,self.window).values

        train_X = []
        train_Y = []
        for i in range(self.window + self.leaf_size + 1, len(target_price) - self.N):
            train_X.append(np.concatenate((x_ema[i - self.leaf_size: i], x_bb[i - self.leaf_size: i], x_mm[i - self.leaf_size: i])))
            return_NDay = (target_price.values[i + self.N] - target_price.values[i]) / target_price.values[i]
            YBUY = 0.05
            YSELL = -0.05
            if return_NDay > YBUY+self.impact:
                train_Y.append(1)
            elif return_NDay < YSELL+self.impact:
                train_Y.append(-1)
            else:
                train_Y.append(0)

        X = np.array(train_X)
        Y = np.array(train_Y)
        # print train_Y
        self.learner.addEvidence(X, Y)

    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        # here we build a fake set of trades  		   	  			    		  		  		    	 		 		   		 		  
        # code should return the same sort of data
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        target_price = prices[symbol]
        x_bb = ind.bolling_bands(target_price, self.window)
        x_ema = ind.ema(target_price, self.window)
        x_mm = ind.momentum(target_price, self.window)

        test_X = []
        for i in range(self.window + self.leaf_size + 1, len(target_price) - self.N):
            test_X.append(np.concatenate((x_ema[i - self.leaf_size: i], x_bb[i - self.leaf_size: i], x_mm[i - self.leaf_size: i])))

        prediction = self.learner.query(np.array(test_X))
        sym =[symbol]
        trader_y = prices[sym].copy()
        trader_y.values[:,:] = 0
        holding = 0
        # print prediction
        for i in range(len(prediction)):
            if prediction[i] <0:
                trader_y.values[i + self.window + self.leaf_size + 1, :] = -1000-holding
                holding = -1000
            elif prediction[i] >0:
                trader_y.values[i + self.window + self.leaf_size + 1, :] = 1000 -holding
                holding = 1000
        return trader_y
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":
    testLearner = StrategyLearner(verbose = False, impact=0.0)
    testLearner.addEvidence( symbol = "AAPL", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000)
    testMatrix = testLearner.testPolicy(symbol = "AAPL", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000)
    print testMatrix
