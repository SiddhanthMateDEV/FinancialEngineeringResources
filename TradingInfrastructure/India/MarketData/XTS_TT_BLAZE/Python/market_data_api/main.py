import requests as rqs
import json 
from configparser import ConfigParser
import os

config_file_path = "/TT_BLAZE_XTS/market_data_api/data/xts_login.ini"
# os.makedirs(config_file_path, exist_ok = True)
config_write = ConfigParser()
config_read = ConfigParser()

class market_data_api_functions:
    def __init__(self, 
                 url = "https://ttblaze.iifl.com", 
                 secretKey = None,
                 apiKey = None
                 ):
        self.url = url
        self.secretKey = secretKey
        self.apiKey = apiKey
        self.auth_token = None
        self.token = None
        self.exchangeSegment = None
        self.xtsMessageCode = None
        self.publishFormat = None
        self.broadCastMode = None
        self.instrumentType = None
        self.index_list_cash_market = None
        self.series_futures_options_list = None
    
    def client_config_response(self):
        #client config
        config_read.read(str(config_file_path))
        self.token = config_read['AUTH']['token']
        CLIENT_CONFIG_URL = fr"{self.url}/apimarketdata/config/clientConfig"
        header_client_config = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        response_client_config = rqs.get(url = CLIENT_CONFIG_URL, 
                                         headers = header_client_config)
        if response_client_config.status_code == 200:
            client_config_response_data = response_client_config.json()
            data = client_config_response_data.get('result') 
            # this might cause an error if so check the key name and change it
            self.exchangeSegment = client_config_response_data.get('exchangeSegments') 
            config_write['exchangeSegments'] = {key: int(value) for key, value in data['exchangeSegments'].items()}
            self.xtsMessageCode = client_config_response_data.get('xtsMessageCode') 
            config_write['xtsMessageCode'] = {key: int(value) for key, value in data['xtsMessageCode'].items()}
            self.publishFormat = client_config_response_data.get('publishFormat') 
            config_write['publishFormat'] = {'format': ','.join(data['publishFormat'])}
            self.broadCastMode = client_config_response_data.get('broadCastMode')
            config_write['broadCastMode'] = {'format': ','.join(data['broadCastMode'])} 
            self.instrumentType = client_config_response_data.get('instrumentType') 
            config_write['instrumentType'] = {key: str(value) for key, value in data['xtsMessageCode'].items()}

        else:
            print("CLIENT CONFIG REQUEST FAILED")

    #get index list
    def index_list_response(self, exchange_segment = None):
        config_read.read(str(config_file_path))
        self.token = config_read['AUTH']['token']
        INDEX_LIST_URL = fr"{self.url}/apimarketdata/instruments/indexlist"
        header_index_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token) 
        }
        payload_index_list = {
            'exchangeSegment': int(exchange_segment)
        }
        response_index_list = rqs.get(url = INDEX_LIST_URL, 
                                      headers = header_index_list, 
                                      params = payload_index_list)
        if response_index_list.status_code == 200:
            index_list_data = response_index_list.json() 
            self.index_list_cash_market = index_list_data.get('result').get('indexList')
        else:
            print("BAD INDEX LIST REQUEST")

    #get series list
    def series_list(self, exchange_segment = None):
        config_read.read(str(config_file_path))
        self.token = config_read['AUTH']['token']
        assert exchange_segment is not None,"Exchange Segment Value cannot be set to None"
        SERIES_LIST_URL = fr"{self.url}/apimarketdata/instruments/instrument/series"
        header_series_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token) 
        }
        payload_series_list = {
            'exchangeSegment': int(exchange_segment)
        }
        response_series_list = rqs.get(url = SERIES_LIST_URL, 
                                       headers = header_series_list, 
                                       params = payload_series_list)

        if response_series_list.status_code == 200:
            series_list_data = response_series_list.json()
            self.series_futures_options_list = series_list_data.get('result')
        else:
            print("BAD REQUEST SERIES LIST")

    def options_expiry_list(self, series = None, symbol = None):
        config_read.read(str(config_file_path))
        self.token = config_read['AUTH']['token']
        if series and symbol is None:
            raise ValueError("Series & Symbol cannot be set to None")
        OPTIONS_EXPIRY_LIST_URL = "https://ttblaze.iifl.com/apimarketdata/instruments/instrument/expiryDate"  
        header_option_expiry_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        payload_option_expiry_list = {
            'exchangeSegment': 2,
            'series': str(series),
            'symbol': str(symbol)
        }
        response_series_list = rqs.get(url = OPTIONS_EXPIRY_LIST_URL, 
                                       headers = header_option_expiry_list, 
                                       params = payload_option_expiry_list)
        if response_series_list.status_code == 200:
            series_list_data = response_series_list.json()
            return series_list_data
        else:
            print("BAD REQUEST SERIES LIST")

    def master_data(self):
        MASTER_DATA_URL = "https://ttblaze.iifl.com/apimarketdata/instruments/master"
        header_master_list = {
            'Content-Type': 'application/json',
            'authorization': str(self.token)
        }
        payload_master_list = {
            'exchangeSegmentList': ["NSECM","NSECD","NSEFO"]
        }
        response_master_list = rqs.post(url = MASTER_DATA_URL, 
                                        headers = header_master_list, 
                                        json = payload_master_list)
        if response_master_list.status_code == 200:
            master_list_data = response_master_list.json()
            data = master_list_data['result']
            data_asset_classes = data.split('\n')
            asset_master_data = []
            data_header = [
                    "ExchangeSegment", "ExchangeInstrumentID", 
                    "InstrumentType", "Name", "Description",
                    "Series", "NameWithSeries", "InstrumentID",
                    "PriceBand.High", "PriceBand.Low",
                    "FreezeQty", "TickSize", "LotSize", 
                    "Multiplier", "UnderlyingInstrumentId",
                    "UnderlyingIndexName", "ContractExpiration", 
                    "StrikePrice", "OptionType",
                    "DisplayName", "PriceNumerator", 
                    "PriceDenominator", "DetailedDescription"
                    ]
            for asset in data_asset_classes:
                asset_values = asset.split('|')
                master_data_dict = dict(zip(data_header,asset_values))
                asset_master_data.append(master_data_dict)

            with open("TT_BLAZE_XTS/market_data_api/data/market_data_list.json","w") as json_file:
                json.dump(asset_master_data, json_file, indent = 4)
        else:
            print("MASTER DATA BAD REQUEST")