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

// vulnerable! the hacker has arbitrary read access
void __attribute__((noreturn)) vuln() {
    // stack vars
    char buffer[FLAG_SIZE];
    unsigned long long loc = 0;

    puts("-- netrunnerware bot v1.2 --");

    // for the plot
    strncpy(buffer, "vasvygengvba_cynaarq_njnvgvat_pbasvezngvba",
            FLAG_SIZE); // says infiltration_planned_awaiting_confirmation

    // -- exploit --
    printf("Any commands? ");
    fgets(buffer, FLAG_SIZE - 1, stdin);
    printf("Roger, preparing to execute: ");
    printf(buffer); // vulnerable!

    printf("Where do I start? ");
    fscanf(stdin, "%lld", &loc);
    getchar();
    memcpy(buffer, (void *)loc, FLAG_SIZE - 1);
    buffer[FLAG_SIZE - 1] = 0;

    // potentially printing out the flag
    printf("Finished command: %s\n", buffer);

    // preventing ret2libc
    exit(0);
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // read flag into a buffer
    read_flag(flag_buffer);

    // for flare
    char ip[32];
    snprintf(ip, 32, "%d.%d.%d.%d", rand() % 256, rand() % 256, rand() % 256,
             rand() % 256);
    ssh_login("netgear1", "j@k3", ip, IP_JAKE);

    // -- exploit --
    vuln();

    return 0;
}
