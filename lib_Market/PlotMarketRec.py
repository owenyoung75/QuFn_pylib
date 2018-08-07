"""
function:   PlotFormat
# setting of plot format, and label seaons&years on X-axis #
    return:     a list of four vertex coordinates of XY-axis
    arg1:       min; minimum value of y
    arg2:       max; maximum value of x
    arg3:       times; times list of records
    arg4:       axes; axis object of current plot (or subplot)
    default:    apply to data form (times especially) from Wall Street Journal;
                require modification for data from other recource
   
function:   PlotValue
# plot DataChain of different choices #
    arg1:       DataChain object;  plotted data
    *arg1:      choices: {'close', 'open', 'low', 'high'}; plotted prices; cane be multiple
    *arg2:      choices: {'save', None}; save figure and close
    
function:   PlotReturn
# plot returns #
    arg1:       DataChain object;  plotted data
    *arg1:      choice: {'compare', none}; plot the S&P index meanwhile to compare
    *arg2:      choices: {'save', None}; save figure and close
    
function:   PlotVolatility
# plot volatilities #
    arg1:       DataChain object;  plotted data
    arg2:       time range for stdev calculation; integer
    arg3:       time overlap in stdev calculation; integer
    *arg1:      choice: {'compare', none}; plot the S&P index meanwhile to compare
    *arg2:      choices: {'save', None}; save figure and close

function:   PlotPlotSimReturn
# plot simulated returns from certain distribution, and compare with real ones #
    return:     array object; simulated returns with given distribution, e.g. Normal, Uniform, .etc
    arg1:       SPIndxData object;  plotted data
    arg2:       <built-in-funciton>; specify distribution type used for simulation
    *arg1:      choice: {'overlap', none}; plot the real and simulated returns together or separately
    *arg2:      choices: {'save', None}; save figure and close

function:   PlotReturnEDF
# plot returns empirical distribution, and compare with Gaussian(Normal) distribution #
    arg1:       DataChain object;  plotted data
    *arg1:      choice: {'log', none}; compare with Gaussian in a log scale as well
    *arg2:      choices: {'save', None}; save figures and close


"""






import random
import numpy as np
import matplotlib; matplotlib.rc('text', usetex=True)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import collections
from scipy import stats
from scipy.interpolate import spline


from .market_records import *


#### Note: This format now only works for daily data plotting because of x-labels
#### For other formats, e.g. high-frequency data, need further extensions
def PlotFormat(_min, _max, _dates, _axes):
    #   Note: Here we assume the time-range covers integer years
    #         to simplify the season&year's labeling on x-axis
    xmax = len(_dates) + 2; xmin = 0
    xmajor_interval = 251.5;      xminor_interval = 63;
    xmajor_ticks = np.arange(xmin, xmax, xmajor_interval)
    xminor_ticks = np.arange(xmin, xmax, xminor_interval)
    
    ymax = _max; ymin = _min
    yrange = ymax - ymin;
    ymin = ymin - int(yrange/10);  ymax = (ymax + int(yrange/10)*2) * 1.01
    ymajor_interval =  yrange/5;   yminor_interval = ymajor_interval/4;
    ymajor_ticks = np.arange(ymin, ymax, ymajor_interval)
    yminor_ticks = np.arange(ymin, ymax, yminor_interval)
    
    _axes.set_xticks(xmajor_ticks)
    _axes.set_xticks(xminor_ticks, minor=True)
    _axes.set_yticks(ymajor_ticks)
    _axes.set_yticks(yminor_ticks, minor=True)
    
    _axes.grid(which='both')
    _axes.grid(which='minor', alpha=0.0)
    _axes.grid(which='major', alpha=0.5)
    
    month = [];  str = []
    NumOfSeasons = int(xmax/xminor_interval);   NumOfYears = int(xmax/xmajor_interval)
    for i in range(NumOfSeasons):
        month.append(i*xminor_interval)
    for i in range(NumOfYears):
        # for time format from Wall Street Journal
        #tmp_year = _dates[int(xmajor_interval/2 + i * xmajor_interval)].split('/')[2]
        # for time format from Yahoo Finance
        tmp_year = _dates[int(xmajor_interval/2 + i * xmajor_interval)].split('-')[0]
        str.append('1/'+tmp_year)
        str.append('4/'+tmp_year)
        str.append('7/'+tmp_year)
        str.append('10/'+tmp_year)
    month.append(xmax);  str.append('1/next-year')
    plt.xticks(month, str, color='k', size=5)

    return [xmin, xmax, ymin, ymax]





