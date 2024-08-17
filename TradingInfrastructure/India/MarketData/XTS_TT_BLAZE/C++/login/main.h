#ifndef MAIN_H
#define MAIN_H
// #define URL "https://ttblaze.iifl.com"


#include <string>
#include <curl/curl.h>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <stdexcept>
/* 
Note: homebrew is used for mac since im developing on mac the json package i installed gets sent here

These are the instructions for mac users, considering you have already installed homebrew: 
brew uninstall nlohmann_json
brew untap nlohmann/json
brew install nlohmann-json
*/
#include </opt/homebrew/Cellar/jsoncpp/1.9.5/include/json/json.h>



class MarketDataCredentials {
    private:
        std::string url;
        std::string access_password;
        std::string version;
        std::string secret_key;
        std::string api_key;

        void writeConfig(const std::string& key, const std::string& value);
        std::string readConfig(const std::string& key);


    public:
        // this is my default constructor for my purpose i have added a dynamic one in the .cpp 
        const std::string HOST_LOOKUP_URL = "https://ttblaze.iifl.com:4000/HostLookUp";
        const std::string HOST_LOGIN_URL = "https://ttblaze.iifl.com/apimarketdata/auth/login";

        MarketDataCredentials(
            const std::string& url,
            const std::string& access_password,
            const std::string& version,
            const std::string& secret_key,
            const std::string& api_key
        );

        void hostLookUp();
        void loginMarketApi();
};

#endif