#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BUFFER_SIZE 0x40
#define READ_SIZE (BUFFER_SIZE * 4)

#define USERNAME "n1k0th3gr3@t"
#define PASSWORD "cr1st1n@scks"

void gift() {
    asm("pop %rdi");
    asm("ret");
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // -- exploit --
    char buffer[BUFFER_SIZE];

    // -- exploit --
    puts("-- N1k0's PC --");

    // get the username
    printf("Username: ");
    fgets(buffer, READ_SIZE, stdin);

    // check the username
    if (strncmp(buffer, USERNAME, strlen(USERNAME)) != 0) {
        puts("Nice try!");
        exit(-1);
    }

    // get the password
    printf("Welcome %s, enter your password: ", buffer);
    fgets(buffer, READ_SIZE, stdin);

    // check the password
    if (strncmp(buffer, PASSWORD, strlen(PASSWORD)) != 0) {
        puts("Nice try!");
        exit(-1);
    }

    puts("You'll have to try harder than that, NYPD!");

    return 0;
}
