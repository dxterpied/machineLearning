
import numpy as np


class RTLearner(object):
    # codes are in the numPy
    def __init__(self, leaf_size, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.root = None
        self.tree = None

    def buildTree(self, dataX, dataY):
        dataX = np.atleast_2d(dataX)
        # if subtree size is less than the leaf_size or all x or y values are the same, return the leaf
        if dataX.shape[0] <= self.leaf_size or len(np.unique(dataY)) == 1 or len(np.unique(dataX)) == 1:
            return np.array([[-1, np.mean(dataY), -1, -1]])
        else:
            # else determine the feature randomly, select the factor position index and then splitvalue
            range = dataX.shape[1]
            featureIndex = np.random.randint(range)
            splitValue = np.median(dataX[:, featureIndex])
            # select the remaining data of the left and right sub-trees
            left = dataX[:, featureIndex] <= splitValue
            right = dataX[:, featureIndex] > splitValue
            leftDataX = dataX[left]
            rightDataX = dataX[right]
            # corner case. if left or right tree size is zero, return the leaf
            if leftDataX.shape[0] == 0 or rightDataX.shape[0] == 0:
                return np.array([[-1, np.mean(dataY), -1, -1]])
            # recursively calculate root node, left tree node and right tree node and then add them to the tables on a row-by-row basis
            leftDataY = dataY[left]
            rightDataY = dataY[right]
            leftTree = self.buildTree(leftDataX, leftDataY)
            rightTree = self.buildTree(rightDataX, rightDataY)
            root = np.array([[featureIndex, splitValue, 1, len(leftTree) + 1]])
            tree = np.concatenate((root, leftTree, rightTree), axis=0)
            return tree

    def addEvidence(self, dataX, dataY):

        self.tree = self.buildTree(dataX, dataY)

    def query(self, points):
        
        yResults = []
        rowNum = points.shape[0]
        for i in range(rowNum):
            notLeaf = True
            nodeIndex = 0
            while notLeaf:
                feature = self.tree[nodeIndex, 0]
                splitValue = self.tree[nodeIndex, 1]
                if feature < 0:
                    notLeaf = False
                    yResults.append(splitValue)
                elif points[i, int(feature)] <= splitValue:
                    nodeIndex = nodeIndex + int(self.tree[nodeIndex, 2])
                else:
                    nodeIndex = nodeIndex + int(self.tree[nodeIndex, 3])
        return yResults


if __name__ == "__main__":
    print "the secret clue is 'robot'"
