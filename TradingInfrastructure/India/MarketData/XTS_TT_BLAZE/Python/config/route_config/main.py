class RouteConfig:
    def __init__(self):
        self._routes = {
            # Interactive API endpoints
            "interactive.prefix": "interactive",
            "user.login": "/interactive/user/session",
            "user.logout": "/interactive/user/session",
            "user.profile": "/interactive/user/profile",
            "user.balance": "/interactive/user/balance",

            # Orders 
            "orders": "/interactive/orders",
            "trades": "/interactive/orders/trades",
            "order.status": "/interactive/orders",
            "order.place": "/interactive/orders",
            
            # Order Handling
            "bracketorder.place": "/interactive/orders/bracket",
            "bracketorder.modify": "/interactive/orders/bracket",
            "bracketorder.cancel": "/interactive/orders/bracket",
            "order.place.cover": "/interactive/orders/cover",
            "order.exit.cover": "/interactive/orders/cover",
            "order.modify": "/interactive/orders",
            "order.cancel": "/interactive/orders",
            "order.cancelall": "/interactive/orders/cancelall",
            "order.history": "/interactive/orders",
            
            # Portfolio Handling
            "portfolio.positions": "/interactive/portfolio/positions",
            "portfolio.holdings": "/interactive/portfolio/holdings",
            "portfolio.positions.convert": "/interactive/portfolio/positions/convert",
            "portfolio.squareoff": "/interactive/portfolio/squareoff",
            "portfolio.dealerpositions": "interactive/portfolio/dealerpositions",
            "order.dealer.status": "/interactive/orders/dealerorderbook",
            "dealer.trades": "/interactive/orders/dealertradebook",
            
            # Marketdata API
            "marketdata.prefix": "apimarketdata",
            "market.login": "/apimarketdata/auth/login",
            "market.logout": "/apimarketdata/auth/logout",
            "market.config": "/apimarketdata/config/clientConfig",
            "market.instruments.master": "/apimarketdata/instruments/master",
            "market.instruments.subscription": "/apimarketdata/instruments/subscription",
            "market.instruments.unsubscription": "/apimarketdata/instruments/subscription",
            "market.instruments.ohlc": "/apimarketdata/instruments/ohlc",
            "market.instruments.indexlist": "/apimarketdata/instruments/indexlist",
            "market.instruments.quotes": "/apimarketdata/instruments/quotes",
            "market.search.instrumentsbyid": '/apimarketdata/search/instrumentsbyid',
            "market.search.instrumentsbystring": '/apimarketdata/search/instruments',
            "market.instruments.instrument.series": "/apimarketdata/instruments/instrument/series",
            "market.instruments.instrument.equitysymbol": "/apimarketdata/instruments/instrument/symbol",
            "market.instruments.instrument.futuresymbol": "/apimarketdata/instruments/instrument/futureSymbol",
            "market.instruments.instrument.optionsymbol": "/apimarketdata/instruments/instrument/optionsymbol",
            "market.instruments.instrument.optiontype": "/apimarketdata/instruments/instrument/optionType",
            "market.instruments.instrument.expirydate": "/apimarketdata/instruments/instrument/expiryDate"
        }