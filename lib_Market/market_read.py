import time
import random
import csv
import time
import shutil
from datetime import date
from selenium import webdriver


from .market_records import *


def read_SingleHF(FilePath):
    name = FilePath.split('.')[0]
    indxChain = []
    print('\n')
    try:
        with open(FilePath, 'r') as file:
            fileReader = csv.reader(file)
            dumb = next(fileReader)
            for line in fileReader:
                indx = HF_value(line[0], line[1], line[2])
                indxChain.append(indx)
        #   for file format with inverse time order, e.g. Wall Street Journal
        #indxChain.reverse()
        print("Pulling high frequency data of " + name + " from csv...")
        return HF_Data(indxChain, name)
    except:
        print("No high frequency data found. Please download manually.")
        return None
