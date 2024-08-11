#include "main.h"
#include <ctime>
#define START_YEAR 2000
#define CURRENT_YEAR 2024



// This function could be more faster with lambda, however I do not know how to do that, if someone does please reach out about this
std::vector<OptionData> Strangle::CallDataVec(){             
    if(OptionDataVec.empty()){
        throw std::invalid_argument("OptionDataVec Passed To CallDataVec() Is Empty");
    }
    

    std::vector<OptionData> FilteredCallData;
    FilteredCallData.reserve(OptionDataVec.size());

    const int expiry_day = this->expiry.tm_mday;
    const int expiry_month = this->expiry.tm_mon;
    const int expiry_year = this->expiry.tm_year;


    if(expiry_day < 0 || expiry_day > 31 ||
        expiry_month < 1 || expiry_month > 12 || 
        expiry_year < START_YEAR || expiry_year > CURRENT_YEAR){
            throw std::invalid_argument("expiry Passed To CallDataVec() Is Causing Errors");
    }


    const auto expiry_date_tuple = std::make_tuple(expiry_day,
                                                    expiry_month,
                                                    expiry_year);

    try {
        for(const auto& data: OptionDataVec){
            const std::tm& curr_time = data.datetime;
            const int& curr_strike_price = data.strike_price;
            const std::string& curr_option_type = data.option_type;

            auto current_time_tuple = std::make_tuple(curr_time.tm_mon,
                                                curr_time.tm_mday,
                                                curr_time.tm_year);

            if((current_time_tuple == expiry_date_tuple) && (curr_strike_price == this->strike_price_one) && (curr_option_type == this->call_symbol)){
                FilteredCallData.push_back(data);
            }
        }
    } catch(std::runtime_error& error) {
        throw std::runtime_error("Error Iterating Through Vector In PutDataVec() In Strangle Class");
    }

    return FilteredCallData;
}

std::vector<OptionData> Strangle::PutDataVec(){

    if(OptionDataVec.empty()){
        throw std::invalid_argument("OptionDataVec Passed To PutDataVec() Is Empty In Strangle Class");
    }
    

    std::vector<OptionData> FilteredPutData;
    FilteredPutData.reserve(OptionDataVec.size());

    const int expiry_day = this->expiry.tm_mday;
    const int expiry_month = this->expiry.tm_mon;
    const int expiry_year = this->expiry.tm_year;


    if(expiry_day < 0 || expiry_day > 31 ||
        expiry_month < 1 || expiry_month > 12 || 
        expiry_year < 2000 || expiry_year > 2030){
            throw std::invalid_argument("expiry Passed To PutDataVec() Is Causing Errors In Strangle Class");
    }


    const auto expiry_date_tuple = std::make_tuple(expiry_day,
                                                    expiry_month,
                                                    expiry_year);


    
    try {
        for(const auto& data: OptionDataVec){
            const std::tm& curr_time = data.datetime;
            const int& curr_strike_price = data.strike_price;
            const std::string& curr_option_type = data.option_type;

            auto current_time_tuple = std::make_tuple(curr_time.tm_mon,
                                                curr_time.tm_mday,
                                                curr_time.tm_year);

            if((current_time_tuple == expiry_date_tuple) && (curr_strike_price == this->strike_price_two) && (curr_option_type == this->put_symbol)){
                FilteredPutData.push_back(data);
            }
        }
    } catch(std::runtime_error& error) {
        throw std::runtime_error("Error Iterating Through Vector In PutDataVec() In Strangle Class");
    }
    return FilteredPutData;
}
