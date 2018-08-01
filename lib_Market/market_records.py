"""
objects: market_value
    :attribute  time:   string object; time of record
    :attribute  low:    float object; lowest value within a day
    :attribute  high:   float object; highest value within a day
    :attribute  open:   float object; open value of a day
    :attribute  close:  float object; close value of a day
    """

"""
objects: DataChain
    :attribute  time:   string list; time of records
    :attribute  low:    float list; daily lowest value
    :attribute  high:   float list; daily highest value
    :attribute  open:   float list; daily open value
    :attribute  close:  float list; daily close value
    
    :attribute  data:           market indx list
    :attribute  StartTime:      string object; first day in records
    :attribute  EndTime:        string object; last day in records
    :attribute  LowestRecord:   dictionary object; {lowest date (string) : lowest value in records}
    :attribute  HighestRecord:  dictionary object; {highest date (string) : highest value in records}
    
    :method '+':        operation;  combine two seperate data according to time order, now only works for daily-data
    :method truncate:   function;   return: a part of the whole records
                                    arg1: date1, begin of truncation, either DATE(string) or INDEX(integer)
                                    arg2: date1, end of truncation, either DATE(string) or INDEX(integer)
    :method LogReturns: function;   return: Log(P(t+dt)) - Log(P(t))
                                    arg1: interval, i.e. time interval dt in above formula
    :method Volatility: function;   return: volatility, calculated as standard deviation over certain time range
                                    arg1: range, time range to calculate standard interval
                                    arg2: overlap, time overlap between uniformally-picked neighbouring date
    
"""


import numpy as np
import collections


class market_value:
    def __init__(self, time, open, high, low, close):
        self.time = str(time)
        self.low = float(low)
        self.high = float(high)
        self.open = float(open)
        self.close = float(close)

class DataChain:
    def __init__(self, indxChain):
        self.data = indxChain
        
        self.StartTime = indxChain[0].time
        self.EndTime = indxChain[-1].time
        
        self.time = []; self.open = []; self.close = []; self.low = []; self.high = []
        for indx in indxChain:
            self.time.append(indx.time)
            self.open.append(indx.open)
            self.close.append(indx.close)
            self.low.append(indx.low)
            self.high.append(indx.high)
        
        self.LowestRecord = {self.time[self.low.index(min(self.low))]: min(self.low)}
        self.HighestRecord= {self.time[self.high.index(max(self.high))]: max(self.high)}
            

####  Note: Current version only works for daily data
    def __add__(self, other):
        date_af = Date_to_Integer(self.firstDay); date_al = Date_to_Integer(self.lastDay)
        date_bf = Date_to_Integer(other.firstDay); date_bl = Date_to_Integer(other.lastDay)
        if (date_al < date_bf ):
            return(SPIndxData(self.data + other.data))
        elif  (date_af > date_bl ):
            return(SPIndxData(other.data + self.data))
        else:
            print("Error: Time range duplicated! Shouldn not merge.")
            return None

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def truncate(self, time1, time2):
        if (type(time1) == type(0) and type(time2) == type(0)):     # Input as index
            if time2 > len(self.data):
                print("Error: Truncation out of range!")
                return None
            else:
                idx_start = time1;  idx_end = time2
        else:                                                       # Input as 'mm/dd/yy'
            idx_start = self.time.index(time1);    idx_end = self.time.index(time2) + 1
        return DataChain(self.data[idx_start : idx_end])


    def Returns(self):
        return self.LogReturns(interval = 1)


    def LogReturns(self, **kwargs):
        interval = 1
        returns = [0.0]   # in daily return case, cast size into the same as dates
        for key, value in kwargs.items():
            if key == 'interval':
                interval = value
        for i in range(int(len(self.close)/interval)-1):
            returns.append( np.log(self.close[(i+1)*interval]/self.close[i*interval]) )
        return returns

    def Volatility(self, range, overlap):
        if overlap >= range:
            overlap = range - 1
        returns = self.LogReturns()
        first_point = int(range/2) + 1
        last_point = len(returns) - first_point
        increment = range - overlap
        start_point = 0
        volty = {}
        while start_point < last_point:
            end_point = start_point + range
            piece = returns[start_point:end_point]
            volty[start_point + first_point] = np.std(piece)
            start_point += increment
        volty = collections.OrderedDict(sorted(volty.items()))
        return volty

    def ReturnScaled(self, interval_list):
        returns = []
        for intv in interval_list:
            returns.append(self.LogReturns(interval = intv))
        return returns

    def Return_Scalling_Behavior(self, interval_list):
        returns = self.ReturnScaled(interval_list)
        MeanReturn = []; VarReturn = []
        for rt in returns:
            MeanReturn.append(np.mean(rt)); VarReturn.append(np.std(rt))
        return MeanReturn, VarReturn




class HF_value(market_value):
    def __init__(self, time, buy, sell):
        market_value.__init__(self, time, buy, buy, sell, sell)
        self.buy = float(buy)
        self.sell = float(sell)

class HF_Data(DataChain):
    def __init__(self, valuechain, name):
        DataChain.__init__(self, valuechain)
        self.name = name
        self.buys = self.open
        self.sells = self.close




def Date_to_Integer(date):
    dt = date.split('/')
    return (int(dt[2])* 370 + int(dt[1])*31 + int(dt[0]))
