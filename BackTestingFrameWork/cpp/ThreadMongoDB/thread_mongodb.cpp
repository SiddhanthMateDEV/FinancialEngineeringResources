#include "thread_mongodb.h"
#include "mongodb_handler.h"
#include "CSVReader.h"
#include "StockData.h"



thread_mongodb::thread_mongodb(const std::string& filename, const std::string& db_name, const std::string& collection, const std::string& uri) : filename(filename), db_name(db_name), collection(collection), uri(uri) {}


std::vector<std::string> thread_mongodb::mongodb_tasks(){
    CSVReader::file_reader()
}