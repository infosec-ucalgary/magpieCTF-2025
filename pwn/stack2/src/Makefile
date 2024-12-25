.PHONY: all

FLAGS		:= -Wl,-z,relro,-z,now -fstack-protector-all
DEBUG_FLAGS := $(FLAGS) -ggdb3 -g

all: stack2
debug:
	gcc $(DEBUG_FLAGS) chal.c -o ../solve/stack2 

clean:
	rm stack2

stack2: chal.c
	gcc $(FLAGS) chal.c -o stack2
