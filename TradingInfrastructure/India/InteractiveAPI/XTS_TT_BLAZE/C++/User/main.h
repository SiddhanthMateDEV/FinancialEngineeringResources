#ifndef MAIN_H
#define MAIN_H

#include <iostream>
#include <string>
#include <vector>
#include "../apiUrls/urls.h"


class URLs;

class User : public URLs {
    private:
        std::string access_password;
        std::string version;
        std::string apiKey;
        std::string secretKey;
        std::string config_file_path;
        
    public:
        User(const std::string& access_password, 
             const std::string& version, 
             const std::string& apiKey, 
             const std::string& secretKey, 
             const std::string& config_file_path,
             const std::string& base_url);
        void HostLookUp();
        void SessionLogin();
        void SessionLogout();
        void Profile();
};

#endif