#include "../main.h"
#include "../../ReadConfig/main.h"

/* 
This instance when run once a day creats and stores the new AUTH TOKEN
from hostLookUp() and takes the AUTH_TOKEN to login and get the LOGIN_TOKEN
which can be later be used through the day for different functionalities
 */
class LoginDetails : public MarketDataCredentials, public ReadIni {
    private:
        const std::string api_key;
        const std::string secret_key;
        const std::string auth_token;
        const std::string login_token;
        MarketDataCredentials mdc;
        ReadIni ri;
    public:
        LoginDetails() : api_key(ri.readConfig("API_KEY","../login.ini")),
                         secret_key(ri.readConfig("SECRET_KEY","../login.ini")),           
                         mdc("https://ttblaze.iifl.com",
                             "2021HostLookUpAccess",
                             "interactive_1.0.1",
                             secret_key,
                             api_key) {};
        void HostLookUp(){
            mdc.hostLookUp();
        }
        void login(){
            mdc.loginMarketApi();
        }
};

int main(){
    LoginDetails _ld;
    _ld.HostLookUp();
    _ld.login();
}