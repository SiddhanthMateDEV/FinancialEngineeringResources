import numpy as np 
import pandas as pd
import configparser
import os
import requests as rqs



"""
This class is made for the interactive api for XTS. It holds the following features:

- Before Sending a login request, the function HostLookUp() will send a post
request to get a token which will be used while sending a session
login request in the header.

- The session login function authenticates the user by sending a post request 
to the server using the secretKey and appKey provided by the broker when you 
registered for the API service(this part goes in the payload parameters), along
with this a token is parsed in the headers.

- 
"""



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
        response = rqs.post(url = HOST_LOOKUP_URL, 
                            json = payload_host_lookup)
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
        
        payload_login_interactive = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        
        login_header_interactive = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        
        SESSION_LOGIN_URL = fr"{self.url}/interactive/user/session"

        res_session_login = rqs.post(url = SESSION_LOGIN_URL, 
                                              headers = login_header_interactive, 
                                              json = payload_login_interactive)
        
        if res_session_login.status_code == 200:
            print("LOGIN INTO INTERACTIVE API SUCCESSFUL")
            print(res_session_login)
            login_response = res_session_login.json()
            self.token = login_response.get('result').get('token')
            print(self.token)
            self.config_read['AUTH'] = {'TOKEN': self.token}

            with open(str(self.config_file_path),'w') as configfile:
                self.config.write(configfile)
            return login_response
        else:
            print("LOGIN INTO INTERACTIVE API FAILED")

    # this one I am not sure how to deal with it so ignore this 
    def SessionLogout(self):
        self.config.read(str(self.config_file_path))
        self.auth_token = self.config['AUTH']['unique_key']
        
        payload_logout_interactive = {
            "secretKey": self.secretKey,
            "appKey": self.apiKey,
            "source": "WebAPI"
        }
        
        logout_header_interactive = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }
        
        SESSION_LOGOUT_URL = fr"{self.url}/interactive/user/session"

        res_session_logout = rqs.delete(url = SESSION_LOGOUT_URL, 
                                              headers = logout_header_interactive, 
                                              json = payload_logout_interactive)
        
        if res_session_logout.status_code == 200:
            print("LOGOUT FROM INTERACTIVE API SUCCESSFUL")
            print(res_session_logout)
        else:
            print("LOGOUT FROM INTERACTIVE API FAILED")
            print(res_session_logout)
    
    def Profile(self,
                ClientID : str):
        self.config.read(str(self.config_file_path))
        self.auth_token = self.config.get("AUTH").get("unique_key")
        
        payload_profile_interactive = {
            "ClientID" : str(ClientID)
        }
        
        headers_profile = {
            "Content-Type": "application/json",
            "authorization": self.auth_token
        }

        GET_PROFILE_URL = fr"{self.url}/interactive/user/profile?clientID=SYMP"

        res_profile = rqs.get(url = GET_PROFILE_URL,
                              headers = headers_profile,
                              json = payload_profile_interactive)
        
        if res_profile.status_code == 200:
            print(fr"The get request from Profile() was successful: {res_profile}")
        else:
            print(fr"The get request from Profile() was unsuccessful: {res_profile}")

