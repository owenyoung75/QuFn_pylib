import os
import glob
import pickle

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from .Asset import *



def Assets_Writing(_asset,
                   _date = None
                   ):
    if _date == None:
        _date = datetime.today()
    if not type(_date) == type(datetime.today()):
        _date = datetime.strptime(_date, '%m/%d/%Y')
    date  = _date.date()
    holder = _asset.HolderName
    filename = "./" + holder + "/"+ holder + "_"+ str(date) + ".pkl"

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(_asset, file)
    file.close()
    return None




def Assets_Reading(_holder,
                   _date = None
                   ):
    if _date == None:
        _date = datetime.today()
    if not type(_date) == type(datetime.today()):
        _date = datetime.strptime(_date, '%m/%d/%Y')
    date  = _date.date()
    filename = "./" + _holder + "/"+ _holder + "_"+ str(date) + ".pkl"

    if not os.path.exists(filename):
        print("Records of User {0} on Date {1} does not exit.".format(_holder, str(date)))
        ###      Future change: maybe exit other records than standard ones
        ###      Need a search starting from the end
        list_of_files = glob.glob('./' + _holder + '/*')
        list_of_files.sort()
        latest_dated = list_of_files[-1]
        date = datetime.strptime(latest_dated.split('.')[-2][-10:], '%Y-%m-%d').date()
        print("Open the most recent records on date: ", date)
        filename = "./" + _holder + "/"+ _holder + "_"+ str(date) + ".pkl"
    with open(filename, 'rb') as file:
        asset = pickle.load(file)
    file.close()
    return asset


















