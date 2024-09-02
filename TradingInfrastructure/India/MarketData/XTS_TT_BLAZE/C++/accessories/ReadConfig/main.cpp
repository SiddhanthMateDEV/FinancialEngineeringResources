#include "main.h"

void ReadIni::writeConfig(const std::string& key, 
                          const std::string& value,
                          const std::string& ConfigFilePathString){
    // creating a config file to be written with the response data
    std::ofstream config_file(ConfigFilePathString,std::ios::app); //using std::ios::app to write items to the end of the file
    if(!config_file.is_open()){
        throw std::runtime_error("Unable to open config file for writing");
    }

    // using getline is also another way but this makes it more visual to see errors 
    config_file<<key<<"="<<value<<"\n";
    config_file.close();
}

std::string ReadIni::readConfig(const std::string& key,
                                const std::string& ConfigFilePathString){
    std::ifstream config_file(ConfigFilePathString);
    if(!config_file.is_open()){
            throw std::runtime_error("Unable to open config file for reading");
    }

    std::string line;

    while(std::getline(config_file,line)){
        if(line.rfind(key,0) == 0){
            config_file.close();
            return line.substr(key.size()+1);
        } else {
            config_file.close();
            throw std::runtime_error("Unable to find the key");
        }
    }

}