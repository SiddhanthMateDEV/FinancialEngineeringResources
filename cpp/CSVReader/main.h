#ifndef MAIN_H
#define MAIN_H
#define DEFAULT_SECONDS ":00" //this macro is defined to set datetime ss to 00 if not set before


#include <iostream>
#include <fstream>
#include <sstream>

#include <string>
#include <vector>

#include <stdexcept>
#include <ctime>

#include <iomanip>
#include <algorithm>

#include <string>
#include <ctime>


// Structures required
// if needed add your own or customise it here
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



class CSVReader{
    private:
        std::string filename;
        bool header;
    public:
        CSVReader(const std::string& filename, const bool& header) : filename(filename), header(header) {}
        std::vector<StockData> EquityFileReader();
        std::vector<OptionData> OptionsFileReader();
};

#endif

