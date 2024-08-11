#include "./main.h"

std::vector<StockData> CSVReader::EquityFileReader() {
    std::vector<StockData> stock_data;
    std::ifstream file(filename);

    if (!file.is_open()){
        throw std::runtime_error("Error Opening Equity Data");
    }

    std::string line;

    if (header) std::getline(file,line);

    while (std::getline(file,line)) {
        std::stringstream ss(line);
        StockData tick_info;

        std::getline(ss,tick_info.date,',');
        std::getline(ss,tick_info.time,',');
        
        std::string open_,close_,high_,low_,volume_,ticker_,datetime_;
        std::tm tm = {};

        try {

            std::getline(ss,open_,',');
            std::getline(ss,high_,',');
            std::getline(ss,low_,',');
            std::getline(ss,close_,',');
            std::getline(ss,volume_,',');
            std::getline(ss,ticker_,',');
            std::getline(ss,datetime_,',');
            
            std::string datetime_with_seconds(datetime_);
            std::cout<<"Datetime: "<<datetime_<<std::endl;

            if(std::count(datetime_.begin(),datetime_.end(),':') == 1) {
                datetime_with_seconds += DEFAULT_SECONDS;//DEFAULT_SECONDS is a macro i defined in CSVReader.h
            } 

            std::istringstream datetime_stream(datetime_with_seconds);

            if(datetime_stream >> std::get_time(&tm,"%Y-%m-%d %H:%M:%S")){            
                tm.tm_sec = 0;
                tm.tm_year += 1900;
                tm.tm_mon += 1;
            } else {
                throw std::runtime_error("Error parsing datetime string into tm");
            }

            tick_info.open = std::stod(open_);
            tick_info.high = std::stod(high_);
            tick_info.low = std::stod(low_);
            tick_info.close = std::stod(close_);
            tick_info.volume = std::stod(volume_);
            
            tick_info.ticker = ticker_;
            tick_info.datetime = tm;
       
        } catch (const std::invalid_argument& e) {
            std::cerr<<"Invalid argument: "<<e.what()<<std::endl;
        } catch (const std::out_of_range& e) {
            std::cerr<<"Value out of range: "<<e.what()<<std::endl;
        }

        stock_data.push_back(tick_info);
    }
    file.close();
    return stock_data;
}

std::vector<OptionData> CSVReader::OptionsFileReader() {
    std::vector<OptionData> options_data;
    std::ifstream file(filename);

    if(!file.is_open()){
        throw std::runtime_error("Error Opening Options Data");
    }

    std::string line;
    if (header) std::getline(file,line);

    while(std::getline(file,line)){
        std::stringstream ss(line);
        std::tm tm = {};

        OptionData tick_info;  

        std::string date_, time_, open_, high_, low_, close_, volume_, openInterest_;

        try {    
        std::getline(ss,tick_info.ticker,',');
        std::getline(ss,date_,',');
        std::getline(ss,time_,',');
        
        std::getline(ss,open_,',');   
        std::getline(ss,high_,',');   
        std::getline(ss,low_,',');   
        std::getline(ss,close_,',');

        std::getline(ss,volume_,',');   
        std::getline(ss,openInterest_,',');  
        } catch (std::runtime_error& e) {
            throw std::runtime_error("Error reading the stream in OptionsFileReader()");
        }

        try {
        tick_info.date = date_;
        tick_info.time = time_;

        tick_info.open = std::stod(open_);
        tick_info.high = std::stod(high_);
        tick_info.low = std::stod(low_);
        tick_info.close = std::stod(close_);

        tick_info.volume = std::stod(volume_);
        tick_info.openInterest = std::stod(openInterest_);
        } catch (std::runtime_error& e) {
            throw std::runtime_error("Error Parsing Strings into OptionData Struct in OptionsFileReader()");
        }

        std::string datetime_str = date_ + " " + time_;
        
        std::string datetime_with_seconds(datetime_str);
        std::istringstream dts(datetime_str);

        if(std::count(datetime_str.begin(),datetime_str.end(),':') ==1){
            datetime_with_seconds += DEFAULT_SECONDS;
        }

        std::istringstream datetime_stream(datetime_with_seconds);
        if(datetime_stream >> std::get_time(&tm,"%Y-%m-%d %H:%M:%S")){
            tm.tm_sec = 0;
            tm.tm_year += 1900;
            tm.tm_mon += 1;
        } else {
            throw std::runtime_error("Error In Parsing Stream into tm Structure OptionsFileReader()");
        }
        
        tick_info.datetime = tm;

        options_data.push_back(tick_info);
    }
    file.close();
    return options_data;
}