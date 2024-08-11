from config.product_config.main import ProductConfig
from config.route_config.main import RouteConfig
from subscribe.main import SubscribedInstruments
from xts_message_codes.main import XtsMessageCodes
from login.main import MarketDataApiCredentials
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


class WebSocket(ProductConfig,
                RouteConfig,
                SubscribedInstruments,
                XtsMessageCodes,
                MarketDataApiCredentials,
                MongoWriter,
                RedisHandler):
    def __init__(self,
                 root_url = "https://ttblaze.iifl.com",
                 mongo_uri = "mongodb://localhost:27017",
                 token = None,
                 db_name = "XTS_WEBSOC_DATA",
                 coll_name = None,
                 publish_format = "JSON",
                 broadcast_mode = "Full",
                 socket_path = "/apimarketdata/socket.io",
                 redis_port = 6379,
                 redis_db = 0,
                 redis_host = "localhost",
                 redis_decode_response = True,
                 redis_interval = 60,
                 ):
        
        RedisHandler.__init__(redis_db = redis_db,
                            redis_port = redis_port,
                            redis_host = redis_host,
                            redis_decode_response = redis_decode_response,
                            redis_interval = redis_interval)
        
        MongoWriter.__init__(mongo_uri = mongo_uri,
                            db_name = db_name,
                            redis_host = redis_host,
                            redis_port = redis_port,)
        

        if not all([root_url,token,db_name,coll_name,
                    publish_format,broadcast_mode,]):
            raise ValueError("Fields required for initiating a websocket are empty or None")

        self.root_url = root_url
        self.token = token
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[str(db_name)]
        self.mongo_coll = self.mongo_db[str(coll_name)]
        self.publish_format = publish_format
        self.broadcast_mode = broadcast_mode
        self.socket_path = socket_path
        self.socket = socketio.Client()
        self.event_loop = asyncio.get_event_loop()

        """
        When the class is initialised this will be called once to get the 
        unique_key to be used for the login request which is right after that
        """
        self.host_look_up()
        self.login_market_api()

        super().__init__()

        if not all([self._routes, self.products]):
            raise ValueError("Empty Config fields for routes and products")


    async def _request(self, 
                       route = None, 
                       method_req = None, 
                       parameters = None, 
                       pool = None):
        
        params = parameters or {}

        try:
            uri = self._routes[str(route)].format(**params)
            url = urljoin(self.root_url, uri)
        except KeyError as e:
            raise ValueError(f"Key error for self._routes: {route}")
        
        headers = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method = method_req,
                    url = url,
                    json = params if method_req in ["POST","PUT"] else None,
                    params = params if method_req in ["GET","DELETE"] else None,
                    headers = headers,
                    ssl = True
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except rqs.exceptions.RequestException as e:
                raise ValueError(fr"HTTPS Error occured at _request function, Error Code: {e.response.status_code}")
            except json.JSONDecodeError as e:
                raise ValueError("Failed to load JSON response at _request function")
            except Exception as e:
                raise ValueError("Error occured in _request function") 
        
    
    async def _post(self, route_param = None, 
                        params = None):
        return await self._request(route = route_param, 
                                   method_req = "POST", 
                                   parameters = params, 
                                   pool = None)
    

    async def send_subscription(self, instruments = None, 
                                xts_message_codes = None):
        try:
            responses = []
            for instrument, code in product(instruments, xts_message_codes):
                params_code = {
                    'instruments': instrument,
                    'xtsMessageCode': code,
                }
                response = await self._post(route_param = 'market.instruments.subscription', 
                                            params = params_code)
                responses.append(response)
            return responses
        except Exception as e:
            raise ValueError("Error in sending subscription") from e
        
    async def subscribe_to_codes(self):
        response = await self.send_subscription(instruments = self.subscribe_payload, 
                                                xts_message_codes = self.xts_message_codes)
        return response


    def socket_functions(self):
        @self.socket.event
        def connect():
            print("Connected to the server")
            self.event_loop.run_until_complete(self.subscribe_to_codes())
        
        @self.socket.event
        def disconnect():
            print("Server is disconnected")

        # touchline data
        @self.socket.on("1501-json-partial")
        def on_touchline(data):
            print("1501 touchline data: ",data)
            self.publish_to_redis("touchline-partial", data)

        # market depth event
        @self.socket.on("1502-json-partial")
        def on_market_data(data):
            print("1502 market data: ",data)
            self.publish_to_redis("market-depth-partial", data)
        
        # candle data event
        @self.socket.on("1505-json-partial")
        def on_candle_data(data):  
            print("1505 candle data: ",data)
            self.publish_to_redis("candle-data-partial", data)

        # market status event
        @self.socket.on("1507-json-partial")
        def on_market_status_data(data):
            print("1507 market status data: ",data)
            self.publish_to_redis("market-status-partial", data)

        # open interest event
        @self.socket.on("1510-json-partial")
        def on_open_interest(data):
            print("1510 open interest data: ",data)
            self.publish_to_redis("open-interest-partial", data)
        
        # ltp event
        @self.socket.on("1512-json-partial")
        def on_ltp_data(data):
            print("1512 LTP data: ",data)
            self.publish_to_redis("ltp-partial", data)

        # instrument property change event
        @self.socket.on("1105-json-partial")
        def on_instrument_change_data(data):
            print("1105 instrument change data: ",data)
            self.publish_to_redis("instrument-change-partial", data)


    def schedule_redis_cleanup(self):
        Timer(self.redis_interval,self.clean_up_redis).start()


    def clean_up_redis(self):
        self.redis_client.flushdb()
        self.schedule_redis_cleanup()


    def start(self):
        channels = [
            "touchline_channel", "market_data_channel", "candle_data_channel",
            "market_status_channel", "open_interest_channel", "ltp_data_channel",
            "instrument_change_channel"
        ]
        self.start_sub(channels = channels)

        
        
        
        
        
        
        




    

    
    
    

        




    
        