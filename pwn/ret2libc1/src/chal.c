#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "../../common.h"

#define TARGET_USERNAME "n1k0th3gr3@t"
#define TARGET_PASSWORD "cr1st1n@scks"
#define LEN_USERNAME 0x40
#define LEN_PASSWORD 0x40

#define LEN_HOSTNAME 0x80
#define LEN_TIME 0x80
#define LEN_PRE (LEN_HOSTNAME + LEN_TIME)
#define LEN_POST (LEN_USERNAME + LEN_PASSWORD + 0x180)
#define LEN_LOGS (LEN_PRE + LEN_POST)
#define MAX_LOGS 64

char *logs_g[MAX_LOGS] = {0};
int num_logs_g = 0;

void gift() {
    asm("pop %rdi");
    asm("ret");
}

// vulnerable function!
void log_entry(char *__input) {
    // check if we can log
    if (num_logs_g >= MAX_LOGS) {
        puts("This machine can't log anymore.");
        return;
    }

    // malloc a chunk for logging
    logs_g[num_logs_g] = malloc(sizeof(char) * LEN_LOGS * MAX_LOGS);
    if (logs_g[num_logs_g] == NULL) {
        puts("Failed to allocate memory for logs_g, cannot proceed.");
        exit(-1);
    }

    // log is formatted:
    // 1. hostname
    // 2. time
    // 3. user input << unsafe!
    char pre_format[] = "[%s @ %s]: ";

    // this function is complicated by design, an attempt to obscure the exploit
    char *hostname = malloc(sizeof(char) * LEN_HOSTNAME);
    if (hostname == NULL) {
        puts("Couldn't allocate memory for hostname, contact the CTF "
             "organizers.");
        exit(-2);
    }
    char *raw_time = malloc(sizeof(char) * LEN_TIME);
    if (raw_time == NULL) {
        puts("Couldn't allocate memory for raw_time, contact the CTF "
             "organizers.");
        exit(-2);
    }
    char *post = malloc(sizeof(char) * LEN_POST);
    if (post == NULL) {
        puts("Couldn't allocate memory for post, contact the CTF organizers.");
        exit(-2);
    }

    // format hostname
    gethostname(hostname, LEN_HOSTNAME);
    hostname[LEN_HOSTNAME - 1] = '\0';

    // format time
    time_t time_struct;
    time(&time_struct);
    strftime(raw_time, LEN_TIME, "%x - %I:%M%p", localtime(&time_struct));
    raw_time[LEN_TIME - 1] = '\0';

    // combine format string and user input together, unsafe!
    strncpy(post, pre_format, LEN_POST);
    strncat(post, __input, LEN_POST - strlen(post));
    post[LEN_POST - 1] = '\0';

    // use snprintf to format everything, unsafe!
    // unsafe due to user input potentially having format characters
    snprintf(logs_g[num_logs_g], LEN_LOGS, post, hostname, raw_time);

    // incrementing the log count
    num_logs_g += 1;

    // cleanup
    free(hostname);
    free(raw_time);
    free(post);
}

void view_logs() {
    for (int i = 0; i < num_logs_g; ++i) {
        puts(logs_g[i]);
    }
}

void menu(int __auth) {
    puts("-- N1k0's PC --");
    puts("1. Sign In");
    if (__auth == 1) {
        puts("2. View Audit Log");
        puts("3. Exit");
    }
    printf("> ");
}

// there is no actual login, this is just filler to generate logs
int login(char *__username, char *__password) {
    // getting the username and password
    printf("Username: ");
    fgets(__username, LEN_POST,
          stdin); // intentional vulnerability here, the read size is waaay
                  // bigger than the buffer size
    printf("Password: ");
    fgets(__password, LEN_POST,
          stdin); // intentional vulnerability here, the read size is waaay
                  // bigger than the buffer size

    // this makes the output nicer (this shouldn't affect solvability)
    __username[strlen(__username) - 1] = '\0';
    __password[strlen(__password) - 1] = '\0';

    // logging to the audit log
    char *message = malloc(sizeof(char) * LEN_POST);
    if (message == NULL) {
        puts("Couldn't allocate memory for message, contact the CTF "
             "organizers.");
        exit(ERR_NO_MALLOC);
    }

    // the `login` function isn't vulnerable, however passing in format
    // characters here makes this program vulnerable because of a logic error in
    // `log_entry`
    snprintf(message, LEN_POST, "Attempted login, username %s, password %s.",
             __username, __password);

    log_entry(message);
    free(message);

    // checking username
    if (strncmp(__username, TARGET_USERNAME, strlen(TARGET_USERNAME)) != 0) {
        puts("Authentication failed.");
        return 0;
    }

    // checking password
    if (strncmp(__password, TARGET_PASSWORD, strlen(TARGET_PASSWORD)) != 0) {
        puts("Authentication failed.");
        return 0;
    }

    // logging on success
    printf("Welcome %s %s.\n", __username, __password);

    return 1;
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // setup username & password
    int auth = 0;
    char username[LEN_USERNAME]; // buffer overflow here!
    char password[LEN_PASSWORD]; // buffer overflow here!

    // main loop
    while (1) {
        int option = 0;

        // print menu
        menu(auth);

        // get choice
        fscanf(stdin, "%d", &option);
        getchar();

        // perform choice
        // using goto statements because I wanna fuck with the participants
        switch (option) {
        case 1:
            auth = login(username, password);
        case 2:
            if (auth == 0) {
                puts("Unauthorized.");
            } else {
                view_logs();
            }
        case 3:
            if (auth == 0) {
                puts("Unauthorized.");
            } else {
                goto LEAVE_MAIN;
            }
        default:
            break;
        }
    }

LEAVE_MAIN:
    // cleanup
    for (int i = 0; i < MAX_LOGS; ++i) {
        if (logs_g[i] != NULL)
            free(logs_g[i]);
    }

    return 0;
}
