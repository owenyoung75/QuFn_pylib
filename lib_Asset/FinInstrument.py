from datetime import datetime
import sys

_dash_line_ = '-' * 96



class Instrument:
    """
        Class: general financial instrument
        
        attribute: Class   asset class         string
        attribute: Type    instrument type     string
        attribute: Name    instrument name     string
        
        method: Price       calculate price value  return: real-number
        """
    def __init__(self,
                 _name,
                 _class,
                 _type
                 ):
        self.Class = _class
        self.Type = _type
        self.Name = _name
    
    
    """
        inputs: _value  face value or others    real-number
                _market market for trading      Market
                _date   date of evaluation      datetime/string
                
        outputs: price  price evaluated     real-number
        """
    def Price(self,
              _value,
              _market,
              _date):
        price = 0
        return price




class Portfolio:
    """
        Class: general portfolio
        
        attribute: Name         name of portfolio               string
        attribute: Basket       all products                    list of Instrument
        attribute: Values       all product values              list of real-number
        attribute: Namelist     all product names               list of strings
        attribute: TotalValue   total value of portfolio        real-value
        attribute: NumProducts  number of products included     integer
        attribute: Updates      updating dates of each product  list of datetime/string
        
        method: __call__        get info of product given name  return: Instrument, [real-number, datetime]
        method: PrintDetails    print details of all products   return: string
        method: Sell            a sell event                    return: Portfolio, real-number
        method: Buy             a buy event                     return: Portfolio
        """
    def __init__(self,
                 _name,
                 _basket,
                 _values,
                 _buy_dates = None
                 ):
        self.Name = _name
        self.Basket = _basket
        self.Values = _values
        self.NameList = _name_list_(_basket)
        self.TotalValue = sum(_values)
        self.NumProducts = len(_basket)
        
        if _buy_dates == None:
            today = datetime.today()
            _buy_dates = []
            self.Updates = []
            for _ in range(len(_values)):
                _buy_dates.append(datetime.today())
