include ./flags.mk
.PHONY: all clean

PROG		:= overflow2
GLOBAL_FLAGS:= $(FLAGS) -w
DEBUG_FLAGS := $(GLOBAL_FLAGS) -ggdb3 -g -Wl,-rpath="${MAKEROOT}" \
				 -Wl,--dynamic-linker="${MAKEROOT}/ld-linux-x86-64.so.2"

# main build target
all: main

main:
	gcc $(GLOBAL_FLAGS) -o $(PROG) chal.c common.c
	gcc $(DEBUG_FLAGS) -o $(PROG).debug chal.c common.c

clean:
	rm $(PROG)*
