import redis
import json
from threading import Timer

class RedisHandler:
    def __init__(self,
                 redis_db = 0,
                 redis_port = 6379,
                 redis_host = "localhost",
                 redis_decode_response = True,
                 redis_interval = 60):
        
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_host= redis_host
        self.redis_decode_response = redis_decode_response
        self.redis_interval = redis_interval

        self.redis_client = redis.Redis(host = self.redis_host, 
                                        port = self.redis_port, 
                                        db = self.redis_db, 
                                        decode_responses = self.redis_decode_response)
        
    def publish_to_redis(self, channel, data):
        self.redis_client.publish(channel, json.dumps(data))

    def schedule_redis_cleanup(self):
        Timer(self.redis_interval,self.clean_up_redis).start()

    def clean_up_redis(self):
        self.redis_client.flushdb()
        self.schedule_redis_cleanup()
        
