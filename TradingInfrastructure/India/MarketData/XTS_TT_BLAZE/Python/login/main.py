import requests as rqs
from configparser import ConfigParser
import os

'''
These are some parameters to pass to use market_data_api class: 
url: The base URL for the API. 
access_password: Password for accessing the host lookup. 
version: Version of the host lookup API. 
secretKey: Secret key for market API authentication. 
apiKey: API key for market API authentication. 
'''
class MarketDataApiCredentials:
    def __init__(self, 
                 url = "https://ttblaze.iifl.com", 
                 access_password = "2021HostLookUpAccess",
                 version = "interactive_1.0.1",
                 secretKey = None,
                 apiKey = None,
                 config_file = "/TT_BLAZE_XTS/market_data_api/data/xts_login.ini"
                 ):
        
        self.url = url
        self.access_password = access_password
        self.version = version
        self.secretKey = secretKey
        self.apiKey = apiKey
        self.auth_token = None
        self.token = None

        self.config_file_path = config_file
        os.makedirs(config_file, exist_ok = True)

        self.config_write = ConfigParser()
        self.config_read = ConfigParser()


    def host_look_up(self):
        HOST_LOOKUP_URL = fr"{self.url}:4000/HostLookUp"
        payload_host_lookup = {
            "accesspassword": self.access_password,
            "version": self.version
        }
        response = rqs.post(url = HOST_LOOKUP_URL, json = payload_host_lookup)
        if response.status_code == 200:
            unique_key = response.json().get('result').get('uniqueKey') 
            if unique_key is None:
                raise ValueError("uniqueKey genereated in empty")
            else:
                self.auth_token = unique_key
                self.config_write['AUTH'] = {'unique_key': unique_key}
                with open("TT_BLAZE_XTS/market_data_api/data/xts_login.ini",'w') as configfile:
                    self.config_write.write(configfile)
        else:
            print(fr"HOST LOOKUP REQUEST HAS FAILED")


    def login_market_api(self):
        self.config_read.read(str(self.config_file_path))
        self.auth_token = self.config_read['AUTH']['unique_key'] or self.host_look_up()
        
        payload_market_data = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        
        login_header_market_data = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        
        LOGIN_URL_MARKET_API = fr"{self.url}/apimarketdata/auth/login"
        response_market_data_login = rqs.post(url = LOGIN_URL_MARKET_API, 
                                              headers = login_header_market_data, 
                                              json = payload_market_data)
        
        if response_market_data_login.status_code == 200:
            login_response = response_market_data_login.json()
            self.token = login_response.get('result').get('token')
            self.config_write['AUTH'].update({'token': self.token})
            with open(str(self.config_file_path),'w') as configfile:
                self.config_write.write(configfile)
            return login_response
        else:
            print("LOGIN INTO MARKET DATA API FAILED")

    
    