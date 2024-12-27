include ./flags.mk
.PHONY: all

DEBUG_FLAGS := $(FLAGS) -ggdb3 -g

all: challenge
debug:
	gcc $(DEBUG_FLAGS) chal.c -o printf2

clean:
	rm printf2

challenge: chal.c
	gcc $(FLAGS) chal.c -o printf2
