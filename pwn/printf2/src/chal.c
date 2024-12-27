#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

// default location for program to read flag into
char flag_buffer[FLAG_SIZE];

void read_flag(char *buffer) {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(1);
    }

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
}

void vuln() {
    // stack vars
    char buffer[BUFFER_SIZE];
    unsigned long *loc = NULL;

    puts("Now the flag isn't on the stack! Good luck dealing with ASLR!");

    // -- exploit --
    printf("Say something better this time: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    printf("You said: ");
    printf(buffer);

    printf("Where do you want to read from? ");
    fscanf(stdin, "%ld", loc);
    getchar();
    memcpy(buffer, loc, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = 0;

    printf("I bet this isn't very interesting: %s\n", buffer);
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // read flag into a buffer
    read_flag(flag_buffer);

    // -- exploit --
    vuln();

    return 0;
}
