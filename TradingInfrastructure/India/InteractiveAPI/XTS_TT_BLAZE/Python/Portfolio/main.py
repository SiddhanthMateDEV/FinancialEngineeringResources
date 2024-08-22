import requests as rqs
from ..apiUrls.main import XTS_URLS

class Portfolio(XTS_URLS):
    def __init__(self):
        super().__init__()

    def Holding(self,
                clientID : str,
                auth_token : str):
        
        if clientID is None:
            clientID = "SYMP1"

        HOLDING_URL = fr"{self.base_url}/interactive/portfolio/holdings?clientID={clientID}"
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token) 
        }

        response = rqs.get(url = HOLDING_URL,
                           headers = headers)
        
        if response.status_code == 200:
            print(fr"The get request from Holding() was successful: {response}")
        else:
            print(fr"The get request from Holding() was unsuccessful: {response}")



    def Position(self,
                 dayOrNet : str,
                 auth_token : str):    
            
        if dayOrNet is None:
            dayOrNet = "DayWise"

        POSITION_URL = fr"{self.base_url}/interactive/portfolio/positions?dayOrNet={str(dayOrNet)}"
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token)
        }
        response = rqs.get(url = POSITION_URL,
                           headers = headers)

        if response.status_code == 200:
            print(fr"The get request from Position() was successful: {response}")
        else:
            print(fr"The get request from Position() was unsuccessful: {response}")

    
    def PositionConvert(self,
                        exchangeSegment : str,
                        exchangeInstrumentID : int,
                        oldProductType : str,
                        newProductType : str,
                        isDayWise : bool,
                        targetQty : int,
                        statisticsLevel : str,
                        isInterOpPosition : bool,
                        auth_token : str):
        POSITION_CONVERT_URL = fr"{self.base_url}/interactive/portfolio/positions/convert"
        
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token)
        }
        payload = {
            "exchangeSegment": str(exchangeSegment),
            "exchangeInstrumentID": int(exchangeInstrumentID),
            "oldProductType": str(oldProductType),
            "newProductType": str(newProductType),
            "isDayWise": bool(isDayWise),
            "targetQty": int(targetQty),
            "statisticsLevel": str(statisticsLevel),
            "isInterOpPosition": bool(isInterOpPosition)
        }   

        response = rqs.put(url = POSITION_CONVERT_URL,
                           headers = headers,
                           json = payload)
        
        if response.status_code == 200:
            print(fr"The get request from PositionConvert() was successful: {response}")
        else:
            print(fr"The get request from PositionConvert() was unsuccessful: {response}")





           
        

