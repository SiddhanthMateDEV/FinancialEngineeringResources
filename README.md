
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

---
## Authors

- [@SiddhanthMateDEV](https://www.github.com/SiddhanthMateDEV)
---

# Financial Engineering Resources

This repository is a comprehensive collection of study materials and tools focused on Financial Engineering. It is structured to support both learning and practical application across key areas such as Finance, Probability & Statistics, and Programming.

The materials are organized by topics, with each section containing curated resources, including books, lecture notes, research papers, and problem sets. These resources are designed to build a strong foundation and advance your knowledge in Financial Engineering.

In addition to theoretical knowledge, this repository also offers practical support in Python, C++, and other programming languages. It includes a variety of functions and utilities that are essential for financial engineering tasks, such as:

- **Data Reading and Processing**
- **Option Pricing Methods**
- **Straddle Calculation and Analysis**
- **Strangle Calculation and Analysis**
- **Time-Based Filtering Functions**
- **Trading Strategies Implementation**

This repository serves as a valuable resource for anyone looking to deepen their understanding of Financial Engineering or to apply these concepts in real-world scenarios.

---

## Formulas/BackTesting Code

### C++ Framework: (Low Latency/HFT applications)

#### Directory Structure

This directory contains various C++  header and overloading functions related to low latency data gathering, storing, application, options calculations, and economic analysis. Below is an outline of the directory structure along with a brief description of each component.

Some components or documentation has not been added but will be in the coming weeks.

```

cpp/
├── CSVReader/
│   ├── main.cpp
│   └── main.h
│
├── main/
│   ├── main.cpp
│
├── straddle/
│   ├── main.cpp
│   └── main.h
│
├── InstrumentStruct/
│   ├── OptionStruct.h
│   └── StockStruct.h
│
├── strangle/
│   ├── main.cpp
│   └── main.h
│
├── ThreadMongoDB/    │   ├── thread_mongodb.cpp
│   └── thread_mongodb.h
│
└── timefuncs/
    ├── main.cpp
    └── main.h
```



#### Descriptions: 

- [**The CSV Reader Directory**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/cpp/CSVReader/main.h)
##### This folder contains the header file for the functionality which will be overloaded by the main.cpp in the same sub-directory:

This includes the `CSVReader` class, which provides methods to read and parse CSV files containing either stock or option data. The `CSVReader` class has two methods:

- `EquityFileReader`: Reads and parses stock data from a CSV file.
- `OptionsFileReader`: Reads and parses option data from a CSV file.

The header file also includes necessary library imports and a macro to set the seconds in the datetime field to `00` if not already set.

- [**The Instrument Structure Directory**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/cpp/InstrumentStruct)
##### This folder contains the header files which holds the structures of how Options Data and Equity Data

`StockStruct.h` contains the structure for holding equity data.
```cpp
struct StockData{
    std::string date;
    std::string time;
    double open;
    double high;
    double low;
    double close;
    long int volume;
    std::string ticker;
    std::tm datetime; 
};
```

`OptionStruct.h` contains the structure for holding option data.

```cpp
struct OptionData{
    std::string ticker;
    std::string date;
    std::string time;
    double open;
    double high;
    double low;
    double close;
    long int volume;
    long int openInterest;
    std::tm datetime;
};
```


### Python Framework: (LFT/MFT applications)

#### Directory Structure

This directory contains various Python modules and packages related to low-frequency trading strategies, options calculations, and economic analysis. Below is an outline of the directory structure along with a brief description of each component.

```
LowFrequency/
│
├── Depreciation/
│   └── main.py
│
├── Economic/
│   └── main.py
│
├── options/
│   ├── optionsFormulas/
│   │   └── main.py
│   └── readFileData/
│       └── main.py
│
├── straddle/
│   └── main.py
│
├── strangle/
│   └── main.py
│
├── timeFuncs/
│   └── main.py
│
├── utils/
│
└── venv/
```

#### Descriptions:

- [**Depreciation**:](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/python/options/Depreciation/main.py)
  
  This module handles calculations related to asset depreciation. It provides various methods to calculate the depreciation of different assets over time, taking into account factors such as the asset's initial value, useful life, and residual value.


- [**Economic**:](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/python/LowFrequency)
  
  This module includes economic analysis functions and calculations. It contains methods for analyzing economic indicators, forecasting economic trends, and performing macroeconomic simulations.


- **options**:
  
  - [**optionsFormulas**:](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/python/options)
    
    This module provides functions for various options pricing formulas. It includes implementations of the Black-Scholes model, binomial options pricing, and other advanced options pricing techniques.


    - **readFileData**: 
      
      This module includes functions for reading and parsing options data files. It provides utilities to load data from CSV files, perform data cleaning, and prepare the data for analysis and modeling.


    - **straddle**:
    
      This module implements strategies and calculations for straddle options trading. It includes methods to evaluate the profitability of straddle positions, calculate break-even points, and analyze risk.


    - **strangle**: 
      
      This module implements strategies and calculations for strangle options trading. It includes methods to evaluate the profitability of strangle positions, calculate break-even points, and analyze risk.


    - **timeFuncs**: 
    
      This module provides functions related to time-based calculations and utilities. It includes methods to handle time series data, perform time-based aggregations, and manage date and time conversions.


    - **utils**:
      
      This directory contains utility functions that are used across various modules. It includes general-purpose functions for data manipulation, logging, configuration management, and other common tasks.

    - **venv**:
      
      This directory contains the virtual environment for the project, ensuring that dependencies are managed and isolated. It is essential for maintaining consistent development environments and avoiding conflicts between package versions.

---

## Trading Infrastructure:

### India:

#### Python Market Data API Code Reference for XTS By TT Blaze API:

#### Directory Structure:

This repository contains the implementation of the TT Blaze Market Data API using Python. The API provides real-time stock market data, instrument subscriptions, market depth events, candle data, open interest events, and more. This code is meant for Low/Mid Frequency Trading Infrastructure.

```
TradingInfrastructure/
└── India/
    └── MarketData/
        └── XTS_TT_BLAZE/
            └── Python/
                ├── config/
                ├── data/
                ├── database_operations/
                ├── login/
                ├── market_data_api/
                ├── subscribe/
                ├── web_socket/
                └── xts_message_codes/

```
#### The Documentation:
- [XTS Documentation By TT Blaze API](https://ttblaze.iifl.com/doc/marketdata/)

#### `config`: Contains the two folders one for the config of products distributed by xts and the other is routes, which contains the paths for getting different api related backend functionality.
- [**Config Routes**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/config)

#### `login`: Manages host look up and login to obtain authetication token and the token for each session.
- [**Login Code**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/login)

#### `market_data_api`: Provides example usage of the Market Data functionalities.
- [**Market Data API Functions**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/market_data_api)

#### `subscribe`: This contains a list of dictionaries of the exchange segment and instrument of id for whose id data will be subscribed.
- [**Subscribe Payload**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/subscribe)

#### `web_socket`: Initializes the websocket instance to listen for data packets.
- [**WebSocket Instance**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/web_socket)

#### `xts_message_codes`: Contains a list of all the codes of xts market data events.
- [**XTS Message Codes**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/Python/xts_message_codes)

#### C++ Market Data API Code Reference for XTS By TT Blaze API:

#### Directory Structure:

This repository contains the implementation of the TT Blaze Market Data API using C++. The API provides real-time stock market data, instrument subscriptions, market depth events, candle data, open interest events, and more. This code is meant for High Frequency Trading Infrastructure.

Still being made!

```
TradingInfrastructure/
└── India/
    └── MarketData/
        └── XTS_TT_BLAZE/
            └── C++/
                ├── config/
                ├── data/
                ├── database_operations/
                ├── login/
                ├── market_data_api/
                ├── subscribe/
                ├── web_socket/
                └── xts_message_codes/
```
#### The Documentation:
- [XTS Documentation By TT Blaze API](https://ttblaze.iifl.com/doc/marketdata/)

#### `config`: Contains the two folders one for the config of products distributed by xts and the other is routes, which contains the paths for getting different api related backend functionality.
- [**Config Routes**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/config)

#### `login`: Manages host look up and login to obtain authetication token and the token for each session.
- [**Login Code**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/login)

#### `market_data_api`: Provides example usage of the Market Data functionalities.
- [**Market Data API Functions**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/market_data_api)

#### `subscribe`: This contains a list of dictionaries of the exchange segment and instrument of id for whose id data will be subscribed.
- [**Subscribe Payload**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/subscribe)

#### `web_socket`: Initializes the websocket instance to listen for data packets.
- [**WebSocket Instance**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/web_socket)

#### `xts_message_codes`: Contains a list of all the codes of xts market data events.
- [**XTS Message Codes**](https://github.com/SiddhanthMateDEV/FinancialEngineeringResources/tree/main/TradingInfrastructure/India/MarketData/XTS_TT_BLAZE/C++/xts_message_codes)

---
## Acknowledgements

I just want to extend my heartfelt thanks to everyone who has supported me on this journey. I haven’t logged as many hours as some in the quant world, but the experience I've gained has been invaluable in building this repository. Here's why I put this together:

- I get it—learning to be a quant is tough, and while I'm not claiming to be the best, I'm committed to continuing this journey and sharing what I know.

- Starting out can feel overwhelming with questions like "Where do I even begin?" or "What do I need to know?" or "Which project should I tackle first?" These were the exact questions that stumped me initially. My hope is that this repository can help answer those questions. If the feedback is positive, I’m thinking of starting a Discord channel to offer more personalized help on weekends or whenever I can.

---

## Appendix



### Finance

#### Books
- **(Springer Finance) Damiano Brigo, Fabio Mercurio** - *Interest Rate Models - Theory and Practice_With Smile, Inflation and Credit* - Springer (2006)
- **(Springer Finance) Steven E. Shreve** - *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model* - Springer (2005)
- **John C. Hull** - *Options, Futures, and Other Derivatives* - Pearson Education (2008)
- **Steven E. Shreve** - *Stochastic Calculus for Finance II: Continuous-Time Models (Springer Finance) (v. 2)* - Springer (2004)
- **Martin Baxter** - *Financial Calculus: An Introduction to Derivative Pricing* - Cambridge University Press (1996)
- **Mark S. Joshi** - *The Concepts and Practice of Mathematical Finance* - Cambridge University Press (2008)
- **Damien Lamberton and Bernard Lapeyre** - *Introduction to Stochastic Calculus Applied to Finance* -  Chapman and Hall/CRC (2007)
- **Tomas Björk** - *Arbitrage Theory in Continuous Time* - Oxford University Press (2009)
- **Rama Cont, Peter Tankov** - *Financial Modelling with Jump Processes* - CRC Press (2010)
- **René Carmona and Michael Tehranchi** - *Interest Rate Models: An Infinite Dimensional Stochastic Analysis Perspective* - Springer (2006)
- **Robert Jarrow** - *Modeling Fixed-Income Securities and Interest Rate Options* - Stanford University Press (2002)
- **Guojun Gan, Chaoqun Ma, and Hong Xie** - *Measure, Probability, and Mathematical Finance: A Problem-Oriented Approach* - Wiley
- **Paul Wilmott, Sam Howison, and Jeff Dewynne** - *The Mathematics of Financial Derivatives: A Student Introduction* - Cambridge University Press (1995)


#### Lectures
- [Derivatives Markets](https://www.lse.ac.uk/resources/calendar2013-2014/courseGuides/FM/2013_FM320.htm) by the London School of Economics: Comprehensive notes on futures, options, and the Black-Scholes model.
- [Options and Derivatives Pricing](https://web.stanford.edu/class/msande348/3480/Assets/Lecture10.pdf) by Stanford University: Notes on pricing techniques, hedging strategies, and risk management.


### Probability & Statistics

#### Books
- **(Springer Series in Statistics) Larry Wasserman** - *All of Statistics: A Concise Course in Statistical Inference* - Springer (2004)
- **(Springer Texts in Statistics) Rick Durrett** - *Probability: Theory and Examples* - Cambridge University Press (2019)
- **David Williams** - *Probability with Martingales* - Cambridge University Press (1991)
- **(Springer Series in Statistics) Peter J. Bickel, Kjell A. Doksum** - *Mathematical Statistics: Basic Ideas and Selected Topics, Volume I* - CRC Press (2015)
- **(Springer Texts in Statistics) A. N. Shiryaev** - *Probability-1* - Springer (2016)
- **(Springer Texts in Statistics) Sheldon M. Ross** - *Introduction to Probability Models* - Academic Press (2019)
- **(Springer Texts in Statistics) Rick Durrett** - *Essentials of Stochastic Processes* - Springer (2016)
- **(Springer Series in Statistics) Jeff Rosenthal** - *A First Look at Rigorous Probability Theory* - World Scientific (2006)
- **(Springer Series in Statistics) Kai Lai Chung** - *A Course in Probability Theory* - Academic Press (2000)
- **(Springer Texts in Statistics) David Freedman** - *Statistical Models: Theory and Practice* - Cambridge University Press (2009)
- **(Springer Series in Statistics) Joseph K. Blitzstein, Jessica Hwang** - *Introduction to Probability* - CRC Press (2014)
- **(Springer Texts in Statistics) Jun Shao** - *Mathematical Statistics* - Springer (2003)

#### Problems
- [(MIT OpenCourseWare) **Prof. John Tsitsiklis - Introduction to Probability** - Massachusetts Institute of Technology](https://ocw.mit.edu/courses/res-6-012-introduction-to-probability-spring-2018/)
- [(Yale University) **Prof. Joseph Chang - Stochastic Processes - Yale University**](http://www.stat.yale.edu/~pollard/Courses/251.spring2013/Handouts/Chang-notes.pdf)
- [(Harvard University) **Prof. Joe Blitzstein - Statistics 110: Probability - Harvard University**](https://projects.iq.harvard.edu/stat110/strategic-practice-problems)
- [(MIT) **Graph Theory And Additive Combinatorics MIT18_217F19**](https://ocw.mit.edu/courses/18-225-graph-theory-and-additive-combinatorics-fall-2023/pages/problem-sets/)


### Programming

#### Books

### C Programming

#### Books
- **(The Wiley Finance Series) Daniel J. Duffy** - *Financial Instrument Pricing Using C* - Wiley (2004)
- **K. N. King** - *C Programming: A Modern Approach* - W. W. Norton & Company (2008)

### C++ Programming

#### Books
- **Daniel J. Duffy** - *Financial Instrument Pricing Using C++* - Wiley (2004)
- **Mark S. Joshi** - *C++ Design Patterns and Derivatives Pricing* - Cambridge University Press (2004)
- **Robert R. Reitano** - *Quantitative Finance: An Object-Oriented Approach in C++* - MIT Press (2010)
- **K. Choudhry and M. Rodriguez** - *Financial Modelling: Theory, Implementation and Practice with MATLAB Source* - John Wiley & Sons (2010)
- **John C. Hull** - *Options, Futures, and Other Derivatives* - Pearson (2008) *(includes C++ code)*
- **John Armstrong** - *C++ for Financial Mathematics* - Cambridge University Press (2021)
- **Les Clewlow and Chris Strickland** - *Implementing Derivative Models* - John Wiley & Sons (1998)
- **Daniel J. Duffy** - *Introduction to C++ for Financial Engineers: An Object-Oriented Approach* - Wiley (2006)
- **Paolo Brandimarte** - *Numerical Methods in Finance and Economics: A MATLAB-Based Introduction* - Wiley (2006) *(includes C++ code examples)*
- **Alexander J. McNeil** - *Financial Engineering with C++* - Princeton University Press (2022)
- **(Chapman and Hall/CRC Financial Mathematics Series) Schlogl, Erik** - *Quantitative Finance: An Object-Oriented Approach in C++* - CRC Press (2013)
- **Stanley B. Lippman, Josée Lajoie, and Barbara E. Moo** - *C++ Primer (5th Edition)* - Addison-Wesley (2013)
- **CARLOS OLIVEIRA** - *Options and Derivatives Programming in C++: Algorithms and Programming Techniques for the Financial Industry* - Apress (2016)
- **Cornelis W. Oosterlee, Lech A. Grzelak** - *Mathematical Modeling and Computational Finance: With Exercises and Python and MATLAB Computer Codes* - World Scientific Publishing Europe Limited (2019)

### Python Programming

#### Books

- **Yves Hilpisch** - *Python for Finance: Mastering Data-Driven Finance* - O'Reilly Media (2018)
- **Mark J. Bennett, Dirk L. Hugen** - *Financial Analytics with R and Python* - Cambridge University Press (2016)
- **Yves Hilpisch** - *Python for Algorithmic Trading: From Idea to Cloud Deployment* - O'Reilly Media (2020)
- **Eryk Lewinson** - *Python for Finance Cookbook: Over 50 Recipes for Applying Modern Python Libraries to Financial Data Analysis* - Packt Publishing (2020)
- **Ed Roberts** - *Introduction to Financial Python* - Independently Published (2020)
- **Shayne Fletcher, Christopher Gardner** - *Financial Modelling in Python* - Wiley (2009)
- **Yves Hilpisch** - *Python for Finance: Analyze Big Financial Data* - O'Reilly Media (2014)
- **Yves Hilpisch** - *Python for Finance: Develop and Deploy Financial Applications* - O'Reilly Media (2022)
- **Eryk Lewinson** - *Python Quantitative Finance* - Packt Publishing (2020)
- **Chris Kelliher** - *Quantitative Finance with Python: A Practical Guide for Investment Professionals* - Springer (2022)
- **Marcos López de Prado** - *Machine Learning for Asset Managers* - Cambridge University Press (2020)
- **Ernest Chan** - *Algorithmic Trading and Quantitative Strategies* - Independently Published (2021)


### Research Papers (Still need to site them hence saving the links)

- [**(Black, F. and Scholes, M. (1973)) The Pricing of Options and Corporate Liabilities. Journal of Political Economy, 81(3), pp.637–654.**](https://www.sfu.ca/~kkasa/BlackScholes_73.pdf)
- [**Theory Of Rational Option Pricing**](https://www.maths.tcd.ie/~dmcgowan/Merton.pdf)
- [**(Markowitz, H. (1952)) Portfolio Selection. The Journal of Finance, 7(1).**](https://www.jstor.org/stable/2975974)
- [**(Edwards, S. (1985)) NBER WORKING PAPER SERIES THE PRICING OF BONDS AND BANK LOANS IN INTERNATIONAL MARKETS: AN EMPIRICAL ANALYSIS OF DEVELOPING COUNTRIES’ FOREIGN BORROWING.**](https://www.nber.org/system/files/working_papers/w1689/w1689.pdf)
- [**(2017). Efficient Capital Markets: A Review of Theory and Empirical Work**](https://www.google.com/search?q=Efficient+Capital+Markets%3A+A+Review+of+Theory+and+Empirical+Work&rlz=1C5CHFA_enIN1117IN1117&oq=Efficient+Capital+Markets%3A+A+Review+of+Theory+and+Empirical+Work&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBBzU2MWowajSoAgCwAgE&sourceid=chrome&ie=UTF-8)

### Other Resources

#### YouTube

- QuantConnect
- QuantInsti
- Mark Meldrum

---

## 🔗 My Links:
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/siddhanth-mate-9b0127222/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/SiddhanthMate)
