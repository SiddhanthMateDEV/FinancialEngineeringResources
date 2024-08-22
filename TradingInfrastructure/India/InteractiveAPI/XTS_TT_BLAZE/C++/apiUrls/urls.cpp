#include "urls.h"

std::string URLs::root_url(){
    if(this->base_url.empty()){
        return "https://ttblaze.iifl.com";
    } else {
        return this->base_url;
    }
}