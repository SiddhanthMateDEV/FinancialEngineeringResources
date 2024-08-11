#include "main.h"
#include <ctime>

std::tm OptionsTimeFunctions::SetEod(){
            this->tm.tm_hour = 15;
            this->tm.tm_min = 30;
            this->tm.tm_sec = 0;
            return this->tm;
}

