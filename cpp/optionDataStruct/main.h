#ifndef MAIN_H
#define MAIN_H

#include <string>
// include this to use tm data structures 
#include <ctime>

// Assuming these are the columns, Ticker	Date	Time	Open	High	Low	Close	Volume	Open Interest
struct OptionData{
    std::string ticker;
    std::string date;
    std::string time;
    double open;
    double high;
    double low;
    double close;
    long int volume;
    long int openInterest;
    std::tm datetime;
};


#endif