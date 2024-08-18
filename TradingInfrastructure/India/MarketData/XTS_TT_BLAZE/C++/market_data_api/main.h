#ifndef MAIN_H
#define MAIN_H
#include <iostream>
#include <string>
#include <vector>
#include <curl/curl.h>
#include <fstream>
#include <filesystem>
#include <stdexcept>


class MarketDataAPIFunctions {
    private:
        std::string url;
        std::string secretKey;
        std::string apiKey;
        std::string authToken;
        std::string token;

    public:
        std::string PublishFormat;
        std::string BroadcastMode;
        std::string InstrumentType;

        MarketDataAPIFunctions() {}

        void ClientConfigResponse();
        std::tuple<int,std::vector<std::string>> IndexListResponse();
        std::vector<std::string> SeriesListResponse();
        std::vector<std::string> ExpiryList();
        std::vector<std::string> MasterDataResponse();
};


#endif
