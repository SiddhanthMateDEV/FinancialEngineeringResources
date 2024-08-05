import numpy as np 
from scipy.stats import norm

class BlackScholes:
    def __init__(self) -> None:
        pass

    def calc(self,
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
        