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
        int choice = -1;

        // asking for a choice
        puts("-- Flag Emporium --");
        puts("1) say something");
        puts("2) read the flag");
        printf("> ");
        fscanf(stdin, "%d", &choice);

        /*
        Originally, there was no switch statement here and the two cases were merged together,
        the reason why this exists is because there was no possible exploit, because you simply
        couldn't change the flag_ptr because %n writes (at most) a short
        */

        switch (choice) {
        case 1:
            // exploit goes here
            printf("Say something: ");
            fgets(buffer, BUFFER_SIZE - 1, stdin);
            printf("You said: ");
            printf(buffer);
            break;
        case 2:
            // read flag into buffer
            read_flag(flag_ptr);
        default:
            puts("You seem like a dirty hacker!");
            exit(1);
        }
    }
}
