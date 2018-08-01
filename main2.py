import numpy as np
import matplotlib.pyplot as plt

from lib_Stock.Stockdata_obtain import *
from lib_Stock.PlotStock import *

if __name__ == '__main__':
    Stockdata = read_Stockdata('INTC.csv')
    print(Stockdata)
    
    dts = np.asarray(range(10)) + 1
    dts = [1,2,3,4,5,6,7,8,9,10]
    means, vars = Stockdata.Return_Scalling_Behavior(dts)
    hists = PlotMultipleReturnEDF(Stockdata, dts)
    vertex = []
    for hist in hists:
        vertex.append( max(hist.values()) )
    
    
    #_ = PlotScallingBehavior(dts, means, 'log')
    #_ = PlotScallingBehavior(dts, vars, 5, 'log')
    #_ = PlotScallingBehavior(dts, vertex, 'log')


    plt.show()
