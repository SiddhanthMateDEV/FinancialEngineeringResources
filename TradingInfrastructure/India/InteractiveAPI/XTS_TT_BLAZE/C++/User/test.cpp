#include <iostream>
#include <string>
#include "main.h"


int main(){
    std::string access_password = "2021HostLookUpAccess";
    std::string version = "interactive_1.0.1";
    std::string secretKey = "sfnwkiherbfiwqpej";
    std::string apiKey = "fndeklwrjngo";
    std::string config_file_path = "ffnejwlejnbflwejrf";

    User user(access_password, 
                    version, 
                    apiKey, 
                    secretKey, 
                    config_file_path,
                    "ttblaze");

}