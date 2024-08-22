#include "main.h"
#include <iostream>

User::User(const std::string& access_password,
            const std::string& version,
            const std::string& apiKey,
            const std::string& secretKey,
            const std::string& config_file_path,
            const std::string& base_url) 
            : URLs(base_url),
              access_password(access_password),
              version(version),
              apiKey(apiKey),
              secretKey(secretKey),
              config_file_path(config_file_path) {

    std::cout<<"Access Password: "<<this->access_password<<std::endl;
    std::cout<<"apiKey: "<<this->apiKey<<std::endl;
    std::cout<<"secretKey: "<<this->secretKey<<std::endl;
    std::cout<<"version: "<<this->version<<std::endl;
    std::cout<<"config_file_path: "<<this->config_file_path<<std::endl;
    std::cout<<"url: "<<URLs::root_url()<<std::endl;

}

