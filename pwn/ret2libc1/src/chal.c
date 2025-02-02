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

#define USERNAME "j@k3th3gr3@t"
#define PASSWORD "inn0c3nc3"

void gift() {
    asm("pop %rdi");
    asm("ret");
}

// vulnerable!
void vuln() {
    char buffer[BUFFER_SIZE] = {0};
    puts("-- j@k3's PC --");

    // get the username
    printf("Username: ");
    read(0, buffer, READ_SIZE); // vulnerable! read size is greater than the buffer size

    // check the username
    if (strncmp(buffer, USERNAME, strlen(USERNAME)) != 0) {
        puts("Nice try!");
        exit(ERR_CHALLENGE_FAILURE);
    }

    // get the password
    printf("Welcome %s, enter your password: ", buffer);
    read(0, buffer, READ_SIZE); // vulnerable! read size is greater than the buffer size

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

    // some flare
    ssh_login("netrunner1", "j@k3", "52.129.50.30", IP_CORS);

    // -- exploit --
    vuln();

    return 0;
}
