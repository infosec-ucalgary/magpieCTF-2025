#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128
#define BUFFER_SIZE 0x100

#define FIELD_LENGTH 16
#define DEFAULT_USERNAME "Cristina"
#define DEFAULT_PASSWORD "Crypto"

typedef struct _user {
    char username[FIELD_LENGTH];
    char password[FIELD_LENGTH];
    int admin;
} user_t;

// struct used to overflow
user_t user_g = {
    .username = DEFAULT_USERNAME, .password = DEFAULT_PASSWORD, .admin = 0};

int login(user_t *__user) {
    // buffers
    char local_user[FIELD_LENGTH];
    char local_pass[FIELD_LENGTH];

    printf("Username: ");
    fgets(local_user, FIELD_LENGTH - 1, stdin);

    printf("Password: ");
    fgets(local_pass, FIELD_LENGTH - 1, stdin);

    // using strncmp so that it doesn't compare the newline that's in local_xxxx
    if (strncmp(local_user, __user->username, strlen(__user->username)) != 0) {
        return 0;
    }
    if (strncmp(local_pass, __user->password, strlen(__user->password)) != 0) {
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

void change_password(user_t *__user) {
    char *buffer = malloc(sizeof(char) * BUFFER_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    printf("Enter new password: ");
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    strcpy(__user->password, buffer); // vulnerable!
    free(buffer);
}

void win() {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd < 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(1);
    }

    char *buffer = malloc(sizeof(char) * FLAG_SIZE);
    if (buffer == NULL) {
        puts("Failed to allocate memory for buffer, cannot proceed.");
        exit(-2);
    }

    // read flag into buffer
    fgets(buffer, FLAG_SIZE - 1, fd);
    fclose(fd);
    printf("Only you can be trusted with this... %s\n", buffer);
    exit(0);
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // login
    if (!login(&user_g)) {
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
        getchar();

        // perform choice
        switch (option) {
        case 1: // change username
            change_username(&user_g);
            break;
        case 2: // change password
            change_password(&user_g);
            break;
        case 3: // admin sign in
            if (user_g.admin == 0) {
                puts("You are not authorized to view this.");
            } else {
                win();
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
