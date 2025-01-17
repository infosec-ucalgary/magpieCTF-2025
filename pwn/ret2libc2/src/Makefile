include ./flags.mk
.PHONY: all

DEBUG_FLAGS := $(FLAGS) -ggdb3 -g

all: challenge
debug:
	gcc $(DEBUG_FLAGS) chal.c -o ret2libc2 \
	-Wl,-rpath="$(PWD)/../../" -Wl,--dynamic-linker="$(PWD)/../../ld-linux-x86-64.so.2"

clean:
	rm ret2libc2

challenge: chal.c
	gcc $(FLAGS) chal.c -o ret2libc2
