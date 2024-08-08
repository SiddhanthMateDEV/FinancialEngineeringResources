#ifndef STOCKDATA_H
#define STOCKDATA_H

#include <string>
#include <ctime>


struct StockData{
    std::string date;
    std::string time;
    double open;
    double high;
    double low;
    double close;
    long int volume;
    std::string ticker;
    std::tm datetime; 
};

#endif

