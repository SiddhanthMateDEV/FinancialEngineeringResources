#include "main.h"

// [6]
size_t WriteCallBack(void* contents,size_t size,size_t nmembs, std::string* response) {
    size_t totalSize = size*nmembs;
    response->append(static_cast<char*>(contents),totalSize);
    return totalSize;
}


struct Bid {
    int Size;
    double Price;
    int TotalOrders;
    int BuyBackMarketMaker;
};

struct Ask {
    int Size;
    double Price;
    int TotalOrders;
    int BuyBackMarketMaker;
};



// MarketDataAPIFunctions::MarketDataAPIFunctions(
//                                const std::string& url,
//                                const std::string& secretKey,
//                                const std::string& apiKey,
//                                const std::string& authToken,
//                                const std::string& token) : url(url), 
//                                                            secretKey(secretKey), 
//                                                            apiKey(apiKey), 
//                                                            authToken(authToken), 
//                                                            token(token) {}

// MarketDataAPIFunctions::MarketDataAPIFunctions(const std::string& url,
//                                             const std::string& secretKey,
//                                             const std::string& apiKey,
//                                             const std::string& authToken,
//                                             const std::string& token){
//     std::string filename = "./login.ini";
//     std::string folder_path(std::filesystem::current_path());
//     if(std::filesystem::exists(filename)){
//         std::cout<<"login.ini File Exists in the Current Working Directory"<<std::endl;
//         std::ifstream inFile(filename);

//         if(inFile.is_open()){
//             std::string line;
//             std::string currentSection;
//             std::map<std::string,std::string> config;

//             while(std::getline(inFile,line)){138451000
//                 if(line.empty()) continue;
//                 std::istringstream istream(line);
//                 std::string key, value;

//                 if(std::getline(istream,key,"=") && std::getline(istream,value)){
//                     key.erase(0,key.find_first_not_of(" \t"));
//                     key.erase(key.find_last_not_of("\t")+1);

//                     value.erase(0,key.find_first_not_of(" \t"));
//                     value.erase(key.find_last_not_of("\t")+1);

//                     config[key] = value;
//                 }
//             }
//         }
//     } else {
//         this->url = url;
//         this->apiKey = apiKey;
//         this->authToken = authToken;
//         this->token = token;
//         this->secretKey = secretKey;

//         std::ofstream file(filename);
//         file<<"AUTH_TOKEN = "<<authToken;
//         file<<"TOKEN = " << token;
//         file<<"API_KEY = " << apiKey;
//         file<<"SECRET_KEY = "<< secretKey;
//         file.close();
//     }

// }

MarketDataAPIFunctions::MarketDataAPIFunctions() {};


/*
Below is the format for Quotes function json payload:
{
  "instruments": [
    {
      "exchangeSegment": 1,
      "exchangeInstrumentID": 22
    }
  ],
  "xtsMessageCode": 1502,
  "publishFormat": "JSON"
}
*/

