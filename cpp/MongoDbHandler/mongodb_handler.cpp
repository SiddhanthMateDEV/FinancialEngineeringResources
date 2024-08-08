// mongodb_handler.cpp
#include "mongodb_handler.h"

mongodb_handler::mongodb_handler(
    const std::string& uri, const std::string& db_name, std::sting& coll_name
) : cli_(mongocxx::uri(uri)) , db_(cli_[dn_name]), coll_(db_[coll_name]) {}

void mongohandler::insert_stock_data(const std::vector<StockData>& stock_data_vector){
    for(const auto& stock : stock_data_vector){
        bsoncxx::builder::stream::document document{};
        document<<"date"<<stock.date
                <<"time"<<stock.time
                <<"open"<<stock.open
                <<"high"<<stock.high
                <<"low"<<stock.low
                <<"close"<<stock.close
                <<"volume"<<stock.volume
                <<"ticker"<<stock.ticker
                <<"datetime"<<stock.datetime;
        coll_.insert_one(document.view());
    }
}