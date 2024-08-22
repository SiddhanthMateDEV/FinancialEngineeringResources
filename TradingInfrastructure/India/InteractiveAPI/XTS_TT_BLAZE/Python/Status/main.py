from ..apiUrls.main import XTS_URLS


class Status(XTS_URLS):
    def __init__(self):
        super().__init__()

    def Status(self,
               userID : str,
               auth_token : str):
        
        if userID is None:
            userID = "SYMP"

        STATUS_URL = fr"{self.base_url}/interactive/status/exchange?userID={userID}"