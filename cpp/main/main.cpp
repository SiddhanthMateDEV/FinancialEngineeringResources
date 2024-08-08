#include <iostream>

#include "../CSVReader/main.h"
#include "../instrumentStructures/main.h"

#include <vector>
#include <sstream>


// This is a playground code setup to test print it and see if the output is correct or not


int main(){
    std::string file_path = "/Users/siddhanthmate/Desktop/AllFiles/CODE/WORK_CODE/fintech/DATA/EQUITY_DATA/60min_data/AARTIIND.csv";

    CSVReader csv_reader(file_path, true);

    std::vector<StockData> stock_data = csv_reader.EquityFileReader();

    for(const auto& data: stock_data){
        std::cout<<"Date:"<<data.date
                  << ", Time: " << data.time
                  << ", Open: " << data.open
                  << ", High: " << data.high
                  << ", Low: " << data.low
                  << ", Close: " << data.close
                  << ", Volume: " << data.volume
                  << ", Ticker: " << data.ticker
                  << ", Year: " << data.datetime.tm_year 
                  << ", Day: " << data.datetime.tm_mday
                  << ", Month: " << data.datetime.tm_mon
                  << ", Hour: " << data.datetime.tm_hour 
                  << ", Minute: " << data.datetime.tm_min 
                  << ", Second: " << data.datetime.tm_sec 
                  << std::endl;
    }
    return 0;
}

