
import matplotlib; matplotlib.rc('text', usetex=True)
import matplotlib.pyplot as plt

from lib_Market.PlotMarket import *



def PlotSPIndx(_data, *args):
    fig = PlotValue(_data, *args)
    filename = 'SP_indx.png'
    save_figure(fig, filename, *args)
    return None



def PlotSPReturn(_data, *args):
    fig = PlotReturn(_data, *args)
    plt.ylabel(r'S\&P 500 returns', {'color': 'b', 'fontsize': 15})

    filename = 'SP_returns.png'
    save_figure(fig, filename, *args)
    return None



def PlotSPVolatility(_data, _interval, _overlap, *args):
    fig = PlotVolatility(_data, _interval, _overlap, *args)
    plt.ylabel(r'S\&P 500 volatility', {'color': 'b', 'fontsize': 15})

    filename = 'SP_volatility.png'
    save_figure(fig, filename, *args)
    return None




def save_figure(_figure, _file_name, *args):
    for arg in args:
        if arg == 'save':
            _figure.savefig(_file_name)
            plt.close(_figure)
            return 1
    return 0



