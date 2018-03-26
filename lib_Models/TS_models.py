import numpy as np
import collections
from random import *

from basic_funcs import *


class Model_AR:
    def __init__(self, _lag, _coeffs=1.0, _sigma=1.0, _center = 1.0):
        self.coeffs = _coeffs
        self.lag = _lag
        self.sigma = _sigma
        self.data = []
        self.initial = []
        for i in range(self.lag):
            self.initial.append(uniform(-_center/10.0, _center/10.0) + _center)
    
    
    def FitData(self, _data):
        data = np.asarray(_data)
        DataLag = []
        for i in range(len(_data) - self.lag):
            history = data[i:(i+self.lag)]
            history = np.insert(history, 0, 1.0)
            DataLag.append(history)
        DataPred = data[self.lag:]
        coeffs = OLS_SVD(DataLag, DataPred)

        _data = data.tolist()
        self.data = _data
        self.sigma = np.std(_data)
        self.initial = _data[0:self.lag]
        self.coeffs = np.reshape(np.asarray(coeffs), (self.lag + 1))

        print(self.coeffs)



    def Generator(self, _num):
        sequence = self.initial[:]
        for i in range(_num - self.lag):
            history = np.asarray(sequence[(len(sequence)-self.lag):])
            history = np.insert(history, 0, 1.0)
            new = np.dot(history, self.coeffs) + normalvariate(0.0, self.sigma)
            sequence.append(new)
        return sequence


    def Residuals(self):
        sequence = []
        for i in range(self.lag):
            sequence.append(0)
        for i in range(len(self.data) - self.lag):
            history = np.asarray(self.data[i:(i+self.lag)])
            history = np.insert(history, 0, 1.0)
            sequence.append( self.data[i+self.lag] - np.dot(history, self.coeffs) )
        return sequence




#class Model_ARCH:
#    def __init__(self, lag)

