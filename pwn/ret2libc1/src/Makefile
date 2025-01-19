include ./flags.mk
.PHONY: all clean

DIST_DIR	:= dist
PROG		:= ret2libc1
GLOBAL_FLAGS:= $(FLAGS) -w
DEBUG_FLAGS := $(FLAGS) -ggdb3 -g -Wl,-rpath="$(PWD)/../../" \
				 -Wl,--dynamic-linker="$(PWD)/../../ld-linux-x86-64.so.2"

# main build target
all: challenge

DIST_DIR:
	mkdir -p "$(PWD)/../../$(DIST_DIR)/"

debug: chal.c | DIST_DIR
	gcc -w $(GLOBAL_FLAGS) chal.c -o "$(PWD)/../../$(DIST_DIR)/ret2libc1"
	gcc -w $(DEBUG_FLAGS) chal.c -o ret2libc1

challenge: chal.c | DIST_DIR
	gcc -w $(GLOBAL_FLAGS) chal.c -o ret2libc1

clean:
	rm ret2libc1*
