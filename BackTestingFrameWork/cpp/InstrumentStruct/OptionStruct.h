#ifndef OPTIONSTRUCTS_H
#define OPTIONSTRUCTS_H

#include <string>
#include <iostream>


struct OptionData{
    std::string ticker;
    std::string date;
    std::string time;
    long int strike_price;
    double open;
    double high;
    double low;
    double close;
    long int volume;
    long int openInterest;
    std::tm datetime;
    std::string option_type;
};


#endif