void MarketDataAPIFunctions::Quotes(const std::string& token,
                               const int& exchangeSegment,
                               const int& exchangeInstrumentID,
                               const int& xtsMessageCode,
                               const std::string& publishFormat){
    
    /* 
    Define all the variables to be used here:
    */
    CURL* curl = nullptr;
    std::string response_buffer;
    CURLcode res;
    std::string json_payload_string;
    struct curl_slist* headers = nullptr;
    Json::Value instruments_json;
    Json::Value payload_json;

    // This is for read write operations from json to string to send a payload in string form:
    Json::StreamWriterBuilder writer;

    // This is for reading the response from the server:
    Json::CharReaderBuilder reader;
    Json::Value response_data;
    std::string errors;

    // This is for reading the response from the server for the listQutoes key/value:
    Json::CharReaderBuilder list_quotes_stream_reader;
    Json::Value list_quotes_data;
    std::string list_quotes_errors;

    // These vectors will be initialised here and the memory will be created once a response is generated:
    std::vector<Bid> bidsVector;
    std::vector<Ask> asksVector;

    st::string url = "https://ttblaze.iifl.com/apimarketdata/instruments/quotes";

    if(!curl){
        std::cerr<<"Error Intialising Curl in Quotes() In The Instruments Class"<<std::endl;
    }

    std::string authorisation_header = "authorization: " + token;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, authorisation_header.c_str());

    instruments_json["exchangeSegment"] = exchangeSegment;
    instruments_json["exchangeInstrumentID"] = exchangeInstrumentID;
    
    payload_json["instrument"] = Json::arrayValue;
    payload_json["instrument"].append(instruments_json);
    payload_json["xtsMessageCode"] = xtsMessageCode;
    payload_json["publishFormat"] = publishFormat;

    json_payload_string = Json::writeString(writer, payload_json);

    if(curl){
        // adding url to the curl handle
        curl_easy_setopt(curl,CURLOPT_URL,url.c_str());
        // adding headers to the curl handle
        curl_easy_setopt(curl,CURLOPT_HTTPHEADER,headers);
        // adding json payload string to the curl handle
        curl_easy_setopt(curl,CURLOPT_POSTFIELDS,json_payload_string.c_str());
        curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,WriteCallBack);
        curl_easy_setopt(curl,CURLOPT_WRITEDATA,&response_buffer);


        std::cout<<"Peforming A Curl Request To Quotes()"<<std::endl;

        res = curl_easy_perform(curl);
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);

        if(response_buffer.empty()){
            std::cerr<<"The response buffer is empty while getting the Quotes()"<<std::endl;
        }

        if(res!=CURLE_OK){
            std::cerr<<"The response buffer is empty while getting the Quotes(): "<<curl_easy_strerror(res)<<std::endl;
            if(res == CURLE_COULDNT_CONNECT){
                std::cerr<<"Couldn't connect to the server. Please check network connection or server address: "<<curl_easy_strerror(res)<<std::endl;
            } else if(res == CURLE_OPERATION_TIMEDOUT){
                std::cerr<<"The request timedout: "<<curl_easy_strerror(res)<<std::endl;
            } else if(res == CURLE_SSL_CONNECT_ERROR){
                std::cerr<<"SSL Connection Error: "<<curl_easy_strerror(res)<<std::endl;
            }
        }

        std::istringstream response_stream(response_buffer);

        if(!Json::parseFromStream(reader,response_stream,&response_data,&errors)){
            std::cerr<<"Error Encountered While Reading the Response Stream from Quotes(): "<<errors<<std::endl;
            if(errors.find("syntax error")!=std::string::npos){
                std::cerr<<"Syntax error detected while Reading the Response Stream from Quotes()"<<std::endl;
            } else {
                std::cerr<<"An Unknown Error Occured"<<std::endl;
            }
        } 

        if(response[0]["description"].find("Get quotes successfully!")!=std::string::npos){
            std::cerr<<"Server Responded With An error"<<std::endl;
        }

        const Json::Value& result = response_data[0]["result"];
        const int mdp = result["mdp"].asInt();
        const int exchangeSegment_response = result["quoteList"]["exchangeSegment"].asInt();
        const int exchangeInstrumentID_response = result["quoteList"]["exchangeInstrumentID"].asInt();


        /* 
        This part deals with unwrapping the listQuotes in response since it is a string format:
        */
        std::string listQuotes = result["listQuotes"].asString();
        std::istringstream list_quotes_stream(listQuotes);
        

        if(!Json::parseFromStream(list_quotes_stream_reader,list_quotes_stream,&list_quotes_data,&list_quotes_errors)){
            std::cerr<<"Error in Reading String Stream of listQuotes from Quotes()"<<std::endl;
        }

        const int messageCode = list_quotes_data["MessageCode"];
        const int ExchangeSegment = list_quotes_data["ExchangeSegment"];
        const int ExchangeInstrumentID = list_quotes_data["ExchangeInstrumentID"];
        const long int ExchangeTimeStamp = list_quotes_data["ExchangeTimeStamp"];

        const Json::Value& bids = list_quotes_data["Bids"];
        const Json::Value& asks = list_quotes_data["Asks"];

        // Getting the Bids:
        bidsVector.reserve(bids.size());
        for(const auto& bid: bids) {
            bidsVector.emplace_back(Bid{
                bid["Size"].asInt(),
                bid["Price"].asDouble(),
                bid["TotalOrders"].asInt(),
                bid["BuyBackMarketMaker"].asInt()
            });
        }

        // Getting the Asks:
        asksVector.reserve(asks.size());
        for(const auto& ask: asks) {
            asksVector.emplace_back(Ask{
                ask["Size"].asInt(),
                ask["Price"].asDouble(),
                ask["TotalOrders"].asInt(), 
                ask["BuyBackMarketMaker"].asInt()});
        }
        
    }

}


std::tuple<int,std::vector<std::string>> MarketDataAPIFunctions::IndexList(const int& exchangeSegment, 
                    const std::string& section_header, 
                    const std::string& section_item_name,
                    const std::string& token) {
    
    CURL* curl;
    curl = curl_easy_init();
    if(!curl){
        std::cerr<<"Error intialising curl in IndexList() in MarketDataAPIFunctions class"<<std::endl;
        return;
    }
    CURLcode res;
    std::string response_buffer;

    std::string authorisation = "authorization: " + token;
    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, authorisation.c_str());

    std::string json_payload_str;
    Json::Value payload_json;
    payload_json["exchangeSegment"] = exchangeSegment;
    Json::StreamWriterBuilder writer;
    payload_str = Json::writeString(writer,payload);

    std::string url = "https://ttblaze.iifl.com/apimarketdata/instruments/indexlist";

    if(curl){
        curl_easy_opt(curl, CURLOPT_URL,url);
        curl_easy_opt(curl,CURLOPT_HTTPHEADER,headers);
        curl_easy_opt(curl, CURLOPT_WRITEFUNCTION, WriteCallBack);
        curl_easy_opt(curl, CURLOPT_WRITEDATA, &response_buffer);

        res = curl_easy_perform(curl);
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
        
        if(response_buffer.empty()){
            throw std::runtime_error("The response buffer is empty while getting the IndexListResponse()");
        }

        if(res!=CURLE_OK){
            std::cerr<<"Bad Request please check the parameters while sending a get request for IndexListResponse()"<<std::endl;
            if(res == CURLE_COULDNT_CONNECT){
                std::cerr<<"Couldn't connect to the server. Please check network connection or server address: "<<curl_easy_strerror(res)<<std::endl;
            } else if(res == CURLE_OPERATION_TIMEDOUT){
                std::cerr<<"The request timedout: "<<curl_easy_strerror(res)<<std::endl;
            } else if(res == CURLE_SSL_CONNECT_ERROR){
                std::cerr<<"SSL Connection Error: "<<curl_easy_strerror(res)<<std::endl;
            }
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

// std::vector<std::string> SeriesListResponse(const int& exchangeSegment, const std::string& segment_header, const std::string& segment_item_name){
//     CURL* curl;
// }
