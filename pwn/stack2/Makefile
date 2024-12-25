.PHONY: all

all: stack2
debug:
	gcc -ggdb3 -g -Wl,-z,relro,-z,now -o stack2 -fstack-protector-all chal.c

clean:
	rm stack2

stack2: chal.c
	gcc -Wl,-z,relro,-z,now -o stack2 -fstack-protector-all chal.c
