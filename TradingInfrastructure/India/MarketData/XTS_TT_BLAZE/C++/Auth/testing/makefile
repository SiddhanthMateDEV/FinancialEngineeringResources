CXX = g++
CXXFLAGS = -std=c++11 -Wall -I/opt/homebrew/include 
LDFLAGS = -L/opt/homebrew/lib -ljsoncpp -lcurl
SOURCES = test.cpp ../main.cpp ../../ReadConfig/readini.cpp 
TARGET = test

all: $(TARGET)

$(TARGET):$(SOURCES)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(SOURCES) -o $(TARGET)

clean:
	rm -f $(TARGET)


