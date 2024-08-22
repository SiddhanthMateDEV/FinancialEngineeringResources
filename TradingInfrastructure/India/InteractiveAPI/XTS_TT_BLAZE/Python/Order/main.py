import requests as rqs
from ..apiUrls.main import XTS_URLS

class Order(XTS_URLS):
    def __init__(self):
        super().__init__()

    def PlaceOrder(self,
                exchangeSegment : str,
                exchangeInstrumentID : int,
                productType : str,
                orderType : str,
                orderSide : str,
                timeInForce : str,
                disclosedQuantity : int,
                orderQuantity : int,
                limitPrice : float,
                stopPrice : float,
                orderUniqueIdentifier : str,
                auth_token : str):
        headers = {
            "Content-Type": "application/json",
            "authorization": auth_token
        }
        payload = {
            "exchangeSegment": str(exchangeSegment),
            "exchangeInstrumentID": int(exchangeInstrumentID),
            "productType": str(productType),
            "orderType": str(orderType),
            "orderSide": str(orderSide),
            "timeInForce": str(timeInForce),
            "disclosedQuantity": str(disclosedQuantity),
            "orderQuantity": str(orderQuantity),
            "limitPrice": float(limitPrice),
            "stopPrice": float(stopPrice),
            "orderUniqueIdentifier": str(orderUniqueIdentifier)
        }

        ORDER_URL = fr"{self.url}/interactive/orders"

        response = rqs.post(url = ORDER_URL,
                                 json = payload,
                                 headers = headers)
        
        if response.status_code == 200:
            print(fr"The get request from PlaceOrder() was successful: {response}")
        else:
            print(fr"The get request from PlaceOrder() was unsuccessful: {response}")


    def ModifyOrder(self,
                    appOrderID : int,
                    modifiedProductType : str,
                    modifiedOrderType : str,
                    modifiedOrderQuantity : int,
                    modifiedDisclosedQuantity : int,
                    modifiedLimitPrice : float,
                    modifiedStopPrice : float,
                    modifiedTimeInForce : str,
                    orderUniqueIdentifier : str,
                    clientID : str,
                    auth_token : str):
        MODIFIED_ORDER_URL = fr"{self.url}/interactive/orders?clientID={clientID}"
        headers = {
            "Content-Type": "application/json",
            "authorization": auth_token
        }
        payload = {
            "appOrderID": int(appOrderID),
            "modifiedProductType": str(modifiedProductType),
            "modifiedOrderType": str(modifiedOrderType),
            "modifiedOrderQuantity": int(modifiedOrderQuantity),
            "modifiedDisclosedQuantity": int(modifiedDisclosedQuantity),
            "modifiedLimitPrice": float(modifiedLimitPrice),
            "modifiedStopPrice": float(modifiedStopPrice),
            "modifiedTimeInForce": str(modifiedTimeInForce),
            "orderUniqueIdentifier": str(orderUniqueIdentifier)
        }

        response = rqs.put(url = MODIFIED_ORDER_URL,
                           json = payload,
                           headers = headers)
        

        if response.status_code == 200:
            print(fr"The get request from ModifyOrder() was successful: {response}")
        else:
            print(fr"The get request from ModifyOrder() was unsuccessful: {response}")

    def CancelOrder(self,
                    appOrderID : int,
                    orderUniqueIdentifier : str,
                    clientID : str,
                    auth_token : str):   
        headers = {
            "Content-Type": "application/json",
            "authorization": str(auth_token)
        }
        CANCEL_ORDER_URL = fr"{self.url}/interactive/orders?appOrderID={appOrderID}"

        response = rqs.delete(url = CANCEL_ORDER_URL,
                              headers = headers)
        
        if response.status_code == 200:
            print(fr"The get request from CancelOrder() was successful: {response}")
        else:
            print(fr"The get request from CancelOrder() was unsuccessful: {response}")

    
    def CancelAllOrder(self,
                       exchangeSegment : str,
                       exchangeInstrumentID : int,
                       auth_token : str):
        
        CANCEL_ALL_ORDER_URL = fr"{self.url}/interactive/orders/cancelall"
        headers = {
            "Content-Type": "application/json",
            "authorization": str(auth_token)
        }
        payload = {
            "exchangeSegment" : str(exchangeSegment),
            "exchangeInstrumentID" : int(exchangeInstrumentID)    
        }

        response = rqs.post(url = CANCEL_ALL_ORDER_URL,
                            headers = headers,
                            json = payload)
        
        if response.status_code == 200:
            print(fr"The get request from CancelAllOrder() was successful: {response}")
        else:
            print(fr"The get request from CancelAllOrder() was unsuccessful: {response}")

    
    def OrderBook(self,
                  clientID : str,
                  auth_token : str):
        ORDER_BOOK_URL = fr"{self.url}/interactive/orders"
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token)
        }
        response = rqs.get(url = ORDER_BOOK_URL,
                            headers = headers)

        if response.status_code == 200:
            print(fr"The get request from OrderBook() was successful: {response}")
        else:
            print(fr"The get request from OrderBook() was unsuccessful: {response}")

    
    def OrderHistory(self,
                     appOrderID : int,
                     auth_token : str):
        ORDER_HISTORY_URL = fr"{self.url}/interactive/orders?appOrderID={appOrderID}"
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token)
        }
        response = rqs.get(url = ORDER_HISTORY_URL,
                            headers = headers)

        if response.status_code == 200:
            print(fr"The get request from OrderHistory() was successful: {response}")
        else:
            print(fr"The get request from OrderHistory() was unsuccessful: {response}")

    
    def TradeBook(self,
                  clientID : str,
                  auth_token : str):
        ORDER_HISTORY_URL = fr"{self.url}/interactive/orders?clientID={clientID}"        
        headers = {
            "Content-Type" : "application/json",
            "authorization" : str(auth_token)
        }   
        response = rqs.get(url = ORDER_HISTORY_URL,
                           headers = headers)

        if response.status_code == 200:
            print(fr"The get request from OrderHistory() was successful: {response}")
        else:
            print(fr"The get request from OrderHistory() was unsuccessful: {response}")
    



        

        
     