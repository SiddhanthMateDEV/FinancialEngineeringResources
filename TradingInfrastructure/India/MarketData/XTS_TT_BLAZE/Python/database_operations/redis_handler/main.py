import redis
import json
from threading import Timer
import logging

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
        self.logger = self.logger.getLogger(__name__)

        try:
            self.redis_client = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                decode_responses=self.redis_decode_response
            )
            self.redis_client.ping()
            self.logger.info(f"Connected to Redis at {self.redis_host}:{self.redis_port} on DB {self.redis_db}")
        except redis.ConnectionError as e:
            self.logger.error(f"Redis connection error: {e}")
            self.redis_client = None
        except redis.RedisError as e:
            self.logger.error(f"Redis error: {e}")
            self.redis_client = None
        except Exception as e:
            self.logger.error(f"Unexpected error during Redis initialization: {e}")
            self.redis_client = None
        
    
    def PublishToRedis(self, channel, data):
        if self.redis_client:
            try:
                self.redis_client.publish(channel, json.dumps(data))
                self.logger.info(f"Published data to channel {channel}")
            except redis.RedisError as e:
                self.logger.error(f"Failed to publish to Redis channel {channel}: {e}")
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON serialization error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error while publishing to Redis: {e}")
        else:
            self.logger.error("Redis client is not initialized. Cannot publish data.")
    
    
    def ScheduleRedisCleanUp(self):
        if self.redis_client:
            try:
                Timer(self.redis_interval, self.CleanUpRedis).start()
                self.logger.info(f"Scheduled Redis cleanup every {self.redis_interval} seconds")
            except Exception as e:
                self.logger.error(f"Failed to schedule Redis cleanup: {e}")
        else:
            self.logger.error("Redis client is not initialized. Cannot schedule cleanup.")



    def CleanUpRedis(self):
        if self.redis_client:
            try:
                self.redis_client.flushdb()
                self.logger.info("Redis database flushed successfully")
                self.ScheduleRedisCleanUp()
            except redis.RedisError as e:
                self.logger.error(f"Failed to flush Redis database: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error during Redis cleanup: {e}")
        else:
            self.logger.error("Redis client is not initialized. Cannot clean up database.")
        
