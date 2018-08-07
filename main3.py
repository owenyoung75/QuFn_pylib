import csv
import numpy as np
import matplotlib.pyplot as plt
from random import *

from lib_Market.market_records import *
from lib_Market.market_read import *
from lib_Market.PlotMarketRec import *
from lib_Models.basic_funcs import *
from lib_Models.TS_models import *


if __name__ == '__main__':
    num_sim = 10

    Data = read_SingleHF('APPL.csv')
    returns = Data.Returns()

    model = Model_AR(5)
    model.FitData(returns)

    ACR = [[]]
    simulations = []
    for i in range(num_sim):
        simulations.append( model.Generator(len(returns)) )
        ACR.append([])

    Tau = []
    for dt in range(11):
        Tau.append(dt)
        ACR[0].append(AutoCorr(returns, dt))
        for i in range(num_sim):
            ACR[i+1].append(AutoCorr(simulations[i], dt))


    fig1 = plt.figure()
    ax = plt.subplot(2,1,1)
    plt.plot(Tau, ACR[0])
    axes = plt.gca()
    axes.axhline(y=0, color = 'black', linewidth = 0.8)
    axes.set_ylim([-0.4,0.4])
    ax = plt.subplot(2,1,2)
    for i in range(num_sim+1):
        plt.plot(Tau, ACR[i])
    axes = plt.gca()
    axes.axhline(y=0, color = 'black', linewidth = 0.8)
    axes.set_ylim([-0.4,0.4])



    Y = np.square( np.asarray(model.Residuals()) ).tolist()
    model2 = Model_AR(5)
    model2.FitData(Y)

    ACR = [[]]
    simulations = []
    for i in range(num_sim):
        simulations.append( model2.Generator(5000) )
        ACR.append([])

    Tau = []
    for dt in range(11):
        Tau.append(dt)
        ACR[0].append(AutoCorr(Y, dt))
        for i in range(num_sim):
            ACR[i+1].append(AutoCorr(simulations[i], dt))



    fig2 = plt.figure()
    ax = plt.subplot(2,1,1)
    plt.plot(Tau, ACR[0])
    axes = plt.gca()
    axes.axhline(y=0, color = 'black', linewidth = 0.8)
    axes.set_ylim([-0.2,0.4])
    ax = plt.subplot(2,1,2)
    for i in range(num_sim+1):
        plt.plot(Tau, ACR[i])
    axes = plt.gca()
    axes.axhline(y=0, color = 'black', linewidth = 0.8)
    axes.set_ylim([-0.2,0.4])


    plt.show()














#    returns = [0.3, 0.7, 0.8, 0.2, 0.1]
#    res = []
#    for i in range(10000):
#        res.append(normalvariate(0.0, 0.0001))
#        returns.append(0.00001
#                       + 0.2*returns[-1] + 0.2*returns[-2] + 0.2*returns[-3] + 0.2*returns[-4] + 0.2*returns[-5]
#                       + res[-1]
#                       )
