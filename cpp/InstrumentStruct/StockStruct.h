#ifndef STOCKSTRUCT_H
#define STOCKSTRUCT_H

#include <string>
#include <ctime>
#include <iostream>


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