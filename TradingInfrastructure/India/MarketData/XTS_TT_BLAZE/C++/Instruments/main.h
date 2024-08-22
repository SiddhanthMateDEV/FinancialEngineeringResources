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



class MarketDataAPIFunctions {
    public: 
        MarketDataAPIFunctions() {};

        void ClientConfigResponse();
        void Quotes();
        std::tuple<int,std::vector<std::string>> IndexListResponse();
        // std::vector<std::string> SeriesListResponse();
        // std::vector<std::string> ExpiryList();
        // std::vector<std::string> MasterDataResponse();
};


#endif
