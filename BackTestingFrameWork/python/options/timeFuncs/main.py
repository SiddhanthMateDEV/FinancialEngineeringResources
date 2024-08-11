from datetime import datetime


class OptionsTimeFunctions:
    def __init__(self) -> None:
        pass

    """
    This function is made to trim the timestamp in the expiry 
    such that that the option expires on that day at 15:30:00Hrs
    """
    def SetEndOfDay(self,dt):
        return dt.replace(hour = 15, minute = 30, second = 00)
    
    """
    This function is made to trim the dataset for a desired time interval
    """
    def TimeFilter(self,
                         data = None,
                         start = None,
                         end = None):
        
        if not any([start,end,data]):
            raise ValueError("Empty parameters passed to the apply_time_mask function")
        
        mask = ((data['datetime'].dt.time >= start) & (data['datetime'].dt.time <= end))
        return data[mask]