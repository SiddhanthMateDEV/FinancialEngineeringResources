#ifndef URLS_H
#define URLS_H

#include <iostream>
#include <string>

class URLs {
    public:
        std::string base_url;
        URLs(const std::string& base_url) : base_url(base_url) {};
        std::string root_url();
};

#endif