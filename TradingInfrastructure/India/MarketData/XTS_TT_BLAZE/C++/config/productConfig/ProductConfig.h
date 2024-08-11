#ifndef PRODUCTCONFIG_H
#define PRODUCTCONFIG_H

#include <string>
#include <map>

class ProductConfig {
public:
    ProductConfig();
    
    std::map<std::string, std::string> Products;
    std::map<std::string, std::string> Order_types;
    std::map<std::string, std::string> Transaction_type;
    std::map<std::string, std::string> Squareoff_mode;
    std::map<std::string, std::string> Squareoff_position_quantity_types;
    std::map<std::string, std::string> Validity;
    std::map<std::string, std::string> Exchange_Segments;

private:
    void initialize();
};

#endif 
