import sys
import os
import time
from itertools import product
import datetime

# to fix inehritance errors
import aiohttp
from pymongo.errors import *
from socketio.exceptions import *
from redis.exceptions import *


import socket
import asyncio
import ssl
import os
import sys

from json import JSONDecodeError
from requests.exceptions import *
from urllib3.exceptions import *
from concurrent.futures import TimeoutError, CancelledError


# Just pointing the path to parent dir for imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

sys.path.insert(0,parent_dir)

# Inherited Classes
from config.product_config.main import ProductConfig
from config.route_config.main import RouteConfig
from subscribe.main import SubscribedInstruments
from config.xts_message_codes.main import XtsMessageCodes
from auth.main import MarketDataApiCredentials
from dbProcess.main import LowLatencyDataBase


import asyncio
from urllib.parse import urljoin
import json 
import socketio
from itertools import product
import aiohttp

from logger.main import LoggerBase
import socketio
import threading


class WebSocket(
                MarketDataApiCredentials,
                LowLatencyDataBase,
                ProductConfig,
                RouteConfig,
                SubscribedInstruments,
                XtsMessageCodes,
                LoggerBase
                ):

    def __init__(self,
                websoc_class_attr = None,
                database_class_attr = None,
                logger_class_attr = None,
                credentials_class_attr = None):

        LoggerBase.__init__(self,**logger_class_attr)

        if websoc_class_attr:
            for var, value in websoc_class_attr.items():
                setattr(self, var, value)

        self.database_attr = database_class_attr

        LowLatencyDataBase.__init__(self,**database_class_attr)
        MarketDataApiCredentials.__init__(self,**credentials_class_attr)
        ProductConfig.__init__(self)
        RouteConfig.__init__(self)  
        SubscribedInstruments.__init__(self)
        XtsMessageCodes.__init__(self)

 
    async def _request(self, 
                       route=None, 
                       method_req=None, 
                       parameters=None, 
                       pool=None):
        
        await asyncio.sleep(0.1)  
        params = parameters or {}
        try:
            uri = self._routes[str(route)].format(**params)
            url = urljoin(self.root_url, uri)
            await self.info(f"Accessing URL: {url}")
        except KeyError as e:
            await self.error(f"Key error for self._routes: {route}. Details: {str(e)}")
            raise ValueError(f"Key error for self._routes: {route}. Ensure the route is correctly defined and the parameters match the expected format. Details: {str(e)}") from e
        except Exception as e:
            await self.error(f"Unexpected error when constructing URL: {str(e)}")
            raise ValueError(f"Unexpected error when constructing URL: {str(e)}")
        
        header = {
            'Content-Type': 'application/json',
            'authorization': str(self.token),
        }

        #Note: Refer this link: https://docs.aiohttp.org/en/stable/client_quickstart.html 
        async with aiohttp.ClientSession() as session:
            try:
                if url.startswith("ws://") or url.startswith("wss://"):
                    # Handle WebSocket connection
                    async with session.ws_connect(url, headers=header, ssl=False) as ws:
                        await self.info(f"WebSocket connection established: {url}")                    
                        await ws.send_str(json.dumps(params))

                        time.sleep(0.1)
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                response_data = json.loads(msg.data)
                                if "error" in response_data:
                                    await self.error(f"Subscription failed with error: {response_data['error']}")
                                    raise ValueError(f"Subscription failed with error: {response_data['error']}")
                                else:
                                    await self.info("Subscription successful.")
                                    return response_data
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                raise ValueError(f"WebSocket connection closed with error: {ws.exception()}")                                    

                if url.startswith(("http://", "https://")):
                    try:
                        async with session.request(
                            method=method_req,
                            url=url,
                            headers=header,
                            json=params if method_req in ["POST", "PUT"] else None,
                            params=params if method_req in ["GET", "DELETE"] else None,
                            ssl=False
                        ) as response:
                            
                            await asyncio.sleep(0.1)
                            
                            response_json = await response.json()

                            if response.status == 200:
                                return response_json

                            if response.status != 200:
                                await self.error(fr"Error in response from server | Error Code: {response.status} | Response: {response}")
                                return 
                    except Exception as e:
                        await self.error(f"An unexpected error occurred during the request to {url}. Details: {str(e)} in _requests function | Response: {response}")
                        raise ValueError(f"An unexpected error occurred during the request to {url}. Details: {str(e)} in _requests function | Response: {response}")

            except Exception as e:
                await self.critical(f"Unexpected error occurred during while creating a session for Http/Https Requests to {url}. Details: {str(e)} in _requests function | Response: {response}")
                raise ValueError(f"Unexpected error occurred during while creating a session for Http/Https Requests to {url}. Details: {str(e)} in _requests function | Response: {response}")

    async def _post(self, 
                    route_param=None, 
                    params=None):
        try:
            response = await self._request(route=route_param,
                                        method_req="POST",
                                        parameters=params,
                                        pool=None)
            return response            
        except Exception as e:
            await self.error(fr"Error in _post function, Error due to: {e}")
    
    async def send_subscription(self,
                                instruments=None, 
                                xts_message_codes=None):
        
        
        instruments = self.subscribe_payload
        xts_message_codes = self.xts_message_codes
        try:
            if instruments is None or xts_message_codes is None:
                await self.error("Instruments and xts_message_codes cannot be None")
                raise ValueError("Instruments and xts_message_codes cannot be None")
            
            responses = []
            tasks = []
            for instrument, code in product(instruments, xts_message_codes):
                params_code = {
                    'instruments': [{
                        "exchangeSegment": instrument["exchangeSegment"],
                        "exchangeInstrumentID": instrument["exchangeInstrumentID"]
                        }],
                    'xtsMessageCode': code,
                }
                tasks.append(self._post(route_param='market.instruments.subscription', 
                                                params=params_code))
                
            try:
                responses = await asyncio.gather(*tasks)
                await self.info(f"Subscribing to instrument | Capturing Responses In send_subscription function")
            except Exception as e:
                await self.critical(f"Unexpected error occurred while subscribing to instrument in send_subscription function")
                raise RuntimeError(f"An unexpected error occurred while subscribing to instrument in send_subscription function")
            
            time.sleep(0.1)
            await self.info("All subscriptions processed successfully.")
            return responses
        except Exception as e:
            await self.critical("Critical error in send_subscription method")
            raise ValueError("Error in sending subscription") 
        

    async def subscribe_to_codes(self):
        try:
            if not self.subscribe_payload or not self.xts_message_codes:
                await self.error("Subscription payload or message codes cannot be empty | Error coming from subscribe_to_codes function")
                raise ValueError("Subscription payload or message codes cannot be empty | Error coming from subscribe_to_codes function")
            
            await self.debug(f"Starting subscription with payload: {self.subscribe_payload} and message codes: {self.xts_message_codes}")
            response = await self.send_subscription(instruments=self.subscribe_payload, 
                                                    xts_message_codes=self.xts_message_codes)        
            return response
        except Exception as e:
            await self.critical(f"Unexpected error occured while running subscribe_to_codes: {e}")
            raise RuntimeError(f"An unexpected error occurred occured while running subscribe_to_codes: {e}") 
    

    def start(self):
        self.socket = socketio.Client(reconnection = True,
                                    reconnection_attempts = 10,
                                    reconnection_delay = 1)
        base_url = f"https://ttblaze.iifl.com/?token={self.token}&userID={self.userID}&publishFormat={self.publish_format}&broadcastMode={self.broadcast_mode}"
        
        self.socket.connect(
                            base_url, 
                            headers={}, 
                            socketio_path="/apimarketdata/socket.io", 
                            transports=['websocket'],
                            namespaces=None,
                            )
        
        @self.socket.event
        def connect():
            print("WebSocket connected")

        @self.socket.event
        def connect_error(data):
            print("The connection failed!")

        @self.socket.event
        def disconnect():
            print("Disconnected from WebSocket")

        @self.socket.on('1501-json-full')
        def on_1501_json_full(data):
            print(f"1501_data:{data}")
            key = "1501-json-full"
            self.data_deques[key].append(data)

        @self.socket.on('1502-json-full')
        def on_1502_json_full(data):
            print(f"1502_data:{data}")
            key = "1502-json-full"
            self.data_deques[key].append(data)

        @self.socket.on('1505-json-full')
        def on_1505_json_full(data):
            print(f"1505_data:{data}")
            key = "1505-json-full"
            self.data_deques[key].append(data)
            print(f"New Data Added To {key}")

        @self.socket.on('1510-json-full')
        def on_1510_json_full(data):
            print(f"1510_data:{data}")
            key = "1510-json-full"
            self.data_deques[key].append(data)
            print(f"New Data Added To {key}")

        @self.socket.on('1512-json-full')
        def on_1512_json_full(data):
            print(f"1512_data:{data}")
            key = "1512-json-full"
            self.data_deques[key].append(data)
            print(f"New Data Added To {key}")
            
        @self.socket.on('1105-json-full')
        def on_1105_json_full(data):
            print(f"1105_data:{data}")
            key = "1105-json-full"
            self.data_deques[key].append(data)
            print(f"New Data Added To {key}")

        self.socket.wait()


    def check_time_and_stop(self):
        start_time = datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
        end_time = datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)

        while True:
            now = datetime.datetime.now()

            if not (start_time <= now <= end_time):
                self.logout()
                print("Logged Out From The check_time_and_stop() function")
                self.socket.close()
                break
            time.sleep(60)
        

    async def run(self):
        try:       
            loop = asyncio.get_event_loop()
            await self.info("Starting an event loop From run function, Initialising All Functions Now:")
            await self.info(fr"Loop Started: {id(loop)}")
            time.sleep(0.1)

            try:            
                await self.info("Initiating Task To start HostLookUp and login function")
                time.sleep(0.1)
                self.auth_token = await self.HostLookUp()
                await self.info("Initiating HostLookUp")
                time.sleep(0.1)
                
                if self.auth_token is None:
                    await self.error(fr"Error In Running HostLookUp function, Auth Token is None")
                    raise ValueError("Auth Token is None")
                
                await self.info("Successful HostLookUp")
                self.token = await self.login()
                await self.info("Successful Login")
                time.sleep(0.1)
                
                if self.token is None:
                    await self.error(fr"Error In Running login function, Token is None")
                    raise ValueError("Token is None")
            except Exception as e:
                await self.error(fr"Error In Running HostLookUp and login function: {e}")
                raise ValueError(fr"Error In Running HostLookUp and login function: {e}")


            try:
                await self.info("Initiating Subscription Of Codes")
                await self.subscribe_to_codes()
                time.sleep(0.1)
                await self.info("Subscribed To Codes")
            except Exception as e:
                await self.error(fr"Error In Running subscribe_to_codes: {e}")
                raise ValueError(fr"Error In Running subscribe_to_codes: {e}")

            try:
                await self.info(fr"Running thread for create_deque_and_handles function")
                thread_deque = threading.Thread(target = self.create_deque_and_handles)
                await self.info(fr"Started thread for create_deque_and_handles function")
                thread_deque.start()
            except Exception as e:
                await self.error(fr"Error In Running create_deque_and_handles: {e}")
                raise ValueError(fr"Error In Running create_deque_and_handles: {e}")

            try:
                await self.info(fr"Running thread for start function")
                thread_start_function = threading.Thread(target = self.start)
                await self.info(fr"Started thread for start function")
                thread_start_function.start()
            except Exception as e:
                await self.error(fr"Error In Running start function: {e}")
                raise ValueError(fr"Error In Running start function: {e}")                

            try:
                await self.info(fr"Running thread for check_time_and_stop function")
                thread_check_time = threading.Thread(target = self.check_time_and_stop)
                await self.info(fr"Started thread for check_time_and_stop function")
                thread_check_time.start()
            except Exception as e:
                await self.warning(fr"Error In Running thread for check_time_and_stop function: {e}")
                raise ValueError(fr"Error In Running check_time_and_stop function: {e}")                
            
        except Exception as e:
            await self.error(f"Error in run: {e}")
