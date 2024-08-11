#ifndef MAIN_H
#define MAIN_H


#include <iostream>
#include <ctime>
#include <vector>
#include <string>
#include <ctime>

#include "../InstrumentStruct/OptionStruct.h"


class OptionsTimeFunctions {
    public:
        OptionsTimeFunctions();

        std::tm SetEndOfDay(const int& hour,
                            const int& minute,
                            const int& second);
        std::vector<OptionData> TimeFilter(const std::vector<OptionData>& OptionDataVec,
                                           const std::tm& start_trade_time,
                                           const std::tm& end_trade_time);
};


#endif