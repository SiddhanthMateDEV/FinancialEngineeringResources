from pymongo import MongoClient
import redis
import json
import concurrent.futures
import logging


class MongoWriter:
    def __init__(self,
                 mongo_uri="mongodb://localhost:27017",
                 db_name=None,
                 coll_name=None,
                 redis_host="localhost",
                 redis_port=int(6379),
                 ):
        self.mongo_uri = mongo_uri
        self.mongo_client = None
        self.mongo_db = None
        self.mongo_coll = None

        self.db_name = db_name
        self.coll_name = coll_name
        self.logger = self.logger.getLogger(__name__)

        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

    def ConnectMongoDB(self):
        try:
            self.logger.debug("Attempting to connect to MongoDB.")
            self.mongo_client = MongoClient(self.mongo_uri)
            self.mongo_client.server_info() 
            self.mongo_db = self.mongo_client[str(self.db_name)]
            self.mongo_coll = self.mongo_db[str(self.coll_name)]
            self.logger.info(f"Connected to MongoDB database: {self.db_name}, collection: {self.coll_name}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB. URI: {self.mongo_uri}, Error: {e}")
            raise RuntimeError("MongoDB connection failed") from e

    def WriteData(self, data):
        try:
            instrument = data.get('instrumentID')
            exchangeSegment = data.get('exchangeSegment')

            if not instrument or not exchangeSegment:
                raise ValueError("Data does not contain 'instrumentID' or 'exchangeSegment'")

            collection_name = f"{instrument}_{exchangeSegment}"
            self.coll_name = collection_name

            self.logger.debug(f"Collection name set to: {self.coll_name}. Attempting to write data.")
            self.ConnectMongoDB()

            self.mongo_coll.insert_one(data)
            self.logger.info(f"Data written to MongoDB collection: {self.coll_name}")
        except Exception as e:
            self.logger.error(f"Error writing data to MongoDB. Data: {data}, Error: {e}")
            raise

    def SubscribeAndWrite(self, channel):
        try:
            self.logger.debug(f"Subscribing to Redis channel: {channel}")
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(channel)

            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        self.logger.debug(f"Received message from channel {channel}: {data}")
                        self.WriteData(data)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to decode JSON message from channel {channel}. Message: {message['data']}, Error: {e}")
                    except Exception as e:
                        self.logger.error(f"Failed to process message from channel {channel}. Message: {message['data']}, Error: {e}")
        except Exception as e:
            self.logger.error(f"Error subscribing to Redis channel {channel}. Error: {e}")
            raise

    def StartSub(self, channels):
        try:
            self.logger.debug(f"Starting subscription for channels: {channels}")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.SubscribeAndWrite, channel) for channel in channels]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"Error in thread executing SubscribeAndWrite. Error: {e}")
        except Exception as e:
            self.logger.error(f"Error starting subscriptions for channels {channels}. Error: {e}")
            raise