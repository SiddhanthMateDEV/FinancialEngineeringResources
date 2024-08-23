import sys
import os

import socketio
import configparser
import time


# Just pointing the path to parent dir for imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

sys.path.insert(0,parent_dir)

from config.product_config.main import ProductConfig
from config.route_config.main import RouteConfig
from subscribe.main import SubscribedInstruments
from config.xts_message_codes.main import XtsMessageCodes
from auth.main import MarketDataApiCredentials
from database_operations.mongo_writer.main import MongoWriter
from database_operations.redis_handler.main import RedisHandler


import asyncio
from urllib.parse import urljoin
import requests as rqs
import json 
import socketio
from pymongo import MongoClient
import redis 
from itertools import product
import aiohttp
from threading import Timer

import logging
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=2), 
        logging.StreamHandler() 
    ]
)

logger = logging.getLogger(__name__)


class WebSocket(MarketDataApiCredentials,
                RedisHandler,
                ProductConfig,
                MongoWriter,
                RouteConfig,
                SubscribedInstruments,
                XtsMessageCodes,
                ):
    
    def __init__(self,
                 root_url = "http://ttblaze.iifl.com",
                 mongo_uri = "mongodb://localhost:27017",
                 db_name = "XTS_WEBSOC_DATA",
                 coll_name = None,
                 publish_format = "JSON",
                 broadcast_mode = "Full",
                 socket_path = "/marketdata/socket.io",
                 ):
        
        MarketDataApiCredentials.__init__(self)
        RedisHandler.__init__(self)
        ProductConfig.__init__(self)
        MongoWriter.__init__(self)
        RouteConfig.__init__(self)  
        SubscribedInstruments.__init__(self)
        XtsMessageCodes.__init__(self)

        self.root_url = root_url
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[str(db_name)]
        self.mongo_coll = self.mongo_db[str(coll_name)]
        self.publish_format = publish_format
        self.broadcast_mode = broadcast_mode
        self.socket_path = socket_path
        self.socket = socketio.Client()
        
    async def _request(self, 
                   route=None, 
                   method_req=None, 
                   parameters=None, 
                   pool=None):
    
        params = parameters or {}

        try:
            uri = self._routes[str(route)].format(**params)
            url = urljoin(self.root_url, uri)
            logger.info(f"Accessing URL: {url}")
        except KeyError as e:
            logger.error(f"Key error for self._routes: {route}. Details: {str(e)}", exc_info=True)
            raise ValueError(f"Key error for self._routes: {route}. Ensure the route is correctly defined and the parameters match the expected format. Details: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error when constructing URL: {str(e)}", exc_info=True)
            raise ValueError(f"Unexpected error when constructing URL: {str(e)}") from e

        header = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method_req,
                    url=url,
                    headers=header,
                    json=params if method_req in ["POST", "PUT"] else None,
                    params=params if method_req in ["GET", "DELETE"] else None,
                    ssl=False
                ) as response:
                    try:
                        response.raise_for_status()
                    except aiohttp.ClientResponseError as e:
                        logger.warning(f"HTTP Error {e.status} during request to {url}: {e.message}", exc_info=True)
                        raise ValueError(f"HTTP Error {e.status} during request to {url}: {e.message}") from e

                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError as e:
                        logger.error(f"Failed to decode JSON response from {url}. Response content-type: {response.content_type}. Details: {str(e)}", exc_info=True)
                        raise ValueError(f"Failed to decode JSON response from {url}. Response content-type: {response.content_type}. Details: {str(e)}") from e
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON response from {url}. Response: {await response.text()}. Details: {str(e)}", exc_info=True)
                        raise ValueError(f"Failed to parse JSON response from {url}. Response: {await response.text()}. Details: {str(e)}") from e

            except aiohttp.ClientError as e:
                logger.error(f"Network-related error occurred during request to {url}: {str(e)}", exc_info=True)
                raise ValueError(f"Network-related error occurred during request to {url}: {str(e)}") from e
            except Exception as e:
                logger.critical(f"Unexpected error occurred during the request to {url}. Details: {str(e)}", exc_info=True)
                raise ValueError(f"Unexpected error occurred during the request to {url}. Details: {str(e)}") from e

    

    async def _post(self, route_param=None, params=None):
        try:
            response = await self._request(route=route_param,
                                           method_req="POST",
                                           parameters=params,
                                           pool=None)

            if response.status >= 200 and response.status < 300:
                try:
                    data = await response.json()
                    return data
                except json.JSONDecodeError as json_err:
                    print(f"Failed to parse JSON: {json_err}")
                    return {"error": "Invalid JSON response"}
            else:
                print(f"Request failed with status code: {response.status}")
                return {"error": f"HTTP Error: {response.status}", "details": await response.text()}

        except aiohttp.ClientConnectionError as conn_err:
            print(f"Connection error: {conn_err}")
            return {"error": "Connection error", "details": str(conn_err)}

        except aiohttp.ClientResponseError as resp_err:
            print(f"Response error: {resp_err}")
            return {"error": f"Response error: {resp_err.status}", "details": str(resp_err)}

        except asyncio.TimeoutError as timeout_err:
            print(f"Request timed out: {timeout_err}")
            return {"error": "Timeout error", "details": str(timeout_err)}

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"error": "Unexpected error", "details": str(e)}

    async def send_subscription(self, instruments=None, xts_message_codes=None):
        try:
            if instruments is None or xts_message_codes is None:
                logger.error("Instruments and xts_message_codes cannot be None")
                raise ValueError("Instruments and xts_message_codes cannot be None")
            
            responses = []
            for instrument, code in product(instruments, xts_message_codes):
                params_code = {
                    'instruments': instrument,
                    'xtsMessageCode': code,
                }
                
                try:
                    response = await self._post(route_param='market.instruments.subscription', 
                                                params=params_code)
                    logger.debug(f"Subscribing to instrument {instrument} with code {code}")
                    responses.append(response)
                    logger.info(f"Successfully subscribed to instrument {instrument} with code {code}")
                except ConnectionError as ce:
                    logger.error(f"Connection error while subscribing to instrument {instrument} with code {code}", exc_info=True)
                    raise ConnectionError(f"Failed to connect while subscribing to instrument {instrument} with code {code}") from ce
                except TimeoutError as te:
                    logger.warning(f"Timeout error while subscribing to instrument {instrument} with code {code}", exc_info=True)
                    raise TimeoutError(f"Request timed out while subscribing to instrument {instrument} with code {code}") from te
                except Exception as e:
                    logger.critical(f"Unexpected error occurred while subscribing to instrument {instrument} with code {code}", exc_info=True)
                    raise RuntimeError(f"An unexpected error occurred while subscribing to instrument {instrument} with code {code}") from e
            logger.info("All subscriptions processed successfully.")
            return responses
        except ValueError as ve:
            logger.error("ValueError in send_subscription method", exc_info=True)
            raise
        except Exception as e:
            logger.critical("Critical error in send_subscription method", exc_info=True)
            raise ValueError("Error in sending subscription") from e
        

    async def subscribe_to_codes(self):
        try:
            if not self.subscribe_payload or not self.xts_message_codes:
                logger.error("Subscription payload or message codes cannot be empty")
                raise ValueError("Subscription payload or message codes cannot be empty")
            
            logger.debug(f"Starting subscription with payload: {self.subscribe_payload} and message codes: {self.xts_message_codes}")
            response = await self.send_subscription(instruments=self.subscribe_payload, 
                                                    xts_message_codes=self.xts_message_codes)
            logger.info("Subscription successful")
            return response
        
        except ValueError as ve:
            logger.error(f"Validation error in subscribing to codes: {ve}", exc_info=True)
            raise ValueError(f"Validation error in subscribing to codes: {ve}") from ve
        except ConnectionError as ce:
            logger.error(f"Connection error during subscription: {ce}", exc_info=True)
            raise ConnectionError(f"Failed to connect during subscription: {ce}") from ce
        except TimeoutError as te:
            logger.warning(f"Subscription request timed out: {te}", exc_info=True)       
            raise TimeoutError(f"Subscription request timed out: {te}") from te
        except Exception as e:
            logger.critical(f"Unexpected error during subscription: {e}", exc_info=True)
            raise RuntimeError(f"An unexpected error occurred during subscription: {e}") from e


    def socket_functions(self):
        @self.socket.event
        def connect():
            print("Connected to the server")
            logger.info("Connected to the server")
            asyncio.create_task(self.subscribe_to_codes())
        
        @self.socket.event
        def disconnect():
            print("Server is disconnected")
            logger.warning("Server is disconnected")

        # touchline data
        @self.socket.on("1501-json-partial")
        def on_touchline(data):
            logger.debug("Received 1501 touchline data: %s", data)
            try:
                self.PublishToRedis("touchline-partial", data)
                logger.info("Published touchline data to Redis")
            except Exception as e:
                logger.error("Failed to publish touchline data to Redis: %s", str(e), exc_info=True)

        # market depth event
        @self.socket.on("1502-json-partial")
        def on_market_data(data):
            logger.debug("Received 1502 market data: %s", data)
            try:
                self.PublishToRedis("market-depth-partial", data)
                logger.info("Published market depth data to Redis")
            except Exception as e:
                logger.error("Failed to publish market depth data to Redis: %s", str(e), exc_info=True)
            
        # candle data event
        @self.socket.on("1505-json-partial")
        def on_candle_data(data):
            logger.debug("Received 1505 candle data: %s", data)
            try:
                self.PublishToRedis("candle-data-partial", data)
                logger.info("Published candle data to Redis")
            except Exception as e:
                logger.error("Failed to publish candle data to Redis: %s", str(e), exc_info=True)


        # market status event
        @self.socket.on("1507-json-partial")
        def on_market_status_data(data):
            logger.debug("Received 1507 market status data: %s", data)
            try:
                self.PublishToRedis("market-status-partial", data)
                logger.info("Published market status data to Redis")
            except Exception as e:
                logger.error("Failed to publish market status data to Redis: %s", str(e), exc_info=True)

        # open interest event
        @self.socket.on("1510-json-partial")
        def on_open_interest(data):
            logger.debug("Received 1510 open interest data: %s", data)
            try:
                self.PublishToRedis("open-interest-partial", data)
                logger.info("Published open interest data to Redis")
            except Exception as e:
                logger.error("Failed to publish open interest data to Redis: %s", str(e), exc_info=True)
        
        # ltp event
        @self.socket.on("1512-json-partial")
        def on_ltp_data(data):
            logger.debug("Received 1512 LTP data: %s", data)
            try:
                self.PublishToRedis("ltp-partial", data)
                logger.info("Published LTP data to Redis")
            except Exception as e:
                logger.error("Failed to publish LTP data to Redis: %s", str(e), exc_info=True)

        # instrument property change event
        @self.socket.on("1105-json-partial")
        def on_instrument_change_data(data):
            logger.debug("Received 1105 instrument change data: %s", data)
            try:
                self.PublishToRedis("instrument-change-partial", data)
                logger.info("Published instrument change data to Redis")
            except Exception as e:
                logger.error("Failed to publish instrument change data to Redis: %s", str(e), exc_info=True)


    def start(self):
        channels = [
            "touchline_channel", "market_data_channel", "candle_data_channel",
            "market_status_channel", "open_interest_channel", "ltp_data_channel",
            "instrument_change_channel"
        ]
        logger.info("Starting subscription to channels: %s", channels)
        try:
            self.start_sub(channels=channels)
            logger.info("Subscription to channels started successfully")
        except Exception as e:
            logger.critical("Failed to start subscription to channels: %s", str(e), exc_info=True)

            
            
        

# def main():

#     ws = WebSocket()
#     try:
#         ws.HostLookUp()
#         ws.login()
#     except Exception as e:
#         print(f"error: {e}")
#     asyncio.run(ws.subscribe_to_codes())

# if __name__ == "__main__":
#     main()


        
        




    

    
    
    

        




    
        