// Please install curl libraries before using
// also note its best to run the function using this: g++ main.cpp -o main -lcurl


#include "main.h"

#define URL "https://ttblaze.iifl.com"
#define HOST_LOOK_UP_PATH ":4000/HostLookUp"
#define LOGIN_PATH "/apimarketdata/auth/login"


std::filesystem::path current_wordking_directory = std::filesystem::current_path();
std::filesystem::path config_file_path = current_wordking_directory / "login_xts.ini";
const std::string config_file_path_str = config_file_path.string();

// append works with C++98,11,14
size_t write_callback(void* contents, size_t size, size_t nmemb, std::string* userp){
    userp->append((char*)contents, size*nmemb);
    return size*nmemb;
}


// adding a dynamic constructor 
MarketDataCredentials::MarketDataCredentials(
    const std::string& url,
    const std::string& access_password,
    const std::string& version,
    const std::string& secret_key,
    const std::string& api_key) : url(url), access_password(access_password), version(version), secret_key(secret_key), api_key(api_key) {
    // creating the directory for the .ini file here 
    std::filesystem::create_directories(std::filesystem::path(config_file_path_str).parent_path());
}

void MarketDataCredentials::writeConfig(const std::string& key, const std::string& value){
    // creating a config file to be written with the response data
    std::ofstream config_file(config_file_path_str,std::ios::app); //using std::ios::app to write items to the end of the file
    if(!config_file.is_open()){
        throw std::runtime_error("Unable to open config file for writing");
    }

    // using getline is also another way but this makes it more visual to see errors 
    config_file<<key<<"="<<value<<"\n";
    config_file.close();
}

std::string MarketDataCredentials::readConfig(const std::string& key){
    std::ifstream config_file(config_file_path_str);
    if(!config_file.is_open()){
            throw std::runtime_error("Unable to open config file for reading");
    }

    std::string line;

    while(std::getline(config_file,line)){
        if(line.rfind(key,0) == 0){
            config_file.close();
            return line.substr(key.size()+1);
        }
    }

    config_file.close();
    throw std::runtime_error("Unable to find the key: "+key);
}

void MarketDataCredentials::hostLookUp(){
    CURL* curl;
    if(!curl){
        std::cerr<<"Error intialising curl in hostLookUp() in MarketDataCredentials class"<<std::endl;
        return;
    }
    CURLcode res;
    std::string response_buffer;


    curl = curl_easy_init();
    if(curl){
        try {    
            std::string HOST_LOOKUP_URL = URL + HOST_LOOK_UP_PATH;
            curl_easy_setopt(curl, CURLOPT_URL, HOST_LOOKUP_URL.c_str());//have to use c_str() for libcurl which is c specific
            curl_easy_setopt(curl, CURLOPT_POST, 1L); //adding this post functionality

            // adding below the json payload
            Json::Value json_data;
            json_data["accesspassword"] = access_password;
            json_data["version"] = version;

            Json::StreamWriterBuilder writer;
            std::string json_data_str = Json::writeString(writer, json_data);

            // update the headers here
            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, "Content-Type: application/json");
            curl_easy_setopt(curl,CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curl,CURLOPT_POSTFIELDS, json_data_str.c_str());
            curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION, write_callback);
            curl_easy_setopt(curl,CURLOPT_WRITEDATA, &response_buffer);

            res = curl_easy_perform(curl);
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);

        } catch (std::exception& e){
            std::cerr<<"Exception occured while excuting curl in hostLookUp() in MarketDataCredentials class"<<std::endl;
        }

        if(res!= CURLE_OK){
            // throw std::runtime_error("An error occured while sending a post request from the hostLookUp() in MarketDataCredentials class: \n");
            std::cout<<"An error occured while sending a post request from the hostLookUp() in MarketDataCredentials class: \n"<<std::endl;
            std::cerr<<curl_easy_strerror(res)<<std::endl;
        }

        Json::CharReaderBuilder reader;
        Json::Value response_data;
        std::string errors;

        std::istringstream res_buff(response_buffer);

        if(!Json::parseFromStream(reader, res_buff, &response_data, &errors)){
            std::cerr<<"Failed to read the json file from hostLookUp() in MarketDataCredentials class"<<std::endl;
        }

        std::cout<<"Read the json file from hostLookUp() in MarketDataCredentials class"<<std::endl;

        std::string unique_key = response_data["result"]["uniqueKey"].asString();

        if(unique_key.empty()){
            throw std::runtime_error("Unique key returned from the json response is empty");
        } else {
            std::string auth_token(unique_key);
            writeConfig("auth_token",auth_token);
        }

    }
}


void MarketDataCredentials::loginMarketApi() {
    std::string authToken;
    
    try {
        authToken = readConfig("auth_token");
    } catch (std::runtime_error& e){
        throw std::runtime_error("Error occured while getting authToken from readConfig()")
    }

    if (authToken.empty()){
        hostLookUp();
        authToken = readConfig("unique_key");
    }

    CURL* curl;
    CURLcode res;
    std::string resBuffer;

    curl = curl_easy_init();

    if (curl) {
        std::string LOGIN_MARKET_URL = URL + LOGIN_PATH;

        try {
            Json::Value payload;
            payload["secretKey"] = secret_key;
            payload["apiKey"] = api_key;
            payload["source"] = "WebAPI";
            
            Json::StreamWriterBuilder writer;
            std::string payloadString = Json::writeString(writer, payload);
        } catch (std::runtime_error& e) {
            throw std::runtime_error("Error arising in creation of payload for loginMarketApi()");
        }

        try {
            struct curl_slist* headers = NULL;
            // just an explanation here since i got confused curl_slist_append() returns the head of the list each time
            headers = curl_slist_append(headers, ("Content-Type: application/json"));
            headers = curl_slist_append(headers, ("authorization: " + authToken.c_str())); //since its a c lib you need to convert the string
        } catch (std::runtime_error& e) {
            throw std::runtime_error("Error arising in creation of headers for loginMarketApi()");
        }
    }
}