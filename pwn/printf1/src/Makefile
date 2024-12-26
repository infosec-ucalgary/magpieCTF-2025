.PHONY: all

FLAGS		:= -Wl,-z,relro,-z,now -fstack-protector-all
DEBUG_FLAGS := $(FLAGS) -ggdb3 -g

all: challenge
debug:
	gcc $(DEBUG_FLAGS) chal.c -o printf1

clean:
	rm printf1

challenge: chal.c
	gcc $(FLAGS) chal.c -o printf1
