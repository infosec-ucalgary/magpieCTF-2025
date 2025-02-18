CC = gcc
LDFLAGS = -lm
SRC_DIR = .
DIST_DIR = ../dist
SRC = black_market.c
OBJ = $(SRC:.c=.o)
TARGET = $(DIST_DIR)/black_market

all: $(TARGET)

$(DIST_DIR):
	mkdir -p $(DIST_DIR)

$(TARGET): $(OBJ) | $(DIST_DIR)
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)
	upx $(TARGET)
	sha1sum $(TARGET) > $(TARGET).sha1.sig

black_market.o: black_market.c
	$(CC) -c $< -o $@ $(LDFLAGS)

clean:
	rm -rf *.o $(DIST_DIR)

.PHONY: all clean
