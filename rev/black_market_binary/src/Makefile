CC = gcc
LDFLAGS = -lm
SRC_DIR = .
DIST_DIR = ../dist
SRC = black_market.c
OBJ = $(SRC:.c=.o)
TARGET = $(DIST_DIR)/black_market

all: $(TARGET)

$(TARGET): $(OBJ) 
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)
	upx $(TARGET)

black_market.o: black_market.c
	$(CC) -c $< -o $@ $(LDFLAGS)

clean:
	rm -f *.o 

.PHONY: all clean
