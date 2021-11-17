# -*- MakeFile -*-

# sudo apt-get install libboost-dev
# sudo apt-get install libboost-python-dev
# sudo apt-get install libboost-numpy-dev
# 			OR
# sudo apt-get install libboost-all-dev

CC = g++

SRC_DIR := ../src
OBJ_DIR = ./obj

CFLAGS = -std=c++11 -fPIC -shared -Wall -Wextra -g -w
PYTHONLIB = `python3.8-config --includes --libs`
BOOSTLIBS = -lboost_python38 -lboost_numpy38

include $(SRC_DIR)/Makefile
OBJECTS = $(targets:.cpp=.o)
OBJECTFILES = $(patsubst %.o, $(OBJ_DIR)/%.o, $(notdir $(OBJECTS)))

#$(info $(OBJECTS))

covidsim: $(SRC_DIR)/covidsim.cpp $(OBJECTS)
	$(CC) $< -o $@.so $(OBJECTFILES) $(CFLAGS) $(PYTHONLIB) $(BOOSTLIBS)

$(OBJECTS): %.o: $(SRC_DIR)/%.cpp
	$(CC) -c $(CFLAGS) $(PYTHONLIB) $(BOOSTLIBS) $< -o $(OBJ_DIR)/$(notdir $@)
