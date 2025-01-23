#include "./common.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define BUFFER_SIZE 0x20
#define READ_SIZE (BUFFER_SIZE * 8)

#define USERNAME "n1k0th3gr3@t"
#define PASSWORD "cr1st1n@scks"

void gift() {
    asm("pop %rdi");
    asm("ret");
}

// vulnerable!
void vuln() {
    char buffer[BUFFER_SIZE];
    puts("-- N1k0's PC --");

    // get the username
    printf("Username: ");
    read(stdin, buffer, READ_SIZE); // vulnerable! read size is greater than the buffer size

    // check the username
    if (strncmp(buffer, USERNAME, strlen(USERNAME)) != 0) {
        puts("Nice try!");
        exit(ERR_CHALLENGE_FAILURE);
    }

    // get the password
    printf("Welcome %s, enter your password: ", buffer);
    read(stdin, buffer, READ_SIZE); // vulnerable! read size is greater than the buffer size

    // check the password
    if (strncmp(buffer, PASSWORD, strlen(PASSWORD)) != 0) {
        puts("Nice try!");
        exit(ERR_CHALLENGE_FAILURE);
    }

    puts("You'll have to try harder than that, NYPD!");
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
    sleep(1);
    printf("Linux turnip 6.1.21-v8+ #1642 SMP PREEMPT %s aarch64\n",
           time_buffer);

    // -- exploit --
    vuln();

    return 0;
}
