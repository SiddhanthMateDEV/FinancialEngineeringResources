import pandas as pd
import numpy as np

class Straddle:
    def __init__(self) -> None:
        pass

    def getStranglePrices(self,
                          atm_strike = None,
                          interval = 100):
        
        if not any([atm_strike,interval]):
            raise ValueError("Empty parameters passed to the find_otms_strikes function")
        
        position_one_price = int(atm_strike - interval)
        position_two_price = int(atm_strike + interval)

        return (position_one_price, position_two_price)