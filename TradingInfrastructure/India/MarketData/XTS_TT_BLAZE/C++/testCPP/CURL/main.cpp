// This is a playground to test curl functionalities

#include <iostream>
#include <curl/curl.h>
#include <fstream>
#include <iostream>


int main(){
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json1");
    headers = curl_slist_append(headers, "Content-Type: application/json2");

    struct curl_slist *current = headers;
    while(headers!=NULL){
        std::cout<<headers->data<<std::endl;
        headers = headers->next;
    }
}