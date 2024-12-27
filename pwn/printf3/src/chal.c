#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

// default location for program to read flag into
char flag_buffer[FLAG_SIZE];

void check_flag() {
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(1);
    }
    fclose(fd);
}

void read_flag(char *buffer) {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    assert(fd != NULL);

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
}

int main() {
    // ensuring that the flag is there
    check_flag();

    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // stack vars
    char buffer[BUFFER_SIZE];
    char *flag_ptr = flag_buffer;
    char *flag_ptr_ptr = flag_ptr;

    // main loop
    while (true) {
        int choice = -1;

        // asking for a choice
        puts("-- printf3 --");
        puts("1) say something");
        puts("2) read the flag");
        printf("> ");
        fscanf(stdin, "%d", &choice);
        getchar(); // this consumes the space, or else this program becomes
                   // impossible

        switch (choice) {
        case 1:
            // exploit goes here
            printf("Say something: ");
            read(0, buffer,
                 BUFFER_SIZE - 1); // can't be fgets because fgets doesn't read
                                   // past nullbytes apparently
            printf("You said: ");
            printf(buffer);
            break;
        case 2:
            // read flag into buffer
            read_flag(flag_ptr);
            break;
        default:
            puts("You seem like a dirty hacker!");
            exit(1);
        }
    }

    return 0;
}
