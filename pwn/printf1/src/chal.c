#include "./common.h"
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define BUFFER_SIZE 0x60

// default location for program to read flag into
char flag_buffer[FLAG_SIZE];

void read_flag(char *buffer) {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(ERR_NO_FLAG);
    }

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
}

void __attribute__((noreturn)) vuln() {
    // stack vars
    char buffer[FLAG_SIZE];
    unsigned long long loc = 0;

    puts("N1k0 says: try and defeat ASLR hacker!");

    // -- exploit --
    printf("I'll let you say something: ");
    fgets(buffer, FLAG_SIZE - 1, stdin);
    printf("You said: ");
    printf(buffer); // vulnerable!

    printf("I bet you don't know where to read from? ");
    fscanf(stdin, "%lld", &loc);
    getchar();
    memcpy(buffer, (void *)loc, FLAG_SIZE - 1);
    buffer[FLAG_SIZE - 1] = 0;

    // potentially printing out the flag
    printf("I doubt this is interesting: %s\n", buffer);

    // preventing ret2libc
    exit(0);
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // read flag into a buffer
    read_flag(flag_buffer);

    srand(time(NULL));

    // time information
    char time_buffer[BUFFER_SIZE];
    time_t time_struct;
    time(&time_struct);
    strftime(time_buffer, BUFFER_SIZE, "%a %b %d %k:%M:%S %Z %Y",
             localtime(&time_struct));

    // some flare
    printf("ssh n1k0@%d.%d.%d.%d\n", rand() % 256, rand() % 256, rand() % 256,
           rand() % 256);
    sleep(1);
    printf("Linux netgear1 6.1.21-v8+ #1642 SMP PREEMPT %s aarch64\n",
           time_buffer);

    // -- exploit --
    vuln();

    return 0;
}
