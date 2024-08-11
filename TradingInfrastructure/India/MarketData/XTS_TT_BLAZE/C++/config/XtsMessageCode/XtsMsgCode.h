#ifndef XTSMESGCODE_H
#define XTSMESGCODE_H

#include <vector>

class XtsMessageCodes {
public:
    XtsMessageCodes();

    std::vector<int> xts_message_codes;

private:
    void initialize();
};

#endif 
