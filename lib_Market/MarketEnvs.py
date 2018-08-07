from datetime import datetime

from .market_records import *


class Market:
    """
        Class:  general financial market
        
        attribute:  UpdatedDate     date of market info collected   datetime
        """
    def __init__(self,
                 _date
                 ):
        if _date == None:
            print("No date specified. Default return: today's market.")
            self.UpdatedDate = datetime.today()
        elif type(_date) == type(datetime.today()):
            self.UpdatedDate = _date
        else:
            print("Transform date-string into datetime structure.")
            print("Note: date format should be mm/dd/yy.")
            self.UpdatedDate = datetime.strptime(_date, '%m/%d/%Y')
        self.Records = []

    def store(self,
              market_recd
              ):
        self.Records.append(market_recd)



class TreasureMarket(Market):
    """
        Class:  general treasure market
        
        attribute:  UpdatedDate     date of market info collected   datetime
        attribute:  RiskFreeRate    risk free rate                  real-number
        attribute:  DurationRisk    duration risk                   real-number
        attribute:  TermStructure   yield curve                     dictionary {integer: real-number}
        
        method: Set_TermStructure   set up yield curve      return: None
        """
    def __init__(self,
                 date,
                 risk_free_rate,
                 term_structure = None,
                 duration_risk = None
                 ):
        super().__init__(date)
        self.RiskFreeRate = risk_free_rate
        self.DurationRisk = duration_risk
        self.TermStructure = term_structure


    """
        inputs: input_dict  yield values of different months    dictionary {integer: real-number}
        """
    def Set_TermStructure(self,
                          input_dict
                          ):
        self.TermStructure = input_dict
                 






