#ifndef MONGODB_HANDLER_H
#define MONGODB_HANDLER_H

#include <cstdint>
#include <iostream>
#include <vector>
#include <bsoncxx/builder/basic/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>
#include <mongocxx/stdx.hpp>
#include <mongocxx/uri.hpp>

#include "StockData.h"

using bsoncxx::builder::basic::kvp;
using bsoncxx::builder::basic::make_array;
using bsoncxx::builder::basic::make_document;


#include <string>

class mongo_handler {
    private:
        mongocxx::instance inst_;
        mongocxx::client cli_;
        mongocxx::database db_;
        mongocxx::collection coll_;

    public:
        mongo_handler(const std::string& uri, const std::string& db_name, const std::string& coll_name);
        void insert_stock_data(const std::vector<StockData>& stock_data_vector);

}

#endif