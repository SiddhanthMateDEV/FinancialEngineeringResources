#ifndef MAIN_H
#define MAIN_H
#include <iostream>
#include <string>
#include <vector>

#include <curl/curl.h>

#include <fstream>
#include <filesystem>
#include <stdexcept>
#include <map>
#include <iomanip>
#include <ctime>

#include </opt/homebrew/Cellar/jsoncpp/1.9.5/include/json/json.h>


class MarketDataAPIFunctions {
    public: 
        MarketDataAPIFunctions() {};

        void ClientConfigResponse();
        void Quotes();
        std::tuple<std::vector<Bid>,std::vector<Ask>> Quotes();
        void Subscribe();
        std::tuple<int,std::vector<std::string>> IndexListResponse();
        // std::vector<std::string> SeriesListResponse();
        // std::vector<std::string> ExpiryList();
        // std::vector<std::string> MasterDataResponse();
};


#endif
