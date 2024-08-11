#ifndef MAIN_H
#define MAIN_H


#include <iostream>
#include <ctime>
#include <vector>
#include <string>
#include <ctime>


class OptionsTimeFunctions {
    private:
        std::tm tm;
    public:
        OptionsTimeFunctions(const std::tm& tm){
            this->tm = tm;
        }
        std::tm SetEod();
        

};


#endif