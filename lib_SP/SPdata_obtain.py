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
import time
import shutil
from datetime import date
from selenium import webdriver


from SPindex import SPindx
from SPindex import SPIndxData


def read_SPdata0(FilePath):
    indxChain = []
    print('\n')
    with open(FilePath, 'r') as file:
        fileReader = csv.reader(file)
        dumb = next(fileReader)
        for line in fileReader:
            indx = SPindx(line[0], line[1], line[2], line[3], line[4])
            indxChain.append(indx)
    print("Pulling S&P index from csv...")
    return SPIndxData(indxChain)


def read_SPdata(FilePath):
    indxChain = []
    print('\n')
    try:
        with open(FilePath, 'r') as file:
            fileReader = csv.reader(file)
            dumb = next(fileReader)
            for line in fileReader:
                indx = SPindx(line[0], line[1], line[2], line[3], line[4])
                #   for file format from Wall Street Journal
                #indxChain.insert(0,indx)
                #   for file format from Yahoo Finance
                indxChain.append(indx)
        print("Pulling S&P index from csv...")
        return SPIndxData(indxChain)
    except:
        print("No S&P index found. Start download online...")
        filepath = download_SPdata()
        return read_SPdata(filepath)





def download_SPdata():
    driver = webdriver.Chrome()
    
    #   From Wall Street Journal
    driver.get('http://quotes.wsj.com/index/SPX/historical-prices')

    # input dates
    # download data of last three years
    current_year = date.today().year
    start_date = '01/03/1950'
    end_date   = '12/31/' + str(current_year - 1)
    text_area_from  = driver.find_element_by_id('selectDateFrom')
    text_area_to    = driver.find_element_by_id('selectDateTo')
    text_area_from.clear(); text_area_from.send_keys(start_date)
    text_area_to.clear();   text_area_to.send_keys(end_date)

    # click download button
    dl_button = driver.find_element_by_id('dl_spreadsheet')
    time.sleep(1)
    dl_button.click()
    
    
    #   From Yahoo Finance
    #driver.get('https://finance.yahoo.com/quote/%5EGSPC/')
    #history_button = driver.find_element_by_xpath("//*[@id='quote-nav']/ul/li[6]/a")
    #history_button.click()
    
    # input dates
    # download data of all past years since 1950
    #current_year = date.today().year
    #start_date = '01/03/1950' ;
    #end_date   = '12/31/' + str(current_year - 1)
    #text_area_from  = driver.find_element_by_xpath("//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[1]/div[1]/div[1]/span[2]/div/input[1]")
    #text_area_to    = driver.find_element_by_xpath("//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[1]/div[1]/div[1]/span[2]/div/input[2]")
    #text_area_from.clear(); text_area_from.send_keys(start_date)
    #text_area_to.clear();   text_area_to.send_keys(end_date)
    
    # click download button
    #dl_button = driver.find_element_by_xpath("//*[@id='Col1-1-HistoricalDataTable-Proxy']/section/div[1]/div[2]/span[2]/a/span")
    #dl_button.click()
    
    
    time.sleep(3)
    driver.quit()

    filepath = '/Users/yangtong/Documents/study/Econ/econphys/HistoricalPrices_' + str(date.today()) + '.csv'
    shutil.move('/Users/yangtong/Downloads/HistoricalPrices.csv',filepath)
    #filepath = '/Users/yangtong/Documents/study/Econ/econphys/GSPC_' + str(date.today()) + '.csv'
    #shutil.move('/Users/yangtong/Downloads/^GSPC.csv',filepath)
    return filepath




