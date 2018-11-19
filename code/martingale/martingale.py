		  		  		    	 		 		   		 		    		   	  			    		  		  		    	 		 		   		 		  import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
 		   	  			    		  		  		    	 		 		   		 		  
def gtid():  		   	  			    		  		  		    	 		 		   		 		  
	return 777777777 
  		   	  			    		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		   	  			    		  		  		    	 		 		   		 		  
	result = False
	a = np.random.random()
	if  a <= win_prob:
		result = True  		   	  			    		  		  		    	 		 		   		 		  
	return result
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
	win_prob = 18.0/38 # set appropriately to the probability of a win
	np.random.seed(gtid()) # do this only once

	#run experiment_1 10 times
	winnings = simpleSimulator(10,win_prob)

	#draw experiment_1_Fig.1
	x = np.arange(0, 1001)
	y0 = winnings[:, 0]
	y1 = winnings[:, 1]
	y2 = winnings[:, 2]
	y3 = winnings[:, 3]
	y4 = winnings[:, 4]
	y5 = winnings[:, 5]
	y6 = winnings[:, 6]
	y7 = winnings[:, 7]
	y8 = winnings[:, 8]
	y9 = winnings[:, 9]
	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.plot(x, y0, label='bet1')
	plt.xlabel('spin times')
	plt.ylabel('winnings')
	plt.title('experiment_1_Fig.1')
	plt.plot(x, y1, label='bet2')
	plt.plot(x, y2, label='bet3')
	plt.plot(x, y3, label='bet4')
	plt.plot(x, y4, label='bet5')
	plt.plot(x, y5, label='bet6')
	plt.plot(x, y6, label='bet7')
	plt.plot(x, y7, label='bet8')
	plt.plot(x, y8, label='bet9')
	plt.plot(x, y9, label='bet10')
	legend = plt.legend(loc='lower right')
	plt.savefig('experiment_1_Fig.1.png')
	plt.clf()

	#run experiment_1 1000 times
	winnings = simpleSimulator(1000,win_prob)

	# draw experiment_1 Fig.2
	x = np.arange(0, 1001)
	y1 = np.zeros(1001)
	y2 = np.zeros(1001)
	y3 = np.zeros(1001)

	for i in range(1,1001):
		y1[i] = np.mean(winnings[i,:])
		y2[i] = np.mean(winnings[i,:]) + np.std(winnings[i,:])
		y3[i] = np.mean(winnings[i,:]) - np.std(winnings[i,:])

	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.plot(x, y1, label='mean')
	plt.xlabel('spin times')
	plt.ylabel('winnings')
	plt.title('experiment_1_Fig.2')
	plt.plot(x, y2, label='mean+std')
	plt.plot(x, y3, label='mean-std')
	legend = plt.legend(loc='lower right')
	plt.savefig('experiment_1_Fig.2.png')
	plt.clf()


	# draw experiment_1 Fig.3

	for i in range(1, 1001):
		y1[i] = np.median(winnings[i, :])
		y2[i] = np.median(winnings[i, :]) + np.std(winnings[i, :])
		y3[i] = np.median(winnings[i, :]) - np.std(winnings[i, :])

	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.plot(x, y1, label='median')
	plt.xlabel('spin times')
	plt.ylabel('winnings')
	plt.title('experiment_1_Fig.3')
	plt.plot(x, y2, label='median+std')
	plt.plot(x, y3, label='median-std')
	legend = plt.legend(loc='lower right')
	plt.savefig('experiment_1_Fig.3.png')
	plt.clf()

	# run experiment_2 1000 times
	winnings = actualSimulator(1000, win_prob)

	# draw experiment_2 Fig.4
	for i in range(1, 1001):

		y1[i] = np.mean(winnings[i, :])
		y2[i] = np.mean(winnings[i, :]) + np.std(winnings[i, :])
		y3[i] = np.mean(winnings[i, :]) - np.std(winnings[i, :])

	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.plot(x, y1, label='median')
	plt.xlabel('spin times')
	plt.ylabel('winnings')
	plt.title('experiment_2_Fig.4')
	plt.plot(x, y2, label='mean+std')
	plt.plot(x, y3, label='mean-std')
	legend = plt.legend(loc='lower right')
	plt.savefig('experiment_2_Fig.4.png')
	plt.clf()

	# draw experiment_2 Fig.5
	for i in range(1, 1001):
		y1[i] = np.median(winnings[i, :])
		y2[i] = np.median(winnings[i, :]) + np.std(winnings[i, :])
		y3[i] = np.median(winnings[i, :]) - np.std(winnings[i, :])


	plt.xlim(0, 300)
	plt.ylim(-256, 100)
	plt.plot(x, y1, label='median')
	plt.xlabel('spin times')
	plt.ylabel('winnings')
	plt.title('experiment_2_Fig.5')
	plt.plot(x, y2, label='median+std')
	plt.plot(x, y3, label='median-std')
	legend = plt.legend(loc='lower right')
	plt.savefig('experiment_2_Fig.5.png')
	plt.clf()


def simpleSimulator(times,win_prob):
	winnings = np.zeros((1001,times))
	for i in range (times):
		episode_winnings = 0
		bet_amount = 1
		for j in range(1,1001):
			if get_spin_result(win_prob):
				episode_winnings = episode_winnings + bet_amount
				bet_amount = 1
			else:
				episode_winnings = episode_winnings - bet_amount
				bet_amount = bet_amount * 2
			if episode_winnings < 80:
				winnings[j,i] = episode_winnings
			else:
				for j in range(j, 1001):
					winnings[j,i] = 80
				break
	return winnings

def actualSimulator(times,win_prob):
	winnings = np.zeros((1001,times))
	for i in range (times):
		episode_winnings = 0
		bet_amount = 1
		for j in range(1,1001):
			if get_spin_result(win_prob):
				episode_winnings = episode_winnings + bet_amount
				bet_amount = 1
			else:
				episode_winnings = episode_winnings - bet_amount
				bet_amount = bet_amount * 2
				if bet_amount > episode_winnings:
					bet_amount = episode_winnings
			if episode_winnings < 80 and episode_winnings > -256:
				winnings[j,i] = episode_winnings
			elif episode_winnings > 80:
				for j in range(j, 1001):
					winnings[j,i] = 80
				break
			else:
				for j in range(j, 1001):
					winnings[j, i] = -256
				break
	return winnings

  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
