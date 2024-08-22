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
        std::tuple<int,std::map<std::string,int>,std::map<std::string,std::map<std::string,int>>> Quotes();
        std::tuple<int,std::vector<std::string>> IndexListResponse();
        // std::vector<std::string> SeriesListResponse();
        // std::vector<std::string> ExpiryList();
        // std::vector<std::string> MasterDataResponse();
};


#endif
