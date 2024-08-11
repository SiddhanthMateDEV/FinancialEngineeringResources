class ProductConfig:
    def __init__(self):
        self.products = {
            "Products": {
                "PRODUCT_MIS": "MIS",
                "PRODUCT_NRML": "NRML"
            },
            "Order_types": {
                "ORDER_TYPE_MARKET": "MARKET",
                "ORDER_TYPE_LIMIT": "LIMIT",
                "ORDER_TYPE_STOPMARKET": "STOPMARKET",
                "ORDER_TYPE_STOPLIMIT": "STOPLIMIT"
            },
            "Transaction_type": {
                "TRANSACTION_TYPE_BUY": "BUY",
                "TRANSACTION_TYPE_SELL": "SELL"
            },
            "Squareoff_mode": {
                "SQUAREOFF_DAYWISE": "DayWise",
                "SQUAREOFF_NETWISE": "Netwise"
            },
            "Squareoff_position_quantity_types": {
                "SQUAREOFFQUANTITY_EXACTQUANTITY": "ExactQty",
                "SQUAREOFFQUANTITY_PERCENTAGE": "Percentage"
            },
            "Validity": {
                "VALIDITY_DAY": "DAY"
            },
            "Exchange_Segments": {
                "EXCHANGE_NSECM": "NSECM",
                "EXCHANGE_NSEFO": "NSEFO",
                "EXCHANGE_NSECD": "NSECD",
                "EXCHANGE_MCXFO": "MCXFO",
                "EXCHANGE_BSECM": "BSECM"
            }
        }
