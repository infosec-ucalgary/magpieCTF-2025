#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../common.h"

#define WIN_USER "cristina33"
#define WIN_CODE "01843101"

#define FIELD_LENGTH 32
#define NUM_USERS 4
#define BUFFER_SIZE ((FIELD_LENGTH * 4) + 0x10)

typedef struct _user {
    char username[FIELD_LENGTH];
    char code[FIELD_LENGTH];
} user_t;

// suspects from the case files
user_t user_table_g[NUM_USERS] = {
    {.username = "hoover95", .code = "7123308"},
    {.username = "runner86", .code = "7299126"},
    {.username = "kaylined", .code = "5381272"},
    {.username = "lenscroft12", .code = "7299126"},
};

void gift() {
    asm("pop %rdi");
    asm("ret");
}

void menu() {
    puts("-- NYPD Terminal v1 --");
    puts("1. Change username");
    puts("2. Admin login");
    puts("3. Exit");
    printf("> ");
}

int login(user_t *__user) {
    // buffers
    char local_user[FIELD_LENGTH];
    char local_code[FIELD_LENGTH];

    printf("Username: ");
    fgets(local_user, FIELD_LENGTH - 1, stdin);

    printf("Enter security code: ");
    fgets(local_code, FIELD_LENGTH - 1, stdin);

    // looking thru all the users to find a match
    for (int i = 0; i < NUM_USERS; i++) {
        // using strncmp & strlen to not include the \n that fgets includes
        if (strncmp(local_user, user_table_g[i].username,
                    strlen(user_table_g[i].username)) != 0) {
            continue;
        }
        if (strncmp(local_code, user_table_g[i].code,
                    strlen(user_table_g[i].code)) != 0) {
            continue;
        }

        // the information was correct, copying the data onto the stack
        memcpy(__user, &user_table_g[i], sizeof(user_t));
        return 1;
    }

    // the hacker didn't input a valid user
    return 0;
}

// vulnerable! the buffer size is greater than the size of the string in the struct
void change_username(user_t *__user) {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new username: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(__user->username, buffer); // vulnerable!
    free(buffer);
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
    printf("Only you can be trusted with this... %s\n", buffer);
    free(buffer);
    exit(0);
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // user struct on the stack
    user_t user;

    // login
    if (!login(&user)) {
        puts("Intruder!");
        exit(1);
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
            change_username(&user);
            break;
        case 2: // try to win
            win(user);
            break;
        case 3: // exit
            goto LOOP_EXIT;
        default:
            break;
        }
    }

LOOP_EXIT:
    return 0;
}
