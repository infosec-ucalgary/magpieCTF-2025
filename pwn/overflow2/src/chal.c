#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../common.h"

#define FIELD_LENGTH 32
#define NUM_USERS 4
#define READ_SIZE (FIELD_LENGTH * 4)

typedef struct _user {
    char username[FIELD_LENGTH];
    char code[FIELD_LENGTH];
} user_t;

enum modes_t { USER, CODE };

// suspects from the case files
user_t user_table_g[NUM_USERS] = {
    {.username = "hoover95", .code = "7123308"},
    {.username = "runner86", .code = "7299126"},
    {.username = "kaylined", .code = "5381272"},
    {.username = "lenscroft12", .code = "7299126"},
};

// global malloc chunk ptrs
char *g_edit_buffer;
char *g_format;

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

// vulnerable!
void edit_user(user_t *user, mode_t mode) {
    // local buffer for printing
    char local_old[FIELD_LENGTH];

    // copy field into buffer
    strncpy(g_edit_buffer, mode == USER ? user->username : user->code,
            FIELD_LENGTH);
    strncpy(local_old, mode == USER ? user->username : user->code,
            FIELD_LENGTH);

    // edit on buffer
    printf("Enter in new value: ");
    fgets(g_edit_buffer, READ_SIZE,
          stdin); // vulnerable! overflows into next malloc chunk!

    // vulnerable! the hacker has control of the format string which is used to
    // leak the flag
    printf(g_format, local_old, g_edit_buffer);

    // copy buffer back into field
    strncpy(mode == USER ? user->username : user->code, g_edit_buffer,
            FIELD_LENGTH);
}

void menu() {
    puts("-- NYPD Admin Terminal --");
    puts("1. Change username");
    puts("2. Change code");
    puts("3. Exit");
    printf("> ");
}

void vuln() {
    // read flag
    char flag_buffer[FLAG_SIZE];
    read_flag(flag_buffer);

    // -- exploit --
    while (1) {
        int option = 0;
        int user = 0;
        mode_t mode;

        // print the menu
        menu();

        // get option
        fscanf(stdin, "%d", &option);
        getchar();

        // switch on option
        switch (option) {
        case 1:
            mode = USER;
        case 2:
            mode = CODE;
        case 3:
            goto LEAVE_VULN;
        default:
            continue;
        }

        // get user
        printf("Which user? (1-4)\n> ");
        fscanf(stdin, "%d", &user);
        getchar();

        // some verification
        if (user < 1 || user > 4) {
            puts("Unauthorized access, dispatching police now.");
            exit(ERR_CHALLENGE_FAILURE);
        }

        // call function
        edit_user(&user_table_g[user - 1], mode);
    }

LEAVE_VULN:
    return;
}

int main() {
    // setup
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // malloc chunks
    g_edit_buffer = malloc(sizeof(char) * FIELD_LENGTH);
    if (g_edit_buffer == NULL) {
        puts("Couldn't allocate memory for g_edit_buffer, contact the CTF "
             "devs.");
        exit(ERR_NO_MALLOC);
    }

    g_format = malloc(sizeof(char) * FIELD_LENGTH);
    if (g_format == NULL) {
        puts("Couldn't allocate memory for g_format, contact the CTF devs.");
        exit(ERR_NO_MALLOC);
    }

    // more setup
    strncpy(g_format, "Changed %s to %s.", FIELD_LENGTH);

    // -- exploit --
    vuln();

    // cleanup
    free(g_edit_buffer);
    free(g_format);

    return 0;
}
