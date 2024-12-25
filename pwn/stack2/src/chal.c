#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

// default location for program to read flag into
char flag_buffer[FLAG_SIZE];

void check_flag() {
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag isn't found, contact the CTF organizers.");
        exit(1);
    }
    fclose(fd);
}

void read_flag(char *buffer) {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    assert(fd != NULL);

    // read flag into buffer
    fread(buffer, FLAG_SIZE, 1, fd);
    fclose(fd);
}

int main() {
    // ensuring that the flag is there
    check_flag();

    // setup
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    // stack vars
    char buffer[BUFFER_SIZE];
    char *flag_ptr = flag_buffer;

    // main loop
    while (true) {
        // exploit goes here
        printf("Say something: ");
        fgets(buffer, BUFFER_SIZE, stdin);
        printf("You said: ");
        printf(buffer);

        // read flag into buffer
        read_flag(flag_ptr);
    }
}
