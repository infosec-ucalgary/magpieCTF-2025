#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

#define ERR_CHALLENGE_FAILURE 2
#define ERR_NO_MALLOC 3
#define ERR_OTHER 4

void menu() {}

void win() {
    // insert impossible condition here

    // flag buffer
    char flag_buffer[FLAG_SIZE];

    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd < 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(ERR_OTHER);
    }

    // read flag into buffer
    fgets(flag_buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
    printf("Only you can be trusted with this... %s\n", flag_buffer);
    exit(0);
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // main loop
    while (1) {
        int option = 0;

        // print menu
        menu();

        // get choice
        fscanf(stdin, "%d", &option);
        getchar();
    }

LOOP_EXIT:
    return 0;
}