#            print("No date specified. Default all buy today:  ", today)
        if type(_buy_dates[0]) == type(datetime.today()):
            self.Updates = _buy_dates.copy()
        else:
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            self.Updates = []
            for date in _buy_dates:
                self.Updates.append(datetime.strptime(date, '%m/%d/%Y'))


    """
        inputs: name    name of product looking for     string
        
        outputs: instrument found instrument                Instrument
                 info       value-holding and updating-date list of string
        """
    def __call__(self, name):
        idx = self.NameList.index(name)
        info = [self.Values[idx], str(self.Updates[idx])]
        return self.Basket[idx], info
    
    def __str__(self):
        str1 = "Portfolio Name: {0} {1}".format(self.Name,'\n')
        str2 = "With {0} products,  TotalValue = {1}".format(self.NumProducts, self.TotalValue)
        return str1 + str2
    """
        inputs: None
        outputs: string
        """
    def PrintDetails(self):
        dashed_line = '-' * 38
        
        print()
        print(dashed_line + " <Portfolio Object> " + dashed_line)
        print(str(self))
        print("Including the following bonds:")
        for idx in range(len(self.Basket)):
            str_product = str(self.Basket[idx])
            str_basket = "{0:10}      {1}".format(self.Values[idx], self.Updates[idx])
            print(str_product + str_basket)
        print(dashed_line + " <Portfolio Object> " + dashed_line)

        return None


    """
        inputs: market          market of trading       Market
                sell_namelist   names for sale          list of Names/None
                sell_values     values of each sale     real-number or list of real-number/None
                date            date of trading         datetime/string/None
                
        outputs:    self            updated portfolio           Portfolio
                    return_values   values returned from sale   real-number
        """
    def Sell(self,
             market,
             sell_namelist = None,
             sell_values = None,
             date = None,
             print_control = True
             ):
        if sell_namelist == [] or sell_namelist == None:
            print("No product specified. Defautly sell the whole basket.")
            # Important: need to copy, otherwise act as pointer
            sell_namelist = self.NameList.copy()
            sell_values = self.Values.copy()
        if sell_values == [] or sell_values == None:
            print("No amounts specified. Default sell all amount for each product.")
            sell_values = [self.Values[self.NameList.index(name)] for name in sell_namelist]
        
        if not type(sell_namelist) == type(['list',]):
            sell_namelist = [sell_namelist,]
        if not type(sell_values) == type(['list',]):
            sell_values = [sell_values,]
        
        if type(sell_values[0]) != type(1.0) and type(sell_values[0]) != type(1):
            print("ERROR: Please provide numeric values for sell.")
            sys.exit()
        if not len(sell_namelist) == len(sell_values):
            print("ERROR: Size dismatch. Please specify one sell-amount for each product.")
            sys.exit()
        NumberOfSold = len(sell_namelist)

        if date == None:
            date = datetime.today()
            print("No date specified. Default sell today: ", date)
        if not type(date) == type(datetime.today()):
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            date = datetime.strptime(date, '%m/%d/%Y')
        ###     Not support high-frequency trading
        ###     Assume market does not change in a day, otherwise remove .date()
        if not date.date() == market.UpdatedDate.date():
        # if not date == market.UpdatedDate:
            print("WARRNING: trading-date and market-date not consistent.")
        
        if market == None:
            print("ERROR: Trading market needs to be specified.")
            sys.exit()
        
        if print_control:
            print('\n')
            print(_dash_line_)
            print("Make the following sell on date: {0} in Portfolio {1}".format(date, self.Name))
        return_values = 0
        for i in range(NumberOfSold):
            name = sell_namelist[i]
            amount = sell_values[i]
            if not name in self.NameList:
                print("ERROR: Product not in this portfolio. Check your sell-list.")
                sys.exit()
            idx = self.NameList.index(name)
            if amount > self.Values[idx]:
                print("ERROR: Not enought amount in {} to sell.".format(name))
                sys.exit()
        
            if print_control:
                str_product = str(self.Basket[idx])
                str_basket = "{0:10}      {1}".format(amount, self.Updates[idx])
                print(str_product + str_basket)

            return_values += self.Basket[idx].Price(amount, market, date)
            if amount == self.Values[idx]:
                self.Basket.pop(idx)
                self.NameList.pop(idx)
                self.Values.pop(idx)
                self.Updates.pop(idx)
                self.NumProducts -= 1
            else:
                self.Values[idx] -= amount
                self.Updates[idx] = date
            self.TotalValue += amount

        if print_control:
            print(_dash_line_)
            print("Left with the following products in Portfolio {0}:".format(self.Name))
            if self.NameList == []:
                print("<Empty basket>  ", "No products left.")
            for idx in range(len(self.NameList)):
                str_product = str(self.Basket[idx])
                str_basket = "{0:10}      {1}".format(self.Values[idx], self.Updates[idx])
                print(str_product + str_basket)
            print(_dash_line_)

        return self, return_values


    """
        inputs: buy_productlist     products of acquisition Instrument or list of Instrument
                values              values of acquisition   real-number or list of real-number
                date_list           dates of acquisition    list of datetime/string/None
                
        outputs:    self   updated portfolio   Portfolio
        """
    def Buy(self,
            market,
            buy_productlist,
            buy_values,
            date = None,
            print_control = True
            ):
        if buy_productlist == [] or buy_productlist == None:
            print("Note: No new instruments bought. Return the same Portfolio.")
            return self
        if not type(buy_productlist) == type(['list',]):
            buy_productlist = [buy_productlist,]
        if not type(buy_values) == type(['list',]):
            buy_values = [buy_values,]
        
        if buy_values == [] or buy_values == None:
            print("ERROR: Please provide par-values.")
            sys.exit()
        if type(buy_values[0]) != type(1.0) and type(buy_values[0]) != type(1):
            print("ERROR: Please provide numeric par-values.")
            sys.exit()
        if not len(buy_values) == len(buy_productlist):
            print("ERROR: Size mismatch. Please provide one par-value for each product.")
            sys.exit()

        # Default case
        if date == None:
            date = datetime.today()
            print("No date specified. Default buy today: ", date)
        # Type check
        if not type(date) == type(datetime.today()):
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            date = datetime.strptime(date, '%m/%d/%Y')

        names = _name_list_(buy_productlist)
        for idx in range(len(names)):
            if names[idx] in self.NameList:
                self.Values[idx] += buy_values[idx]
                self.Updates[idx] =  date
            else:
                self.Basket.append(buy_productlist[idx])
                self.Values.append(buy_values[idx])
                self.NameList.append(names[idx])
                self.NumProducts += 1
                self.Updates.append(date)
            self.TotalValue += buy_values[idx]


        cost = 0
        for idx in range(len(buy_productlist)):
            cost += buy_productlist[idx].Price(buy_values[idx],
                                               market,
                                               date)
        if print_control:
            print('\n')
            print(_dash_line_)
            print("Added the following holdings in Portfolio {0} on dates:".format(self.Name))
            for idx in range(len(buy_productlist)):
                str_product = str(buy_productlist[idx])
                str_basket = "{0:10}      {1}".format(buy_values[idx], date)
                print(str_product + str_basket)
            print(_dash_line_)

        return self, cost
        
    """
        inputs: market      market of trading   Market
                trade_date  date of trading     datetime/string

        outputs: price_list  list of all products prices in market on trade_date   list of real-numbers
        """
    def PriceList(self,
                  market,
                  trade_date = None
                  ):
        if market == None:
            print("ERROR: Trading market needs to be specified.")
            return None
        if trade_date == None:
            trade_date = datetime.today()
            print("No date specified. Default return today:  ", trade_date)
        elif type(trade_date) != type(datetime.today()):
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            trade_date = datetime.strptime(trade_date, '%m/%d/%Y')

        price_list = []
        for idx in range(len(self.Basket)):
            price_list.append(self.Basket[idx].Price(self.Values[idx],
                                                     market,
                                                     trade_date))
        return price_list


    """
        inputs: market      market of trading   Market
                trade_date  date of trading     datetime/string

        outputs: price  total prices in market on trade_date    list of real-numbers
        """
    def Price(self,
              market,
              trade_date = None
              ):
        price_list = self.PriceList(market, trade_date)
        return(sum(price_list))


    """
        inputs: market      market of trading   Market

        outputs: price  total prices in market today    list of real-numbers
        """
    def PriceToday(self,
                   market
                   ):
        today = datetime.today()
        return self.Price(market, today)





def _name_list_(basket):
    names = []
    for instrument in basket:
        if instrument.Name in names:
            print("ERROR: Product duplicated! Please check.")     # Maybe change to add par-values??
            sys.exit()
        names.append(instrument.Name)
    return names




