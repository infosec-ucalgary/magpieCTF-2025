#include "./common.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define FIELD_LENGTH 0x30
#define NUM_SUSPECTS 4
#define READ_SIZE (FIELD_LENGTH * 12)

typedef struct _user {
    char username[FIELD_LENGTH];
    char code[FIELD_LENGTH];
} user_t;

enum modes_t { USER, CODE };

// suspects from the case files
user_t suspect_table_g[NUM_SUSPECTS] = {
    {.username = "Harriette Explo", .code = "48e6b718e2672d"},
    {.username = "Richard Hash", .code = "d8b01b2435a39d"},
    {.username = "Terry Blue", .code = "55c64d0fcd6f9d5"},

    // uh oh, this guy shouldn't be here!
    {.username = "aa01171677e220e6e7a7ca41cc455ed6add9d8a0",
     .code = "dW5leG9ub3JhdGVk"},
};

// global malloc chunk ptrs
char *g_edit_buffer;
char *g_format;

void gift() {
    asm("pop %rdi");
    asm("ret");
}

void read_flag(char *buffer) {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
        puts("Flag cannot be found, contact the CTF organizers.");
        exit(ERR_NO_FLAG);
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

void show_suspects() {
    for (int i = 0; i < NUM_SUSPECTS; ++i) {
        fprintf(stdout, "Suspect %d: %20s, digital footprint %20s.\n", i + 1,
                suspect_table_g[i].username, suspect_table_g[i].code);
    }
}

void menu() {
    puts("-- NYPD Admin Terminal --");
    puts("1. Change username");
    puts("2. Change code");
    puts("3. View suspects");
    puts("4. Exit");
    printf("> ");
}

void vuln() {
    // read flag
    char flag_buffer[FLAG_SIZE] = {0}; // because the formatting is bugging me
    read_flag(flag_buffer);

    // -- exploit --
VULN_START_LOOP:
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
            break;
        case 2:
            mode = CODE;
            break;
        case 3:
            show_suspects();
            goto VULN_START_LOOP;
        case 4:
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
        edit_user(&suspect_table_g[user - 1], mode);
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

    // for the plot, decrypts to: do_you_even_have_any_proof
    strncpy(g_edit_buffer, "ZG9feW91X2V2ZW5faGF2ZV9hbnlfcHJvb2Y/",
            FIELD_LENGTH);

    // for the challenge, base template string
    strncpy(g_format, "Changed %s to %s.", FIELD_LENGTH);

    // for flare
    ssh_login("terminal2", "j@k3", "10.0.0.21", IP_CORS);

    // -- exploit --
    vuln();

    // cleanup
    free(g_edit_buffer);
    free(g_format);

    return 0;
}
