import numpy as np
import pandas as pd
import random 
import time
import redis


from collections import deque 
from datetime import datetime



class EventSimulatorXTS:
    def __init__(self) -> None:
        pass


        
    def generate_synthetic_data_1512(self):
        message_code = 1510
        message_version = 4
        application_type = 0
        token_id = 0
        exchange_segment = 2
        exchange_instrument_id = random.choice([48542, 48543, 48544])
        exchange_timestamp = int(time.time()) - random.randint(0, 1000)
        xts_market_type = 1
        open_interest = random.randint(740000, 750000)
        underlying_instrument_id = 0
        underlying_exchange_segment = 1
        underlying_id_index_name = "NIFTY BANK"
        underlying_total_open_interest = random.randint(72000000, 73000000)
        sequence_number = random.randint(1470762261880000, 1470762261890000)

        data_dict = {
            "MessageCode": message_code,
            "MessageVersion": message_version,
            "ApplicationType": application_type,
            "TokenID": token_id,
            "ExchangeSegment": exchange_segment,
            "ExchangeInstrumentID": exchange_instrument_id,
            "ExchangeTimeStamp": exchange_timestamp,
            "XTSMarketType": xts_market_type,
            "OpenInterest": open_interest,
            "UnderlyingInstrumentID": underlying_instrument_id,
            "UnderlyingExchangeSegment": underlying_exchange_segment,
            "UnderlyingIDIndexName": underlying_id_index_name,
            "UnderlyingTotalOpenInterest": underlying_total_open_interest,
            "SequenceNumber": sequence_number
        }
        return data_dict

    def generate_synthetic_data_1502(self):
        return {
            "MessageCode": 1502,
            "MessageVersion": 4,
            "ApplicationType": 0,
            "TokenID": 0,
            "ExchangeSegment": 2,
            "ExchangeInstrumentID": random.randint(40000, 50000),
            "ExchangeTimeStamp": int(time.time()),
            "Bids": [
                {"Size": random.randint(10, 300), 
                "Price": round(random.uniform(257, 260), 2), 
                "TotalOrders": random.randint(1, 6), 
                "BuyBackMarketMaker": 0} for _ in range(5)
            ],
            "Asks": [
                {"Size": random.randint(100, 450), 
                "Price": round(random.uniform(258, 261), 2), 
                "TotalOrders": random.randint(1, 6), 
                "BuyBackMarketMaker": 0} for _ in range(5)
            ],
            "Touchline": {
                "BidInfo": {"Size": random.randint(10, 300), 
                            "Price": round(random.uniform(257, 260), 2), 
                            "TotalOrders": random.randint(1, 6), 
                            "BuyBackMarketMaker": 0},
                "AskInfo": {"Size": random.randint(100, 450), 
                            "Price": round(random.uniform(258, 261), 2), 
                            "TotalOrders": random.randint(1, 6), 
                            "BuyBackMarketMaker": 0},
                "LastTradedPrice": round(random.uniform(258, 261), 2),
                "LastTradedQuantity": random.randint(10, 100),
                "TotalBuyQuantity": random.randint(80000, 90000),
                "TotalSellQuantity": random.randint(150000, 200000),
                "TotalTradedQuantity": random.randint(30000000, 32000000),
                "AverageTradedPrice": round(random.uniform(260, 270), 2),
                "LastTradedTime": int(time.time()) - 1,
                "LastUpdateTime": int(time.time()),
                "PercentChange": round(random.uniform(-20, 20), 2),
                "Open": round(random.uniform(250, 310), 2),
                "High": round(random.uniform(310, 370), 2),
                "Low": round(random.uniform(190, 250), 2),
                "Close": round(random.uniform(300, 310), 2),
                "TotalValueTraded": None,
                "BuyBackTotalBuy": 0,
                "BuyBackTotalSell": 0
            },
            "BookType": 1,
            "XMarketType": 1,
            "SequenceNumber": random.randint(1_000_000_000_000_000, 2_000_000_000_000_000)
        }


    def generate_synthetic_data_1501(self):
        return {
            "MessageCode": 1501,
            "MessageVersion": 4,
            "ApplicationType": 0,
            "TokenID": random.randint(1000, 9999),
            "ExchangeSegment": 2,
            "ExchangeInstrumentID": random.randint(10000, 99999),
            "ExchangeTimeStamp": int(time.mktime(datetime.now().timetuple())),
            "BookType": random.choice([1, 2]),
            "XMarketType": random.choice([1, 2]),
            "SequenceNumber": random.randint(1000000000000000, 9999999999999999),
            "Touchline": {
                "LastTradedPrice": round(random.uniform(200, 400), 2),
                "LastTradedQuantity": random.randint(1, 100),
                "TotalBuyQuantity": random.randint(50000, 150000),
                "TotalSellQuantity": random.randint(50000, 150000),
                "TotalTradedQuantity": random.randint(10000000, 50000000),
                "AverageTradedPrice": round(random.uniform(200, 400), 2),
                "LastTradedTime": int(time.mktime(datetime.now().timetuple())) - 1,
                "LastUpdateTime": int(time.mktime(datetime.now().timetuple())),
                "PercentChange": round(random.uniform(-20, 20), 2),
                "Open": round(random.uniform(200, 400), 2),
                "High": round(random.uniform(200, 400), 2),
                "Low": round(random.uniform(150, 250), 2),
                "Close": round(random.uniform(200, 400), 2),
                "TotalValueTraded": random.choice([None, round(random.uniform(100000, 500000), 2)]),
                "BuyBackTotalBuy": random.randint(0, 1000),
                "BuyBackTotalSell": random.randint(0, 1000),
                "AskInfo": {
                    "Size": random.randint(50, 150),
                    "Price": round(random.uniform(200, 400), 2),
                    "TotalOrders": random.randint(1, 10),
                    "BuyBackMarketMaker": random.randint(0, 1),
                },
                "BidInfo": {
                    "Size": random.randint(50, 150),
                    "Price": round(random.uniform(200, 400), 2),
                    "TotalOrders": random.randint(1, 10),
                    "BuyBackMarketMaker": random.randint(0, 1),
                }
            }
        }
    
    def __del__(self):
        print("Deleting Simulator Instance")

    def delete_instance(self):
        del self

    def publish_to_redis(self,
                         redis_client = None , 
                         channel = None, 
                         data = None):
        if not all([redis_client,channel, data]):
            return

        redis_client.publish(str(channel),data)


    def run_synthetic_data_producer(self,redis = None,channel_name = ["1502_json",
                                                                    "1501_json",
                                                                    "1512_json"]):
        count = 0
        while True:
            data = None
            data_1502 = self.generate_synthetic_data_1502()
            data_1501 = self.generate_synthetic_data_1501()
            data_1512 = self.generate_synthetic_data_1512()

            
            print(data_1501)
            print(data_1502)

            self.publish_to_redis(redis_client = redis,channel=channel_name[1], data = str(data_1501))
            self.publish_to_redis(redis_client = redis,channel=channel_name[0], data = str(data_1502))
            self.publish_to_redis(redis_client = redis,channel=channel_name[2], data = str(data_1512))
            
            count+=1
            print(count)
            time.sleep(0.1)
            if count>10000:
                del self
                break

def main():
    redis_client = redis.Redis(host = "localhost", port = 6379, db = 1)
    sim = EventSimulatorXTS()
    sim.run_synthetic_data_producer(redis = redis_client)



    
if __name__ == "__main__":
    main()