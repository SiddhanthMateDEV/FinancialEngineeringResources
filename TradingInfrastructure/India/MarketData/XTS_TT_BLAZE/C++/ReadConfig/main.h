#ifndef READINI_H
#define READINI_H

#include <string>
#include <fstream>
#include <iostream>
#include <filesystem>
#include <stdexcept>

class ReadIni {
    public:
        ReadIni() {};
        void writeConfig(const std::string& key, const std::string& value, const std::string& ConfigFilePathString);
        std::string readConfig(const std::string& key, const std::string& ConfigFilePathString);
};

#endif