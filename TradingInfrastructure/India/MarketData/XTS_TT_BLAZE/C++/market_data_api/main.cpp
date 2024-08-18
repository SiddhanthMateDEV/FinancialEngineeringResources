#include "main.h"

// [6]
size_t WriteCallBack(void* contents,size_t size,size_t nmembs, std::string* response) {
    size_t totalSize = size*nmembs;
    response->append(static_cast<char*>(contents),totalSize);
    return totalSize;
}



MarketDataAPIFunctions::MarketDataAPIFunctions(
                               const std::string& url,
                               const std::string& secretKey,
                               const std::string& apiKey,
                               const std::string& authToken,
                               const std::string& token) : url(url), 
                                                           secretKey(secretKey), 
                                                           apiKey(apiKey), 
                                                           authToken(authToken), 
                                                           token(token) {}

MarketDataAPIFunctions::MarketDataAPIFunctions(const std::string& url,
                                            const std::string& secretKey,
                                            const std::string& apiKey,
                                            const std::string& authToken,
                                            const std::string& token){
    std::string filename = "./login.ini";
    std::string folder_path(std::filesystem::current_path());
    if(std::filesystem::exists(filename)){
        std::cout<<"login.ini File Exists in the Current Working Directory"<<std::endl;
        std::ifstream inFile(filename);

        if(inFile.is_open()){
            std::string line;
            std::string currentSection;
            std::map<std::string,std::string> config;

            while(std::getline(inFile,line)){
                if(line.empty()) continue;
                std::istringstream istream(line);
                std::string key, value;

                if(std::getline(istream,key,"=") && std::getline(istream,value)){
                    key.erase(0,key.find_first_not_of(" \t"));
                    key.erase(key.find_last_not_of("\t")+1);

                    value.erase(0,key.find_first_not_of(" \t"));
                    value.erase(key.find_last_not_of("\t")+1);

                    config[key] = value;
                }
            }
        }
    } else {
        this->url = url;
        this->apiKey = apiKey;
        this->authToken = authToken;
        this->token = token;
        this->secretKey = secretKey;

        std::ofstream file(filename);
        file<<"AUTH_TOKEN = "<<authToken;
        file<<"TOKEN = " << token;
        file<<"API_KEY = " << apiKey;
        file<<"SECRET_KEY = "<< secretKey;
        file.close();
    }

},


std::tuple<int,std::vector<std::string>> MarketDataAPIFunctions::IndexList(const int& exchangeSegment, const std::string& section_header, const std::string& section_item_name) {
    
    CURL* curl;
    curl = curl_easy_init();
    if(!curl){
        std::cerr<<"Error intialising curl in IndexList() in MarketDataAPIFunctions class"<<std::endl;
        return;
    }
    CURLcode res;
    std::string response_buffer;

    std::string authorisation = "authorization: " + this->token;
    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, authorisation.c_str());

    std::string json_payload_str;
    Json::Value payload_json;
    payload_json["exchangeSegment"] = exchangeSegment;
    Json::StreamWriterBuilder writer;
    payload_str = Json::writeString(writer,payload);

    const std::string url = "https://ttblaze.iifl.com/apimarketdata/instruments/indexlist";

    if(curl){
        curl_easy_opt(curl, CURLOPT_URL,url);
        curl_easy_opt(curl, CURLOPT_WRITEFUNCTION, WriteCallBack);
        curl_easy_opt(curl, CURLOPT_WRITEDATA, &response_buffer);

        if(response_buffer.empty()){
            throw std::runtime_error("The response buffer is empty while getting the IndexListResponse()");
        }

        res = curl_easy_perform(curl);
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        if(res!=CURLE_OK){
            throw std::runtime_error("Bad Request please check the parameters while sending a get request for IndexListResponse()");
        }
        
        Json::CharReaderBuilder reader;
        Json::Value response_data;
        std::string errors;

        std::istringstream res_buff(response_buffer);
        if(!Json::parseFromStream(reader,res_buff,&response_data, &errors)){
            throw std::runtime_error("Error reading buffer into JSON object in IndexList()");
        }

        const Json::Value& result = response_data[0]["result"];
        const int exchangeSegment = result["exchangeSegment"].asInt();

        std::vector<std::string> IndexList;
        for(const auto& index_item: result["indexList"]){
            IndexList.push_back(index_item.asString());
        }

        // Print items to test this function
        std::cout<<"Index: "<<std::endl;
        for(const auto& index_item: IndexList){
            std::cout<<"-"<<index_item<<std::endl;
        }
        std::cout<<"exchangeSegment: "<<exchangeSegment<<std::endl;

        return std::make_tuple(exchangeSegment,IndexList);
    } else {
        std::cout<<"Something went wrong with IndexListResponse()"<<std::endl;
    }
}

std::vector<std::string> SeriesListResponse(const int& exchangeSegment, const std::string& segment_header, const std::string& segment_item_name){
    CURL* curl;
}

