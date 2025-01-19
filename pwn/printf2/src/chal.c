#include "./common.h"
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define BUFFER_SIZE 0x100

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

void vuln() {
    // stack vars
    char buffer[BUFFER_SIZE];
    char *flag_ptr = flag_buffer;

    // main loop
    while (true) {
        int choice = -1;

        // asking for a choice
        printf("n1k0@netgear2 $ ");
        fscanf(stdin, "%d", &choice);
        getchar(); // this consumes the space, or else this program becomes
                   // impossible

        switch (choice) {
        case 1:
            // exploit goes here
            printf("write> ");
            read(0, buffer,
                 BUFFER_SIZE - 1); // can't be fgets because fgets doesn't read
                                   // past nullbytes apparently
            printf("written> ");
            printf(buffer); // vulnerable!
            break;
        case 2:
            // read flag into buffer
            read_flag(flag_ptr);
            break;
        default:
            puts("unw3lc0m3");
            exit(ERR_CHALLENGE_FAILURE);
        }
    }
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
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
    sleep(2);
    printf("Linux netgear2 6.1.21-v8+ #1642 SMP PREEMPT %s aarch64\n",
           time_buffer);

    vuln();

    return 0;
}
