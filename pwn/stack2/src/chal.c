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

int login(user_t *cmp) {
    char local_user[LENGTH];
    char local_pass[LENGTH];

    printf("Username: ");
    fgets(local_user, LENGTH - 1, stdin);

    printf("Password: ");
    fgets(local_pass, LENGTH - 1, stdin);

    // compare the two
    if (strcmp(local_user, cmp->username) != 0) {
        return 0;
    }
    if (strcmp(local_pass, cmp->password) != 0) {
        return 0;
    }

    return 1;
}

void menu() {
    puts("-- NYPD Terminal v2 --");
    puts("1. Change username");
    puts("2. Change password");
    puts("3. Exit");
    printf("> ");
}

void change_username(user_t *cmp) {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new username: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(cmp->username, buffer); // vulnerable!
    free(buffer);
}

void change_password(user_t *cmp) {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new password: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(cmp->password, buffer); // vulnerable!
    free(buffer);
}

void admin_login() {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(1);
    }

    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
    printf("Only you can be trusted with this... %s\n", buffer);
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // setup user
    user_t user = {
        .username = DEFAULT_USERNAME,
        .password = DEFAULT_PASSWORD,
        .admin = 0
    };

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

        // perform choice
        switch (option) {
        case 1: // change username
            change_username(&user);
            break;
        case 2: // change password
            change_password(&user);
            break;
        case 3: // exit
            exit(0);
            break;
        default:
            break;
        }
    }

    return 0;
}
