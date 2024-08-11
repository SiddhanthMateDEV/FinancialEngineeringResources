#ifndef MAIN_H
#define MAIN_H

#include <iostream>
#include "../InstrumentStruct/OptionStruct.h"
#include <vector>
#include <string>
#include <ctime>

class Straddle {
    private:
        std::vector<OptionData> OptionDataVec;
        std::tm expiry;
        std::tm start_trade_time;
        std::tm end_trade_time;
        double strike_price;

    public:
        Straddle(const std::vector<OptionData>& OptionDataVec,
                 const std::tm& expiry, 
                 const std::tm& start_trade_time,
                 const std::tm& end_trade_time,
                 const double& strike_price){
                    this->OptionDataVec = OptionDataVec;
                    this->expiry = expiry;
                    this->start_trade_time = start_trade_time;
                    this->end_trade_time = end_trade_time;
                    this->strike_price = strike_price;
                }
                
        std::vector<OptionData> CallDataVec();
        std::vector<OptionData> PutDataVec();
};

#endif 