import numpy as np 
from scipy.stats import norm 
import pandas as pd
from timeFuncs.main import OptionsTimeFunctions
from datetime import datetime


class OptionsFormulaBook(OptionsTimeFunctions):
    def __init__(self):
        super.__init__()

    def calculateOptionPremium(self,
                strike_price = None, 
                spot_price = None, 
                time_to_maturity = None, 
                rate_of_interest = 7/100, 
                sigma = 0.2, 
                option_type = None):

        d1 = ((np.log(spot_price/strike_price)) + ((rate_of_interest)+((sigma**2)/2))*time_to_maturity)/(sigma*np.sqrt(time_to_maturity))
        d2 = d1 - sigma*(np.sqrt(time_to_maturity))

        if option_type == 'CE' or option_type == 'c':
            return float(((spot_price*norm.cdf(d1)) - (strike_price*np.exp(-rate_of_interest*time_to_maturity)*norm.cdf(d2))))
        elif option_type == 'PE' or option_type == 'p':
            return float(((strike_price*np.exp(-rate_of_interest*time_to_maturity)*norm.cdf(-d2)) - (spot_price*norm.cdf(-d1))))
        else:
            raise ValueError("Invalid Option Type")
        
    def filterOptionsByType(self,
                              df = None):
        call_data = df[df['option_type'] == 'c']
        put_data = df[df['option_type'] == 'p']
        return (call_data, put_data)
        
    def straddlePrice(self, 
                      call_price = None,
                      put_price = None):
        return call_price + put_price
    
    def nearestAtmStrike(self, spot_price = None, strike_prices = None):
        return min(strike_prices, key = lambda x: abs(x-spot_price))
    
    def closestStrike(self, 
                      price = None, 
                      interval = 100):
        return int(round(price/interval)*interval)
        

    
