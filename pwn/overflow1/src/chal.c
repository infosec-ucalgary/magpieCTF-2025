#include "./common.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

// need to login with these
#define LOGIN_USER "cors33"
#define LOGIN_CODE "aW5ub2NlbnQ="

// need to change the fields to this
#define WIN_USER "netrunner2d"
#define WIN_CODE "2d9d90b636318a"

#define FIELD_LENGTH 0x30
#define NUM_SUSPECTS 4
#define BUFFER_SIZE ((FIELD_LENGTH * 8) + 0x10)

typedef struct _user {
    char username[FIELD_LENGTH];
    char code[FIELD_LENGTH];
} user_t;

// suspects from the case files
user_t suspect_table_g[NUM_SUSPECTS] = {
    {.username = "Harriette Explo", .code = "48e6b718e2672d"},
    {.username = "Richard Hash", .code = "d8b01b2435a39d"},
    {.username = "Terry Blue", .code = "55c64d0fcd6f9d5"},

    // uh oh, this guy shouldn't be here!
    {.username = "aa01171677e220e6e7a7ca41cc455ed6add9d8a0",
     .code = "dW5leG9ub3JhdGVk"},
};

void gift() {
    asm("pop %rdi");
    asm("ret");
}

void menu() {
    puts("-- NYPD Terminal --");
    puts("1. Change username");
    puts("2. Admin login");
    puts("3. Show suspects");
    puts("4. Exit");
    printf("> ");
}

int login(user_t *__user) {
    // buffers
    char local_user[FIELD_LENGTH];
    char local_code[FIELD_LENGTH];

    printf("Username: ");
    fgets(local_user, FIELD_LENGTH,
          stdin); // fgets by default reads n - 1 bytes

    printf("Enter security code: ");
    fgets(local_code, FIELD_LENGTH,
          stdin); // fgets by default reads n - 1 bytes

    // check if the input matches up
    if (strncmp(local_user, LOGIN_USER, strlen(LOGIN_USER)) != 0) {
        // didn't input the correct user
        return 0;
    }
    if (strncmp(local_code, LOGIN_CODE, strlen(LOGIN_CODE)) != 0) {
        // didn't input the correct code
        return 0;
    }

    // copy info out of the function
    strncpy(__user->username, local_user, FIELD_LENGTH);
    strncpy(__user->code, local_code, FIELD_LENGTH);

    // success
    return 1;
}

void show_suspects() {
    for (int i = 0; i < NUM_SUSPECTS; ++i) {
        fprintf(stdout, "Suspect %d: %20s, digital footprint %20s.\n", i + 1,
                suspect_table_g[i].username, suspect_table_g[i].code);
    }
}

void win(user_t __user) {
    // check information
    if (strncmp(__user.username, WIN_USER, strlen(WIN_USER)) != 0) {
        puts("Intruder!");
        exit(ERR_CHALLENGE_FAILURE);
    }
    if (strncmp(__user.code, WIN_CODE, strlen(WIN_CODE)) != 0) {
        puts("Intruder!");
        exit(ERR_CHALLENGE_FAILURE);
    }

    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd < 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(ERR_NO_FLAG);
    }

    // malloc memory for the flag
    char *buffer = malloc(sizeof(char) * FLAG_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(ERR_NO_MALLOC);
    }

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);

    // print
    printf("One of these things is not like the other... %s\n", buffer);

    // cleanup
    free(buffer);
    exit(0);
}

int vuln() {
    // user struct on the stack
    user_t user;

    // login
    if (!login(&user)) {
        puts("Authentication failure.");
        exit(ERR_CHALLENGE_FAILURE);
    }

    // main loop
    while (1) {
        int option = 0;

        // print menu
        menu();

        // get choice
        fscanf(stdin, "%d", &option);
        getchar(); // remove trailing newline

        // perform choice
        switch (option) {
        case 1: // change username
                // vulnerable! the buffer size is greater than the size of the
                // string in the
                // struct
            printf("Enter new username: ");
            fgets(user.username, BUFFER_SIZE, stdin);
            break;
        case 2: // try to win
            win(user);
            break;
        case 3: // show suspects
            show_suspects();
            break;
        case 4: // exit
            goto LOOP_EXIT;
        default:
            break;
        }
    }

LOOP_EXIT:
    return 0;
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // for flare
    ssh_login("terminal1", "j@k3", "10.0.0.20", IP_CORS);

    // -- exploit --
    vuln();

    return 0;
}
