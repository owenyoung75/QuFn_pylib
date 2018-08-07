
import matplotlib; matplotlib.rc('text', usetex=True)
import matplotlib.pyplot as plt

from lib_Market.PlotMarketRec import *



def PlotStockPrice(_data, *args):
    fig = PlotValue(_data, *args)
    filename = _data.name + '_Price.png'
    save_figure(fig, filename, *args)
    return None



def PlotStockReturn(_data, *args):
    fig = PlotReturn(_data, *args)
    labely = 'Stock ' + _data.name + ' return'
    plt.ylabel(labely, {'color': 'b', 'fontsize': 15})
    
    filename = _data.name + '_returns.png'
    save_figure(fig, filename, *args)
    return None



def PlotStockVolatility(_data, _interval, _overlap, *args):
    fig = PlotVolatility(_data, _interval, _overlap, *args)
    plt.ylabel(r'Stock volatility', {'color': 'b', 'fontsize': 15})
    
    filename = _data.name + '_volatility.png'
    save_figure(fig, filename, *args)
    return None




def save_figure(_figure, _file_name, *args):
    for arg in args:
        if arg == 'save':
            _figure.savefig(_file_name)
            plt.close(_figure)
            return 1
    return 0



