#ifndef ROUTECONFIG_H
#define ROUTECONFIG_H

#include <string>
#include <map>

class RouteConfig {
public:
    RouteConfig();
    std::map<std::string, std::string> routes;

private:
    void initialize();
};

#endif 