def CompareValue(_data, _axes, *args):
    for arg in args:
        if arg == 'close':
            plt.plot(_data.close)
        elif arg == 'open':
            plt.plot(_data.open)
        elif arg == 'low':
            plt.plot(_data.low)
        elif arg == 'high':
            plt.plot(_data.high)

    coordinates = PlotFormat(list(_data.LowestRecord.values())[0], list(_data.HighestRecord.values())[0], _data.time, _axes)
    plt.ylabel(r'Market Value', {'color': 'b', 'fontsize': 15})
    return coordinates




def PlotValue(_data, *args):
    fig = plt.figure()
    ax = plt.axes()
    off = 8.0
    
    coordinates = CompareValue(_data, ax, *args)
    plt.xlabel(r'Seasons(mm/yy) in each year', {'color': 'b', 'fontsize': 15})

    return fig



def PlotReturn(_data, *args):
    fig = plt.figure()
    ax = plt.axes()
    off = 5.0
    
    for arg in args:
        if arg == 'compare':
            ax = plt.subplot(2,1,1)
            _ = CompareValue(_data, ax, 'close')
            ax = plt.subplot(2,1,2)
            off = 3.0
            break

    returns = _data.Returns()
    plt.plot(returns)
    
    coordinates = PlotFormat(min(returns), max(returns), _data.time, ax)
    plt.xlabel(r'Seasons(mm/yy) in each year', {'color': 'b', 'fontsize': 15})
    return fig



def PlotVolatility(_data, _interval, _overlap, *args):
    fig = plt.figure()
    ax = plt.axes()
    off = 5.0
    
    for arg in args:
        if arg == 'compare':
            ax = plt.subplot(2,1,1)
            _ = CompareValue(_data, ax, 'close')
            ax = plt.subplot(2,1,2)
            off = 3.0
            break

    volty = _data.Volatility(_interval, _overlap)
    plt.plot(volty.keys(), volty.values())
    
    coordinates = PlotFormat(min(volty.values()), max(volty.values()), _data.time, ax)
    plt.xlabel(r'Seasons(mm/yy) in each year', {'color': 'b', 'fontsize': 15})
    return fig



def PlotSimReturn(_data, _distr, *args):
    returns = _data.Returns()
    mu = np.mean(returns);  sigma = np.std(returns)
    sim_LogReturn = _distr(mu, sigma, len(_data.time))
    
    fig = plt.figure()
    ax = plt.axes()
    off = 5.0
    for arg in args:
        if arg == 'overlap':
            plt.plot(returns)
            ylabel = r'Real returns .vs. White Noise'
            break
        else:
            ax = plt.subplot(2,1,1)
            plt.plot(returns)
            coordinates = PlotFormat(min(returns), max(returns), _data.time, ax)
            plt.ylabel(r'Real returns', {'color': 'b', 'fontsize': 15})
            ax = plt.subplot(2,1,2)
            ylabel = r'Normal returns'
            off = 3.0

    plt.plot(sim_LogReturn)
    coordinates = PlotFormat(min(sim_LogReturn), max(sim_LogReturn), _data.time, ax)
    
    plt.xlabel(r'Seasons(mm/yy) in each year', {'color': 'b', 'fontsize': 15})
    plt.ylabel(ylabel, {'color': 'b', 'fontsize': 15})

    filename = 'Return&Normal_compare.png'
    save_figure(fig, filename, *args)
    return sim_LogReturn



def PlotReturnEDF(_data, *args):
    fig = plt.figure()
    hist = PlotSingleReturnEDF(_data, 1, 'compare', *args)
    
    filename = 'Returns_EDF.png'
    for arg in args:
        if arg == 'log':
            filename = 'LogReturns_EDF.png'
            break
    save_figure(fig, filename, *args)
    return hist


