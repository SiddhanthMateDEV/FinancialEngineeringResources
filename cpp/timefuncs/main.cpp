#include "main.h"
#include <ctime>
#include <iostream>

std::tm OptionsTimeFunctions::SetEndOfDay(){
    std::tm eod_tm;
    eod_tm.tm_hour = this->hour;
    eod_tm.tm_min = this->min;
    eod_tm.tm_sec = this->sec;
    return eod_tm;
}


// This function could be more faster with lambda, however I do not know how to do that, if someone does please reach out about this
std::vector<OptionData> TimeFilter(const std::vector<OptionData>& OptionDataVec,
                                    const std::tm& start_trade_time,
                                    const std::tm& end_trade_time){
                            
            std::vector<OptionData> FilteredData;
            FilteredData.reserve(OptionDataVec.size());

            int start_hour = start_trade_time.tm_hour;
            int end_hour = end_trade_time.tm_hour;

            int start_min = start_trade_time.tm_min;
            int end_min = end_trade_time.tm_min;

            int start_sec = start_trade_time.tm_sec;
            int end_sec = end_trade_time.tm_sec;

            const auto start_time_tuple = std::make_tuple(start_hour,
                                                          start_min,
                                                          start_sec);

            const auto end_time_tuple = std::make_tuple(end_hour,
                                                        end_min,
                                                        end_sec);

            for(const auto& data: OptionDataVec){
                const std::tm& curr_time = data.datetime;

                auto current_time_tuple = std::make_tuple(curr_time.tm_hour,
                                                    curr_time.tm_min,
                                                    curr_time.tm_sec);

                if((current_time_tuple>= start_time_tuple) && (current_time_tuple<=end_time_tuple)){
                    FilteredData.push_back(data);
                }
            }

            return FilteredData;
}
