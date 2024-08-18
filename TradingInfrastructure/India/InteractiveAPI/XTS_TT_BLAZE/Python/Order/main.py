from ..User.main import User
import requests as rqs

class Order(User):
    def __init__(self, url="https://ttblaze.iifl.com", 
                 access_password="2021HostLookUpAccess", 
                 version="interactive_1.0.1", 
                 secretKey=None, 
                 apiKey=None):
        super().__init__(url, access_password, version, secretKey, apiKey)


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
                orderUniqueIdentifier : str):

        order_headers = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }

        order_payload = {
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

        order_response = rqs.post(url = ORDER_URL,
                                 json = order_payload,
                                 headers = order_headers)
        
        if order_response.status_code == 200:
            print(fr"The get request from PlaceOrder() was successful: {order_response}")
        else:
            print(fr"The get request from PlaceOrder() was unsuccessful: {order_response}")

        
     