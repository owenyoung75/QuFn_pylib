
import numpy as np
import collections
from random import *


def Corr(_dataX, _dataY):
    meanX = np.mean(_dataX)
    meanY = np.mean(_dataY)
    devX = np.std(_dataX)
    devY = np.std(_dataY)
    return np.dot((_dataX - meanX)/devX,(_dataY-meanY)/devY) / len(_dataX)


def AutoCorr(_data, _interval=1):
    length = len(_data)
    X = _data[0:(length-_interval)]
    Y = _data[_interval:]
    return Corr(X, Y)



def OLS_SVD(_data, _y):
    M = np.asmatrix(_data)
    U, s, V = np.linalg.svd(M)
    y = np.transpose( _y * U )[0:len(s)]
    y = np.transpose(y)/s
    coeffs = np.transpose( y * V )
    return coeffs





