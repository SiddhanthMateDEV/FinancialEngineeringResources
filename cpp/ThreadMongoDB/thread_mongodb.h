#ifndef THREAD_
#define MAIN

#include <iostream>
#include "mongodb_handler.h"
#include "CSVReader.h"
#include "StockData.h"

// ignore this directory for now its based of some old code of mine
class thread_mongodb{
    private:
        // for csv reader functions
        std::string filename;
        // for database functions
        std::string db_name;
        std::string collection;
        std::string uri;    
    public:
        mongodb_tasks(const std::string& filename, const std::string& db_name, const std::string collection, const std::string& uri);
        std::vector<std::string>;
}

#endif