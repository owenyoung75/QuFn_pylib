from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from lib_Asset.MarketEnvs import *
from lib_Asset.FinInstrument import *
from lib_Asset.Bond import *
from lib_Asset.Asset import *

from lib_Asset.Write_Read import *


yield_curve = {}
yield_curve[1] = 0.0187
yield_curve[3] = 0.0198
yield_curve[6] = 0.0216
yield_curve[12] = 0.0237
yield_curve[12*2] = 0.0259
yield_curve[12*3] = 0.0266
yield_curve[12*5] = 0.0273
yield_curve[12*7] = 0.0280
yield_curve[12*10]= 0.0283
yield_curve[12*15]= 0.0300

market = TreasureMarket(datetime.today(), 0.0198)
market.Set_TermStructure(yield_curve)

bond1 = Bond("Bond_a",
             '09/01/2021',
             6,
             0.023)
bond2 = Bond("Bond_b",
             '09/01/2023',
             6,
             0.053)
bond3 = Bond("Bond_c",
             '09/01/2028',
             12,
             0.083)
bond4 = Bond("Bond_d",
             '09/01/2028',
             12,
             0.080)
bond5 = Bond("Bond_e",
             '09/01/2028',
             12,
             0.081)

basket1 = [bond1,  bond2]; face_values1 = [100, 1000]
basket2 = [bond2,  bond3]; face_values2 = [200, 5000]
ptf1 = BondPortfolio("PTFA", basket1, face_values1)
ptf2 = BondPortfolio("PTFB", basket2, face_values2)




asset_version0 = Asset("PaoPao", 10000000, [ptf1])
asset_version0.PrintDetails()
Assets_Writing(asset_version0)




asset_version1 = Assets_Reading('PaoPao')
asset_version1.Remember([bond4])
asset_version1.TradeEvent("BUY", market,
                          [bond2, bond3],
                          [  90,  700  ]
                          )
asset_version1.TradeEvent("BUY", market,
                          ['Bond_a', 'Bond_c'],
                          [  50,        100  ]
                          )

asset_version1.PrintDetails()
Assets_Writing(asset_version1)




asset_version2 = Assets_Reading('PaoPao', '08/21/2018')
asset_version2.AddPortfolio(ptf2)
asset_version2.TradeEvent("SELL", market,
                          ['Bond_c', 'Bond_b'],
                          [  50,        50  ],
                          ptf_name = 'PTFB'
                          )
asset_version2.PrintDetails()
Assets_Writing(asset_version2)


