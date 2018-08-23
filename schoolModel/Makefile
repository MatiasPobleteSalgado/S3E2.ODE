OBJS = main.cu
CC = nvcc

#COMPILER_FLAGS = -w -std=c++0x

INCLUDE_FLAGS = -I/src
LINKER_FLAGS = -lSDL2 -lSDL2main

OBJ_NAME = exec

all : $(OBJS)
	$(CC) $(OBJS) $(COMPILER_FLAGS) $(INCLUDE_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)
