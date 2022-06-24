#Makefile for iverilog target

PROJ=stsearchMulti

# Change this directory to verilog
IVERILOG_DIR = /home/ziyue/researchlib/iverilog
IVERILOG_LIB = $(IVERILOG_DIR)/lib/ivl
IVERILOG_INC = $(IVERILOG_DIR)/include/iverilog

TARGET=$(IVERILOG_LIB)/$(PROJ).tgt
CONFIG_FILE=$(PROJ).conf $(PROJ)-s.conf
CONFIG_TARGET=$(IVERILOG_LIB)/$(PROJ).conf $(IVERILOG_LIB)/$(PROJ)-s.conf

# $(patsubst pattern,replacement,text): OBJECTS is replace all [xx].cpp to [xx].o
OBJECTS=$(patsubst %.cpp, %.o, $(wildcard *.cpp))
# $(wildcard pattern…): collect all ".h" file from the path of ../include/
HEADERS=$(wildcard ../include/*.h)

# force executing
.PHONY: all clean

all: $(TARGET) $(CONFIG_TARGET)

clean:
	@rm -rf *.o
	@rm -rf $(TARGET)

# simple format:
# target … : prerequisites …
#        recipe
#        …
#        …
# @ disables printing the command line being executed. 
# $@ is the name of the target(See format abovs) being generated, and $< the first prerequisite (usually a source file).
%.o: %.cpp	$(HEADERS)
	@g++ -Wall -ggdb3 -std=c++11 -c $< -o $@ -I../include/ -I$(IVERILOG_INC) -I$(IVERILOG_DIR) -fpic 
	@echo "Compiling $<..."

$(TARGET): $(OBJECTS)
	@g++ $(OBJECTS) -Wall -ggdb3 -o $@ -std=c++11 -fpic -shared -lyices 
	@echo "Linking..."

$(CONFIG_TARGET): $(CONFIG_FILE)
	cp -f $(CONFIG_FILE) -t $(IVERILOG_LIB)
	@echo "Copying config file..."

# Appeared parameters for g++
# -Wall: It's short for "warn all" -- it turns on (almost) all the warnings that g++ can tell you about.
# -ggdb3: produces extra debugging information, for example: including macro definitions. 
# -o: output file
# -Idir: include directory
# -fpic: https://www.cnblogs.com/cswuyg/p/3830703.html