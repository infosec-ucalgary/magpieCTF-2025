#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

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

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // stack vars
    char flag_buffer[FLAG_SIZE];
    char buffer[BUFFER_SIZE];

    // read the flag into the buffer
    read_flag(flag_buffer);

    // -- exploit --
    printf("Say something: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    printf("You said: ");
    printf(buffer);
    puts("Doesn't seem very interesting.");

    return 0;
}
