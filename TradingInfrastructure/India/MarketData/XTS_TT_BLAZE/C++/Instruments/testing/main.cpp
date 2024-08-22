#include "../main.h"
#include "../accessories/ReadConfig/readini.h"

/* 
This instance when run once a day creats and stores the new AUTH TOKEN
from hostLookUp() and takes the AUTH_TOKEN to login and get the LOGIN_TOKEN
which can be later be used through the day for different functionalities
 */
class RunInstruments : public ReadIni {
    public:
        LoginDetails() :    ReadIni(),

                            MarketDataAPIFunctions(
                                                        const std::string& url,
                                                        const std::string& secretKey,
                                                        const std::string& apiKey,
                                                        const std::string& authToken,
                                                        const std::string& token) : 
                                    {
            HostLookUp();
            Login();
            /* 
            I will be adding a functionality to logout based on end of day of 
            market session
            */
        };
};

int main(){
    LoginDetails _ld;
}