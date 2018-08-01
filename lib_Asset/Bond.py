from datetime import datetime
from .FinInstrument import *

name_length = 10



class Bond(Instrument):
    """
        Class: Bond
        
        attribute: Class            Debt                                string
        attribute: Type             Bond                                string
        attribute: Name             bond name                           string
        attribute: CouponRatio      annual coupon rate                  real-number
        attribute: CouponFrequency  number of months for coupon payment integer
        
        method: __price__   internal calculation of price   return: real-number
        method: Price       calculate bond price            return: real-number
        method: PriceToday  calculate today's bond price    return: real-number
        """
    def __init__(self,
                 name = 'name',
                 maturity_date = datetime.today(),
                 coupon_frequency = 6,
                 coupon_ratio = 0
                 ):
        super().__init__(name, _class="Debt", _type="Bond")
        self.CouponRatio = coupon_ratio
        self.CouponFrequency = coupon_frequency
        if type(maturity_date) == type(datetime.today()):
            self.MaturityDate = maturity_date
        else:
#            print("Transform date-string into datetime structure.")
#            print("Note: date format should be mm/dd/yy.")
            self.MaturityDate = datetime.strptime(maturity_date, '%m/%d/%Y')

    def __str__(self):
        string = "--- {0:10}  {1:15}  {2}     ".format(self.Type, self.Name, self.MaturityDate.date())
        return string


    """
        inputs: _par_value  par-value of bond   real-number
                _periods    peorid left         integer
                _yeild      yield value         real-number
                
        outputs: price      price of bond   real-number
        """
    def __price__(self,
                  _par_value,
                  _periods,
                  _yield
                  ):

        from_par = _par_value / (1.0 + _yield)**_periods
        from_coupon = 0
        for i in range(_periods):
            from_coupon += _par_value * self.CouponRatio / (1.0 + _yield)**(i+1)
        return (from_par + from_coupon)


    """
        inputs: par_value       face value of bond          real-number
                treasure_market treasure market of trading  TreasureMarket
                trade_date      trading dates               datetime/string
        
        outputs: price  bond price on trade_date in treasure_market   real-number
        """
    def Price(self,
              par_value,
              treasure_market,
              trade_date = None,
              ):
        if trade_date == None:
            print("No date set. Default return: today's price.")
            trade_date = datetime.today()
        if type(trade_date) != type(datetime.today()):
#            print("Transform date-string into datetime structure.")
#            print("Note: date format should be mm/dd/yy.")
            trade_date = datetime.strptime(trade_date, '%m/%d/%Y')
    
        months_left = (self.MaturityDate.year - trade_date.year) * 12 + (self.MaturityDate.month - trade_date.month)
        periods_left = int(months_left/self.CouponFrequency + 1)

        if treasure_market == None:
            print("ERROR: Treasure market needs to be defined.")
            return None
        if months_left < 0:
            print("ERROR: Trade cannot be after maturity.")
            return None
        if par_value < 0:
            print("ERROR: Par-value cannot be negative.")
            return None

        ### locate trade-time on the yield-curve ###
        term_structure = treasure_market.TermStructure
        terms = list(term_structure.keys())
        idx = 0
        while terms[idx] < months_left:
            idx += 1
            if idx == len(terms):
                print("ERROR: Provided term-structure not long enough. Please specify longer yield curves!")
                return None
        less_than   = terms[idx]
        longer_than = terms[idx-1]
        yield_1 = term_structure[longer_than]
        yield_2 = term_structure[less_than]
        if idx == 0:
            longer_than = 0
        yield_to_maturity = yield_1 + (yield_2-yield_1) * (months_left - longer_than) / (less_than - longer_than)

        return self.__price__(par_value,
                              periods_left,
                              yield_to_maturity)


    """
        inputs: par_value       face value of bond          real-number
                treasure_market treasure market of trading  TreasureMarket
    
        outputs: price  price of bond today in treasure_market   real-number
        """
    def PriceToday(self,
                   par_value,
                   market_today
                   ):
        today = datetime.today()
        return self.Price(par_value,
                          market_today,
                          today)






