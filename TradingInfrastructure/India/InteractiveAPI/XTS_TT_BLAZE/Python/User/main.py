import numpy as np 
import pandas as pd
import configparser
import os
import requests as rqs

class User:
    def __init__(self,
                 url = "https://ttblaze.iifl.com", 
                 access_password = "2021HostLookUpAccess",
                 version = "interactive_1.0.1",
                 secretKey = None,
                 apiKey = None):
        
        self.url = url
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.version = version
        self.access_password = access_password
        self.config_file_path = "./login.ini"

        self.cofig = configparser.ConfigParser()

    def HostLookUp(self):
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
                self.config['AUTH'] = {'unique_key': unique_key}
                with open(str(self.config_file_path),'w') as configfile:
                    self.config.write(configfile)
        else:
            print(fr"HOST LOOKUP REQUEST HAS FAILED")

    def SessionLogin(self):
        self.config.read(str(self.config_file_path))
        self.auth_token = self.config['AUTH']['unique_key']
        
        payload_market_data = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        
        login_header_market_data = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        
        # LOGIN_URL_MARKET_API = fr"{self.url}/apimarketdata/auth/login"
        LOGIN_URL_MARKET_API = fr"{self.url}/interactive/user/session"

        response_market_data_login = rqs.post(url = LOGIN_URL_MARKET_API, 
                                              headers = login_header_market_data, 
                                              json = payload_market_data)
        
        if response_market_data_login.status_code == 200:
            print("LOGIN INTO INTERACTIVE API SUCCESSFUL")
            print(response_market_data_login)
            login_response = response_market_data_login.json()
            self.token = login_response.get('result').get('token')
            print(self.token)
            self.config_read['AUTH'] = {'TOKEN': self.token}

            with open(str(self.config_file_path),'w') as configfile:
                self.config.write(configfile)
            return login_response
        else:
            print("LOGIN INTO INTERACTIVE API FAILED")

    def SessionLogout(self):
        self.config.read(str(self.config_file_path))
        self.auth_token = self.config['AUTH']['unique_key']
        
        payload_market_data = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        
        login_header_market_data = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        
        # LOGIN_URL_MARKET_API = fr"{self.url}/apimarketdata/auth/login"
        LOGIN_URL_MARKET_API = fr"{self.url}/interactive/user/session"

        response_market_data_login = rqs.delete(url = LOGIN_URL_MARKET_API, 
                                              headers = login_header_market_data, 
                                              json = payload_market_data)
        
        if response_market_data_login.status_code == 200:
            print("LOGOUT FROM INTERACTIVE API SUCCESSFUL")
        else:
            print("LOGOUT FROM INTERACTIVE API FAILED")

    