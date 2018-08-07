"""
function:   read_SPdata
    return:     a SPIndxData object from certain file
    arg:        FilePath; path to the file, if file exist, directly read data, if no file, download from external website
    
    
function:   download_SPdata
    return:     a string refering to the file-path of downloaded data
    default:    website: Wall Street Journal;   data: from 2000/01/03 to the end of last year
    
"""


import time
import random
import csv
import shutil
import pandas as pd
from pandas import read_csv

from .StockRec import StockRecd
from .StockRec import StockData


def read_Stockdata(FilePath):
    stock_name = FilePath.split('.')[0]
    indxChain = []
    print('\n')
    try:
        with open(FilePath, 'r') as file:
            fileReader = csv.reader(file)
            dumb = next(fileReader)
            for line in fileReader:
                indx = StockRecd(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
                indxChain.append(indx)
        #   for file format from Wall Street Journal
        #indxChain.reverse()
        print("Pulling stock " +stock_name + " data from csv...")
        return StockData(indxChain, stock_name)
    except:
        print("No stock data found. Please download manually.")
        return None




