import pandas as pd
import numpy as np
# from timeFuncs.main import OptionsTimeFunctions


class Straddle:
    def __init__(self):
        super().__init__

    def filterByExpiryAndStrike(self,
                            data = None, 
                            time = None,
                            expiry = None,
                            strike_price = None,
                            start_trade_time = None,
                            end_trade_time = None,
                            ): 
        
        time = pd.to_datetime(str(time)).time()
        try:
            # dont add an if to check data empty its already being checked in TimeFilter
            data = self.TimeFilter(data = data,
                                                start = start_trade_time,
                                                end = end_trade_time)
        except Exception as e:
            raise ImportError("Something went wrong in filterByExpiryAndStrike() while calling TimeFilter()")
        
        grouped_call_data = data[(data['expiry'] == expiry) & (data['option_type'] == 'c') & (data['strike_price'] == strike_price)].reset_index(drop = True)
        grouped_put_data = data[(data['expiry'] == expiry) & (data['option_type'] == 'p') & (data['strike_price'] == strike_price)].reset_index(drop = True)

        if len(grouped_call_data) != len(grouped_put_data):
            raise KeyError("Length of call and put grouped data does not match in filterByExpiryAndStrike()")

        return (grouped_call_data, grouped_put_data)
    

