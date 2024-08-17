CXX = g++
CXXFLAGS = -std=c++11 -I/opt/homebrew/include
LDFLAGS = -L/opt/homebrew/lib -ljsoncpp -lcurl
SOURCES = ../../ReadConfig/main.cpp test.cpp
TARGET = test

all: $(TARGET)

$(TARGET):$(SOURCES)
	$(CXX) $(CXXFLAGS) $(LDFFLAGS) -o $(TARGET) $(SOURCES) 

clean:
	rm -f $(TARGET)


