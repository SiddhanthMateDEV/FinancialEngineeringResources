#ifndef MAIN_H
#define MAIN_H
#include <iostream>
#include <string>
#include <vector>

#include "../InstrumentStructures/IndexListCashMarket.h"
#include "../InstrumentStructures/SeriesFNOList.h"

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
        std::vector<CashListStruct> CashList;
        std::vector<fnoListStruct> SeriesFNOList;
        // std::string exchangeSegment;
        // int xtsMessageCode;

        MarketDataAPIFunctions(const std::string& url,
                               const std::string& secretKey,
                               const std::string& apiKey,
                               const std::string& authToken,
                               const std::string& token){
                                this->url = url;
                                this->secretKey = secretKey;
                                this->apiKey = apiKey;
                                this->authToken = authToken;
                                this->token = token;
        }

        void ClientConfigResponse();
        void IndexListResponse();
        void SeriesListResponse();
};


#endif
