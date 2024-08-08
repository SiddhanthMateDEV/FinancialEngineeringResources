#ifndef CSVREADER_H
#define CSVREADER_H

#include "../StockDataStruct/StockData.h"
#include "../optionDataStruct/main.h"

#include <iostream>
#include <fstream>
#include <sstream>

#include <string>
#include <vector>

#include <stdexcept>
#include <ctime>

#include <iomanip>
#include <algorithm>

#define DEFAULT_SECONDS ":00" //this macro is defined to set datetime ss to 00 if not set before


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