def PlotMultipleReturnEDF(_data, intvs):
    fig = plt.figure()
    hists = []
    for intv in intvs:
        hists.append(PlotSingleReturnEDF(_data, intv))
    return hists



def PlotSingleReturnEDF(_data, intv, *args):
    cmp = False;    log = False
    for arg in args:
        if arg == 'compare':
            cmp = True
        elif arg == 'log':
            log = True

    returns = _data.LogReturns(interval = intv)
    count, bins = np.histogram(returns,  int(len(returns)/20), normed=True)
    cnter = []; hist = {}
    for i in range(len(bins)-1):
        cnter.append( (bins[i] + bins[i+1])/2.0 )
        hist[cnter[i]] = count[i]

    if log:
        plt.plot(cnter, np.log(count).tolist())
        #new_cnter = np.linspace(min(cnter), max(cnter), 200)
        #new_count = spline(np.array(cnter), count, new_cnter)
        #plt.plot(new_cnter.tolist(), np.log(new_count).tolist())
        plt.xlabel(r'Log(returns)', {'color': 'b', 'fontsize': 15})
        plt.ylabel('Log(empirical PDF)', {'color': 'b', 'fontsize': 15})
    else:
        plt.hist(returns, int(len(returns)/15), normed=True)
        #plt.plot(cnter, count.tolist())
        plt.xlabel(r'Returns', {'color': 'b', 'fontsize': 15})
        plt.ylabel('Empirical PDF', {'color': 'b', 'fontsize': 15})


    if cmp:
        xmin = min(returns)*1.05;    xmax = max(returns)*1.05;      dx = (xmax - xmin)/100
        mean = np.mean(returns);     stdev = np.std(returns)
        t = np.arange(xmin, xmax, dx)
        gaus = np.exp(-(t-mean)**2/(2.0*stdev*stdev))/(stdev * np.sqrt(2 * np.pi))
        if log:
            plt.plot(t, np.log(gaus))
        else:
            plt.plot(t, gaus)

    return  hist



def PlotScallingBehavior(time_intervals, scaled_values, *args):
    log = False; order = 5
    for arg in args:
        if arg == 'log':
            log = True
        elif type(arg) == int:
            order = arg

    time_intervals = np.asarray(time_intervals); scaled_values = np.asarray(scaled_values)
    
    coeffs = np.polyfit(time_intervals, scaled_values, order)
    func = np.poly1d(coeffs)
    print(coeffs)
    tp = np.linspace(time_intervals[0], time_intervals[-1], 100)
    
    fig = plt.figure()
    _ = plt.plot(time_intervals, scaled_values, '.', tp, func(tp), '-')
    plt.xlabel(r'time intervals',   {'color': 'b', 'fontsize': 15})
    plt.ylabel(r'scaled values', {'color': 'b', 'fontsize': 15})
    save_figure(fig, 'time_scalling.png', *args)

    if log:
        fig = plt.figure()
        time_intervals = np.log(time_intervals); scaled_values = np.log(scaled_values)
        coeffs_log = np.polyfit(time_intervals, scaled_values, 1)
        #slope, intercept, r_value, p_value, std_err = stats.linregress(time_intervals, scaled_values)
        func = np.poly1d(coeffs_log)
        tp = np.linspace(time_intervals[0], time_intervals[-1], 100)

        _ = plt.plot(time_intervals, scaled_values, '.', tp, func(tp), '-')
        plt.xlabel(r'Log(time intervals)',   {'color': 'b', 'fontsize': 15})
        plt.ylabel(r'Log(scaled values)', {'color': 'b', 'fontsize': 15})
        save_figure(fig, 'Log_time_scalling.png', *args)
        print(coeffs_log)
        return coeffs, coeffs_log
    else:
        return coeffs




def save_figure(_figure, _file_name, *args):
    for arg in args:
        if arg == 'save':
            _figure.savefig(_file_name)
            plt.close(_figure)
            return None
    return None



