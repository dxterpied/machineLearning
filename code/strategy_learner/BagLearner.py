
import numpy as np
import RTLearner as rt


class BagLearner(object):

    def __init__(self, learner, kwargs={"leaf_size": 1, "verbose": False}, bags=20, boost=False, verbose=False):
        self.learner = learner
        self.bagLearners = []
        self.bags = bags
        self.kwargs = kwargs
        self.boost = boost
        self.verbose = verbose
        for i in range(self.bags):
            self.bagLearners.append(self.learner(**kwargs))

   
    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        rowNum = np.atleast_2d(dataX).shape[0]
        dataY = dataY.reshape(rowNum, 1)
        for i in range(self.bags):
            randomRows = np.random.choice(rowNum, rowNum)
            randomDataX = dataX[randomRows, :]
            randomDataY = dataY[randomRows, 0]
            self.bagLearners[i].addEvidence(randomDataX, randomDataY)

    def query(self, xtest):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        results = []
        for i in range(self.bags):
            results.append(self.bagLearners[i].query(xtest))
        return np.mean(results, axis=0)


if __name__ == "__main__":
    print "the secret clue is 'robot'"
