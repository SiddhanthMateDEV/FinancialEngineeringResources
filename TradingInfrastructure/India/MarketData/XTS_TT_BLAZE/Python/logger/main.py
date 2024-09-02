import logging
import asyncio
from datetime import datetime
import aiofiles


class LoggerBase:
    def __init__(self, 
                 logger=None, 
                 log_file = None):
        
        self.log_file = log_file
        self.logger = logger


        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.setLevel(logging.INFO)
            
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(stream_handler)
            
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(file_handler)
        else:
            self.logger = logger
        
        self.logger.info(f"{self.__class__.__name__} logger initialized")
    
    async def async_log(self, level, message):
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message)

        if self.log_file:
            log_message = f"{datetime.now()} - {self.__class__.__name__} - {level.upper()} - {message}\n"
            async with aiofiles.open(self.log_file, mode='a') as f:
                await f.write(log_message)

    async def info(self, message,*args,**kwargs):
        await self.async_log('info', message)

    async def warning(self, message,*args,**kwargs):
        await self.async_log('warning', message)

    async def error(self, message,*args,**kwargs):
        await self.async_log('error', message)

    async def debug(self, message,*args,**kwargs):
        await self.async_log('debug', message)

    async def critical(self, message,*args,**kwargs):
        await self.async_log('critical', message)
