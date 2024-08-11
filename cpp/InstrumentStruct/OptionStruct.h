#ifndef OPTIONSTRUCTS_H
#define OPTIONSTRUCTS_H

#include <string>
#include <iostream>


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