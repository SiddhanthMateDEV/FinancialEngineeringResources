#include <iostream>
#include <filesystem>
#include <string>
#include <fstream>

int main(){
    std::string filename = "./login.ini";
    
    std::string folder_path = std::filesystem::current_path();
    if(!std::filesystem::exists(filename)){
        std::cout<<"login.ini File Exists in the Current Working Directory"<<std::endl;
    } 
    std::ofstream file(filename);

    std::string token = "fnwerjfnwolejkfn";
    std::string auth_token = "nfeowrjnbforje";
    
    file<<"[AUTH]\n";
    file<<"TOKEN = "<<token;

    file.close();


    return 0;
}