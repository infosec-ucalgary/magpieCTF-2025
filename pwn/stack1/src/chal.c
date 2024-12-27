#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

#define USERS 8
#define LENGTH 16
#define DEFAULT_USERNAME "Christina"
#define DEFAULT_PASSWORD "Crypto"

typedef struct _user {
    char username[LENGTH];
    char password[LENGTH];
    int admin;
} user_t;

user_t *user_g = NULL;

int login() {
    char local_user[LENGTH];
    char local_pass[LENGTH];

    printf("Username: ");
    fgets(local_user, LENGTH - 1, stdin);

    printf("Password: ");
    fgets(local_pass, LENGTH - 1, stdin);

    // compare the two
    if (strcmp(local_user, user_g->username) != 0) {
        return 0;
    }
    if (strcmp(local_pass, user_g->password) != 0) {
        return 0;
    }

    return 1;
}

void menu() {
    puts("-- NYPD Terminal v1 --");
    puts("1. Change username");
    puts("2. Change password");
    puts("3. Admin login");
    puts("4. Exit");
    printf("> ");
}

void change_username() {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new username: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(user_g->username, buffer); // vulnerable!
    free(buffer);
}

void change_password() {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new password: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(user_g->password, buffer); // vulnerable!
    free(buffer);
}

void admin_login() {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(1);
    }

    // read flag into buffer
    printf("Only you can be trusted with this... ");
    fgets(stdout, FLAG_SIZE - 1, fd);
    fclose(fd);
    puts("");
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // setup user
    user_g = malloc(sizeof(user_t));
    if (user_g == NULL) {
        puts("Failed to allocate memory for user_g, cannot proceed.");
        exit(-1);
    }
    strncpy(user_g->username, DEFAULT_USERNAME, LENGTH - 1);
    strncpy(user_g->password, DEFAULT_PASSWORD, LENGTH - 1);

    // login
    if (!login()) {
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

        // perform choice
        switch (option) {
        case 1: // change username
            change_username();
            break;
        case 2: // change password
            change_password();
            break;
        case 3: // admin sign in
            if (user_g->admin == 0) {
                puts("You are not authorized to view this.");
                continue;
            } else {
                admin_login();
            }
            break;
        case 4: // exit
            exit(0);
            break;
        default:
            break;
        }
    }

    return 0;
}
