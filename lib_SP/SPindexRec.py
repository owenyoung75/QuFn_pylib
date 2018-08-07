"""
objects: SPIndxRecd         A type of market index
"""

"""
objects: SPIndxData         A type of data chain
        :method Returns: function;   return: Log(P(t+1)) - Log(P(t)), i.e. daily log return

"""

import numpy as np
import collections

from lib_Market.market_records import *


class SPIndxRecd(market_recd):
    def __init__(self, date, open, high, low, close):
        super().__init__(date, open, high, low, close)



class SPIndxData(DataChain):
    def __init__(self, indxChain):
        super().__init__(indxChain)




