from pymongo import MongoClient
import redis
import json
import concurrent.futures

class MongoWriter:
    def __init__(self,
                 mongo_uri = "monogdb://localhost:27017",
                 db_name = None,
                 coll_name = None,
                 redis_host = "localhost",
                 redis_port = int(6379),
                 ):
        self.mongo_uri = mongo_uri
        self.mongo_client = None
        self.mongo_db = None
        self.mongo_coll = None

        self.db_name = db_name
        self.coll_name = None

        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)


    def connect_to_mongo_db(self):
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.mongo_client.server_info()
            self.mongo_db = self.mongo_client[str(self.db_name)]
            self.mongo_coll = self.mongo_db[str(self.coll_name)]
        except Exception as e:
            print(fr"Error occured inside 'connect_to_mongo_db', Error: {e}")

    def write_data(self,data):
        instrument = data.get('instrumentID')
        exchangeSegment = data.get('exchangeSegment')

        collection_name = f"{instrument}_{exchangeSegment}"
        self.coll_name = collection_name
        
        try:
            self.connect_to_mongo_db()
        except Exception as e:
            raise RuntimeError(fr"Error in runtime while calling connect_to_mongo_db() in write_data()")
        
        self.mongo_coll.insert_one(data)
        
    
    def subscribe_and_write(self, channel):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                self.write_data(data)

    def start_sub(self, channels):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.subscribe_and_write, channel) for channel in channels]

    