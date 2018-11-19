  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import math  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
# this function should return a dataset (X and Y) that will work  		   	  			    		  		  		    	 		 		   		 		  
# better for linear regression than decision trees  		   	  			    		  		  		    	 		 		   		 		  
def best4LinReg(seed=1489683273):  		   	  			    		  		  		    	 		 		   		 		  
    np.random.seed(seed)
    X = np.random.rand(20,4)*100
    Y = X[:,0]*2 + X[:,1]*4 + X[:,2]*5 + X[:,3]*6
    return X, Y

  		   	  			    		  		  		    	 		 		   		 		  
def best4DT(seed=1489683273):  		   	  			    		  		  		    	 		 		   		 		  
    np.random.seed(seed)
    X = np.random.random(size=(15, 6))*10
    Y = np.zeros(15)
    for i in range(6):
        Y += Y + np.sin(X[:,i]**2)
    return X,Y
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "they call me Tim."  		   	  			    		  		  		    	 		 		   		 		  
