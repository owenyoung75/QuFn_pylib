import numpy as np
import matplotlib.pyplot as plt

from lib_SP.SPdata_obtain import *
from lib_SP.PlotSP import *

from lib_Stock.Stockdata_obtain import *
from lib_Stock.PlotStock import *

if __name__ == '__main__':
    SPdata = read_SPdata('GSPCs.csv')

    PlotSPIndx(SPdata, 'close')
    PlotSPReturn(SPdata, 'compare')
    PlotSPVolatility(SPdata, 21, 20, 'compare')
    sim_return = PlotSimReturn(SPdata, np.random.normal, 'overlap')
    PlotReturnEDF(SPdata, 'log')
    

    #PlotSPIndx(SPdata, 'high', 'low', 'save')
    #PlotSPReturn(SPdata, 'compare', 'save')
    #PlotSPVolatility(SPdata, 21, 20, 'compare', 'save')
    #PlotSimReturn(SPdata, np.random.normal, 'overlap', 'save')
    #PlotReturnEDF(SPdata, 'compare', 'save')
   
   
    Yt = np.add.accumulate(sim_return)
    plt.figure()
    plt.plot(Yt)
   
    plt.show()
