from ..apiUrls.main import XTS_URLS
import requests as rqs

class Message(XTS_URLS):
    def __init__(self):
        super().__init__()

    def ExchangeMessage(self,
                        exchangeSegment : int,
                        auth_token : str):
        EXCHANGE_MESSAGE_URL = fr"{self.base_url}/interactive/messages/exchange?exchangeSegment={exchangeSegment}"
        headers = {
            "Content-Type" : "application/json",
            "authorization": str(auth_token),
        }

        response = rqs.get(url = EXCHANGE_MESSAGE_URL,
                           headers = headers)
        
        if response.status_code == 200:
            print(fr"The get request from ExchangeMessage() was successful: {response}")
        else:
            print(fr"The get request from ExchangeMessage() was unsuccessful: {response}")





