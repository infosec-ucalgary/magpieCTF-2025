include ./flags.mk
.PHONY: all clean

PROG		:= printf1
GLOBAL_FLAGS:= $(FLAGS) -w
DEBUG_FLAGS := $(GLOBAL_FLAGS) -ggdb3 -g -Wl,-rpath="$(PWD)/../../" \
				 -Wl,--dynamic-linker="$(PWD)/../../ld-linux-x86-64.so.2"

# main build target
all: main

dist: chal.c # for the docker container
	gcc $(GLOBAL_FLAGS) -o $(PROG) $<

main: chal.c
	gcc $(GLOBAL_FLAGS) -o $(PROG) $<
	gcc $(DEBUG_FLAGS) -o $(PROG).debug $<

clean:
	rm $(PROG)*