class BondPortfolio(Portfolio):
    """
        Class: portfolio only with bond
        
        attribute: Name         name of portfolio           string
        attribute: Basket       all bonds                   list of Instrument
        attribute: BondsBasket  all bonds                   list of Instrument
        attribute: Values       all bond values             list of real-number
        attribute: ParValues    all bond values             list of real-number
        attribute: Namelist     all bond names              list of strings
        attribute: TotalValues  total value of portfolio    real-value
        attribute: NumProducts  number of bonds included    integer
        attribute: Updates      updating dates of each bond list of datetime/string
        
        method: __call__        get info of bond given name     return: Bond, [real-number, datetime]
        method: _promote        promote to a general Portfolio  return: BondPortfolio
        method: PrintDetails    print details of all bonds      return: string
        method: Sell            a sell event                    return: BondPortfolio, real-number
        method: Buy             a buy event                     return: BondPortfolio
        method: PriceList       prices of each bond             return: list of real-number
        method: Price           total portfolio price           return: real-number
        method: PriceToday      total portfolio price today     return: real-number
        """
    def __init__(self,
                 name,
                 bonds_basket,
                 par_values,
                 buy_dates = None
                 ):
        super().__init__(name, bonds_basket, par_values, buy_dates)
        self.BondsBasket = bonds_basket
        self.ParValues = par_values


    def _promote(self):
        general_portfolio = Portfolio("Promoted"+self.Name,
                                      self.BondsBasket.copy(),
                                      self.ParValues.copy(),
                                      self.BuyDates.copy())
        return general_portfolio
    
    def __str__(self):
        str1 =  "BondPortfolio Name: {0} {1}".format(self.Name,'\n')
        str2 = "With {0} bonds,  TotalValue = {1}".format(self.NumProducts, self.TotalValue)
        return str1 + str2

    def PrintDetails(self):
        dashed_line = '-' * 36
        
        print()
        print( dashed_line + " <BondPortfolio Object> " + dashed_line )
        print(str(self))
        print("Including the following bonds:")
        print("    {0:10}  {1:15}  {2:12}     {3:10}      {4}".format("Type",
                                                                      "Name",
                                                                      "Maturity",
                                                                      "Face Value",
                                                                      "Buy Date"))
        for idx in range(len(self.NameList)):
            str_bond = str(self.BondsBasket[idx])
            str_basket = "{0:10}      {1}".format(self.ParValues[idx], self.Updates[idx])
            print(str_bond + str_basket)
        print( dashed_line + " <BondPortfolio Object> " + dashed_line )
        return None


    def Buy(self,
            market,
            bond_list,
            par_values,
            _date = None,
            _print_control = True
            ):
        if bond_list == [] or bond_list == None:
            print("Note: No new bonds bought. Return the same Portfolio.")
            return self
        if not type(bond_list) == type(['list',]):
            bond_list = [bond_list,]
        if not type(bond_list[0]) == type(self.BondsBasket[0]):
            print("WARNING: This is a bond-portfolio, other product types should not be added.")
            print("         You may create a general Portfolio object using _promote() method.")
        return super(BondPortfolio, self).Buy(market,
                                              bond_list,
                                              par_values,
                                              _date,
                                              _print_control)


#    """
#        inputs: market      market of trading   TreasureMarket
#                trade_date  date of trading     datetime/string
#        
#        outputs: price_list  list of all bonds prices in market on trade_date   list of real-numbers
#        """
#    def PriceList(self,
#                  market,
#                  trade_date = None
#                  ):
#        if market == None:
#            print("ERROR: Trading market needs to be specified.")
#            return None
#        if trade_date == None:
#            trade_date = datetime.today()
#            print("No date specified. Default return today:  ", trade_date)
#        elif type(trade_date) != type(datetime.today()):
#            print("Transform date-string into datetime structure.")
#            print("Note: date format should be mm/dd/yy.")
#            trade_date = datetime.strptime(trade_date, '%m/%d/%Y')
#
#        price_list = []
#        for idx in range(len(self.BondsBasket)):
#            price_list.append(self.BondsBasket[idx].Price(self.ParValues[idx],
#                                                          market,
#                                                          trade_date))
#        return price_list
#                     
#
#    """
#        inputs: market      market of trading   TreasureMarket
#                trade_date  date of trading     datetime/string
#    
#        outputs: price  total prices in market on trade_date    list of real-numbers
#        """
#    def Price(self,
#              market,
#              trade_date = None
#              ):
#        price_list = self.PriceList(market, trade_date)
#        return(sum(price_list))
#    
#    
#    """
#        inputs: market      market of trading   TreasureMarket
#        
#        outputs: price  total prices in market today    list of real-numbers
#        """
#    def PriceToday(self,
#                   market
#                   ):
#        today = datetime.today()
#        return self.Price(market, today)


