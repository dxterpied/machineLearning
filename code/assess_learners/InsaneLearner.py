  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import sys
import BagLearner as bl

#The defined API
#import InsaneLearner as it
# learner = it.InsaneLearner(verbose = False) # constructor
# learner.addEvidence(Xtrain, Ytrain) # training step
# Y = learner.query(Xtest) # query

class InsaneLearner(object):
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False):
        self.learners = []
        self.verbose = verbose
        for i in range(20):
            self.learners.append(bl.BagLearner(lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = True))
		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			    		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			    		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			    		  		  		    	 		 		   		 		  
        """
        for i in range(20):
            self.learners[i].addEvidence(dataX, dataY)


    def query(self,xtest):
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			    		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			    		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			    		  		  		    	 		 		   		 		  
        """
        results = []
        for i in range(20):
            results.append(self.learners[i].query(xtest))
        return np.mean(results,axis = 0)


if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"  		   	  			    		  		  		    	 		 		   		 		  
