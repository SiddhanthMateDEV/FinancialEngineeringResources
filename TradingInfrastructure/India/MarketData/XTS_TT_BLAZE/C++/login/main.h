#ifndef MAIN_H
#define MAIN_H


#include <string>
#include <curl/curl.h>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <stdexcept>
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
        MarketDataCredentials(
            const std::string& url = "https://ttblaze.iifl.com",
            const std::string& access_password = "2021HostLookUpAccess",
            const std::string& version = "interactive_1.0.1",
            const std::string& secret_key = "",
            const std::string& api_key = ""
        );

        void hostLookUp();
        void loginMarketApi();
};

#endif