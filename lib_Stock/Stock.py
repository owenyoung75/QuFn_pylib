"""
objects: SPindx         A type of market index
    :attribute  adjust:     float object; adjusted close price
    :attribute  volume:     integer object; number of shares
"""

"""
objects: SPIndxData     A type of data chain
    :attribute  adjust:     float list; adjusted close prices list
    :attribute  volume:     integer list; share numbers list

"""


import numpy as np
import collections

from lib_Market.market_records import *


class Stock(market_value):
    def __init__(self, time, open, high, low, close, adjust, volume):
        market_value.__init__(self, time, open, high, low, close)
        self.adjust = adjust
        self.volume = volume



class StockData(DataChain):
    def __init__(self, indxChain, name):
        self.name = name
        self.data = indxChain
        
        self.StartTime = indxChain[0].time
        self.EndTime   = indxChain[-1].time
        
        self.time = []; self.open = []; self.close = []; self.low = [];
        self.high = []; self.adjust = []; self.volume = []
        for indx in indxChain:
            self.time.append(indx.time)
            self.open.append(indx.open)
            self.close.append(indx.close)
            self.low.append(indx.low)
            self.high.append(indx.high)
            self.adjust.append(indx.adjust)
            self.volume.append(indx.volume)
                        
        self.LowestRecord = {self.time[self.low.index(min(self.low))]: min(self.low)}
        self.HighestRecord= {self.time[self.high.index(max(self.high))]: max(self.high)}




