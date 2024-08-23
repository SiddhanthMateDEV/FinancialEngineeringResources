import requests as rqs
import configparser

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
                 ):
        
        self.url = url
        self.access_password = access_password
        self.version = version
        self.secretKey = secretKey
        self.apiKey = apiKey
        self.auth_token = None
        self.token = None

        self.config_file_path = './login.ini'
        self.config = configparser.ConfigParser()

    def HostLookUp(self):
        HOST_LOOKUP_URL = fr"{self.url}:4000/HostLookUp"
        self.config.read(self.config_file_path)
        payload_host_lookup = {
            "accesspassword": self.access_password,
            "version": self.version
        }

        try:
            response = rqs.post(url=HOST_LOOKUP_URL, json=payload_host_lookup)
            response.raise_for_status()  
        except rqs.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred during host lookup: {http_err}")
            return None
        except rqs.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred during host lookup: {conn_err}")
            return None
        except rqs.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred during host lookup: {timeout_err}")
            return None
        except rqs.exceptions.RequestException as req_err:
            print(f"An error occurred during host lookup: {req_err}")
            return None

        try:
            response_data = response.json()
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
            return None

        unique_key = response_data.get('result', {}).get('uniqueKey')
        if unique_key is None:
            raise ValueError("uniqueKey generated is empty")

        self.auth_token = unique_key
        self.config["AUTH"]["unique_key"] = unique_key

        try:
            with open(self.config_file_path, 'w') as configfile:
                self.config.write(configfile)
            print("HostLookUp was successful")
        except IOError as io_err:
            print(f"Error writing to config file: {io_err}")
            return None

        return self.auth_token  


    def login(self):
        try:
            self.config.read(str(self.config_file_path))
            self.auth_token = self.config['AUTH'].get('unique_key')
            self.apiKey = self.config['AUTH'].get('api_key')
            self.secretKey = self.config['AUTH'].get('secret_key')

            if not all([self.auth_token, self.apiKey, self.secretKey]):
                raise ValueError("Missing authentication credentials in the configuration file.")

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

            try:
                response_market_data_login = rqs.post(
                    url=LOGIN_URL_MARKET_API, 
                    headers=login_header_market_data, 
                    json=payload_market_data
                )
                response_market_data_login.raise_for_status()
            except rqs.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred during market data login: {http_err}")
                return None
            except rqs.exceptions.ConnectionError as conn_err:
                print(f"Connection error occurred during market data login: {conn_err}")
                return None
            except rqs.exceptions.Timeout as timeout_err:
                print(f"Timeout error occurred during market data login: {timeout_err}")
                return None
            except rqs.exceptions.RequestException as req_err:
                print(f"An error occurred during market data login: {req_err}")
                return None

            try:
                login_response = response_market_data_login.json()
            except ValueError as json_err:
                print(f"JSON decode error: {json_err}")
                return None

            self.token = login_response.get('result', {}).get('token')
            if self.token is None:
                raise ValueError("Token received is empty")

            self.config['AUTH']['token'] = self.token

            try:
                with open(str(self.config_file_path), 'w') as configfile:
                    self.config.write(configfile)
                print("Login was successful")
            except IOError as io_err:
                print(f"Error writing to config file: {io_err}")
                return None

            return self.token

        except KeyError as key_err:
            print(f"Key error: Missing {key_err} in the configuration file.")
            return None
        except ValueError as val_err:
            print(f"Value error: {val_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None