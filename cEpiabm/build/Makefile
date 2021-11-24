# -*- MakeFile -*-

# sudo apt-get install libboost-dev
# sudo apt-get install libboost-python-dev
# sudo apt-get install libboost-numpy-dev
# 			OR
# sudo apt-get install libboost-all-dev

CC = g++

SRC_DIR := ../src
OBJ_DIR = ./obj

CFLAGS = -std=c++17 -fPIC -shared -Wall -Wextra -w
#PYTHONLIB = `python3.8-config --includes --libs`
#PYBIND = `python3.8 -m pybind11 --includes`
#BOOSTLIBS = -lboost_python38 -lboost_numpy38

include $(SRC_DIR)/Makefile
OBJECTS = $(targets:.cpp=.o)
OBJECTFILES = $(patsubst %.o, $(OBJ_DIR)/%.o, $(notdir $(OBJECTS)))

#$(info $(OBJECTS))

test: $(SRC_DIR)/test.cpp $(OBJECTS)
	$(CC) $(SRC_DIR)/test.cpp -o test.exe $(OBJECTFILES) -std=c++17 -w

$(OBJECTS): %.o: $(SRC_DIR)/%.cpp
	$(CC) -c $(CFLAGS) $< -o $(OBJ_DIR)/$(notdir $@)
