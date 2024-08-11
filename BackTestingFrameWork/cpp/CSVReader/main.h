#ifndef MAIN_H
#define MAIN_H
#define DEFAULT_SECONDS ":00" //this macro is defined to set datetime ss to 00 if not set before


#include <iostream>
#include <fstream>
#include <sstream>

#include "../InstrumentStruct/OptionStruct.h"
#include "../InstrumentStruct/StockStruct.h"

#include <vector>

#include <stdexcept>
#include <ctime>

#include <iomanip>
#include <algorithm>

#include <string>
#include <ctime>

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

