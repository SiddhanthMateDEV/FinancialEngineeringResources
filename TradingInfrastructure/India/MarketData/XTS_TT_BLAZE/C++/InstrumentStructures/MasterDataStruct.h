#ifndef MASTERDATASTRUCT_H
#define MASTERDATASTRUCT_H
#include <string>

struct MasterDataStruct {
    std::string exchangeSegment;
    int exchangeSegmentID;
    std::string InstrumentType;
    std::string name;
    std::string description;
    std::string series;
    std::string NameWithSeries;
    std::string InstrumentID;
    double PriceBandHigh;
    double PriceBandLow;
    long int FreezeQty;
    float TickSize;
    int LotSize;
    int Multiplier;
    int UnderlyingInstrumentId;
    std::string UnderlyingIndexName;
    std::string ContractExpiration; //Needs to be edited while processing
    int StrikePrice;
    std::string OptionType;
    std::string DisplayName;
    int PriceNumerator;
    int PriceDenominator;
    std::string DetailedDescription;
};

#endif
