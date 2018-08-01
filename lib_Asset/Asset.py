from datetime import datetime
import sys

from .MarketEnvs import *
from .FinInstrument import *
from .FinInstrument import _name_list_
from .Bond import *


_dash_line_ = '+' * 96


class Asset:
    def __init__(self,
                 _holder_name,
                 _cash,
                 _portfolios,
                 _base_instruments = None
                 ):
        self.HolderName = _holder_name
        self.Cash = _cash
        
        if not type(_portfolios) == type(["list",]):
            _portfolios = [_portfolios,]
        self.Portfolios = _portfolios
        
        if _base_instruments == None:
            _base_instruments = []
            for portfolio in _portfolios:
                for instrument in portfolio.Basket:
                    if not instrument.Name in _name_list_(_base_instruments):
                        _base_instruments.append(instrument)
        self.BaseInstruments = _base_instruments

        self.NamesPortfolio  = [portfolio.Name  for portfolio  in _portfolios]
        self.NamesInstrument = [instrument.Name for instrument in _base_instruments]


    def PrintDetails(self):
        dashed_line = '+' * 40
        
        print('\n')
        print(_dash_line_)
        print(dashed_line + " <Asset Object> " + dashed_line)
        print(_dash_line_)
        print("Account Holder: {0}".format(self.HolderName) )
        print("Cash value: {0};  Total value in Portfolios: {1}".format(self.Cash,
                                                                        sum([ptf.TotalValue for ptf in self.Portfolios])
                                                                        ))
        print("Mangaing the following {0} Portfolios: {1}".format(len(self.NamesPortfolio), '\n'))
        for portfolio in self.Portfolios:
            portfolio.PrintDetails()
        print('\n')
        print(_dash_line_)
        print(dashed_line + " <Asset Object> " + dashed_line)
        print(_dash_line_)
        print('\n')
        
        return None
    
    
    def AddPortfolio(self,
                     _portfolio
                     ):
        self.Portfolios.append(_portfolio)
        self.NamesPortfolio.append(_portfolio.Name)
    
        for instr in _portfolio.Basket:
            if not instr.Name in self.NamesInstrument:
                self.BaseInstruments.append(instr)
                self.NamesInstrument.append(instr.Name)
        return None
    
    
    def Remember(self, instruments):
        if not type(instruments) == type(["list",]):
            instruments = [instruments,]
        for instr in instruments:
            if not instr.Name in self.NamesInstrument:
                self.BaseInstruments.append(instr)
                self.NamesInstrument.append(instr.Name)
        return None


    def TradeEvent(self,
                   _type,
                   market,
                   namelist,
                   values,
                   date = None,
                   ptf_name = None,
                   _print_control = False
                   ):
        if date == None:
#            print("Note: No date specified. Default trading on today.")
            date = datetime.today()
        if not type(date) == type(datetime.today()):
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            date = datetime.strptime(date, '%m/%d/%Y')
                
        if _type == "SELL" :
            return self._sell_(market,
                               namelist,
                               values,
                               date,
                               ptf_name,
                               _print_control
                               )
        elif _type == "BUY" :
            return self._buy_(market,
                              namelist,
                              values,
                              date,
                              ptf_name,
                              _print_control
                              )
        else:
            print("WARRNING: Unknonw trading type: {}. Return without trading.".format(_type))
            return 0


    def _sell_(self,
               _market,
               _sell_namelist,
               _sell_values,
               _date = None,
               _ptf_name = None,
               _print_control = False
               ):
        if _ptf_name == None:
            ptf = self.Portfolios[0]
        else:
            ptf = _find_from_name_(self.Portfolios, _ptf_name)[0]
        
        if not type(_sell_namelist) == type(["list",]):
            _sell_namelist = [_sell_namelist,]
        if not type(_sell_values) == type(["list",]):
            _sell_values = [_sell_values,]
        
        for i in range(len(_sell_namelist)):
            name = _sell_namelist[i]
            amount = _sell_values[i]
            idx = ptf.NameList.index(name)
            if amount > ptf.Values[idx]:
                print("WARRNING: NOT enough to sell for product {0}: ".format(name))
                print("Return without trading.")
                return 0
    
        _, returns = ptf.Sell(_market,
                              _sell_namelist,
                              _sell_values,
                              _date,
                              _print_control)
        self.Cash += returns
        return returns


    def _buy_(self,
              _market,
              _buy_list,
              _buy_values,
              _date = None,
              _ptf_name = None,
              _print_control = False
              ):
        if _ptf_name == None:
            ptf = self.Portfolios[0]
        else:
            ptf = _find_from_name_(self.Portfolios, _ptf_name)[0]
    
        if not type(_buy_list) == type(["list",]):
            _buy_list = [_buy_list,]
        if not type(_buy_values) == type(["list",]):
            _buy_values = [_buy_values,]

        ###     Check input type: name-string or instruments
        if type(_buy_list[0]) == type(str('string')):
            for name in _buy_list:
                if not name in self.NamesInstrument:
                    print("ERROR: No info for Instrument {0}. Please define it first.".format(name))
                    sys.exit()
            _buy_productlist = _find_from_name_(self.BaseInstruments, _buy_list)
        else:
            for instr in _buy_list:
                if not instr.Name in self.NamesInstrument:
                    self.BaseInstruments.append(instr)
                    self.NamesInstrument.append(instr.Name)
            _buy_productlist = _buy_list

        
        costs = 0
        for idx in range(len(_buy_productlist)):
            costs += _buy_productlist[idx].Price(_buy_values[idx],
                                                 _market,
                                                 _date)
        
        if costs > self.Cash:
            print("WARRNING: NOT enough cash when buying: ")
            print(_buy_list)
            print("Return without trading.")
            costs = 0
        else:
            _, costs = ptf.Buy(_market,
                               _buy_productlist,
                               _buy_values,
                               _date,
                               _print_control)
        self.Cash -= costs
        return  costs




def _find_from_name_(_objects_list,
                     _names
                     ):
    if not type(_names) == type(["list",]):
        _names = [_names,]
    
    objects = []
    for name in _names:
        found = 0
        for object in _objects_list:
            if object.Name == name:
                objects.append(object); found = 1
                break
        if not found:
            print("ERROR: {0} does not exit in {1}.".format(name, _objects_list))
            return None
    return objects








