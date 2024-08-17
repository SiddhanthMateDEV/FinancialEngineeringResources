#include <iostream>
#include <filesystem>

int main(){
    // const size_t size = 1024;
    // char buffer[size];
    // if(getcwd(buffer,size)!=NULL){
    //     std::cout<<"Current Working Directory: "<<buffer<<std::endl;
    // } else {
    //     std::cerr<<"Error getting cwd"<<std::endl;
    // }
    std::string file_path = std::filesystem::current_path();
    std::cout<<"Current Path is: "<<file_path<<std::endl;

    return 0;
}