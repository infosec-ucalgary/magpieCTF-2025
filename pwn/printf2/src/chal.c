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

void vuln() {
    // stack vars
    char buffer[BUFFER_SIZE];
    char *flag_ptr = 0;

    // for the plot
    strncpy(buffer, "xelcgb_vf_tbar", FLAG_SIZE); // says krypto_is_gone

    // main loop
    while (true) {
        int choice = -1;

        // asking for a choice
        printf("j@k3@netgear2 $ ");
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

    // for flare
    char ip[32];
    snprintf(ip, 32, "%d.%d.%d.%d", rand() % 256, rand() % 256, rand() % 256,
             rand() % 256);
    ssh_login("netgear2", "j@k3", ip, IP_JAKE);

    // -- exploit --
    vuln();

    return 0;
}
