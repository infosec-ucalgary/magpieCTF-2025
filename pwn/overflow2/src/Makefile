include ./flags.mk
.PHONY: all clean

DIST_DIR	:= dist
PROG		:= overflow2
GLOBAL_FLAGS:= $(FLAGS) -w
DEBUG_FLAGS := $(FLAGS) -ggdb3 -g -Wl,-rpath="$(PWD)/../../" \
				 -Wl,--dynamic-linker="$(PWD)/../../ld-linux-x86-64.so.2"

# main build target
all: challenge

DIST_DIR:
	mkdir -p "$(PWD)/../../$(DIST_DIR)/"

debug: chal.c | DIST_DIR
	gcc -w $(GLOBAL_FLAGS) chal.c -o "$(PWD)/../../$(DIST_DIR)/overflow2"
	gcc -w $(DEBUG_FLAGS) chal.c -o overflow2

challenge: chal.c | DIST_DIR
	gcc -w $(GLOBAL_FLAGS) chal.c -o overflow2

clean:
	rm overflow2*
