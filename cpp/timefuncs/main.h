#ifndef MAIN_H
#define MAIN_H


#include <iostream>
#include <ctime>
#include <vector>
#include <string>
#include <ctime>

#include "../InstrumentStruct/OptionStruct.h"


class OptionsTimeFunctions {
    private:
        int hour;
        int min;
        int sec;
    public:
        OptionsTimeFunctions(const int& hour,
                             const int& min,
                             const int& sec){
            this->hour = hour;
            this->min = min;
            this->sec = sec;
        }

        std::tm SetEndOfDay();
        std::vector<OptionData> TimeFilter(const std::vector<OptionData>& OptionDataVec,
                                           const std::tm& start_trade_time,
                                           const std::tm& end_trade_time);
};


#endif