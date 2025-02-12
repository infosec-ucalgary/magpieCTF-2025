#include "./common.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define TARGET_USERNAME "j@k3th3gr3@t"
#define TARGET_PASSWORD "d3c31tful_l3@d3r"
#define LEN_USERNAME 0x40
#define LEN_PASSWORD 0x40
#define READ_SIZE 0x100

#define LEN_HOSTNAME 0x30
#define LEN_TIME 0x30
#define LEN_PRE (LEN_HOSTNAME + LEN_TIME) // pre = hostname & timestamp
#define LEN_LOGMSG (LEN_USERNAME + LEN_PASSWORD + 0x80) // the log content
#define LEN_LOG (LEN_PRE + LEN_LOGMSG + 0x20)           // the length of the log
#define MAX_LOGS 32

char *logs_g[MAX_LOGS] = {0};
int num_logs_g = 0;

void gift() {
    asm("pop %rdi");
    asm("ret");
}

// vulnerable!
void log_entry(char *__input, ssize_t nb) {
    // check if we can log
    if (num_logs_g >= MAX_LOGS) {
        puts("This machine can't log anymore.");
        return;
    }

    // malloc a chunk for logging
    logs_g[num_logs_g] = malloc(sizeof(char) * LEN_LOG);
    if (logs_g[num_logs_g] == NULL) {
        puts("Failed to allocate memory for logs_g, cannot proceed.");
        exit(ERR_NO_MALLOC);
    }

    // log is formatted:
    // 1. hostname
    // 2. time
    // 3. user input
    char pre_format[] = "[%s @ %s]: ";

    // this function is complicated by design, an attempt to obscure the exploit
    char *hostname = malloc(sizeof(char) * LEN_HOSTNAME);
    if (hostname == NULL) {
        puts("Couldn't allocate memory for hostname, contact the CTF "
             "organizers.");
        exit(ERR_NO_MALLOC);
    }
    char *raw_time = malloc(sizeof(char) * LEN_TIME);
    if (raw_time == NULL) {
        puts("Couldn't allocate memory for raw_time, contact the CTF "
             "organizers.");
        exit(ERR_NO_MALLOC);
    }
    char *post = malloc(sizeof(char) * LEN_LOGMSG);
    if (post == NULL) {
        puts("Couldn't allocate memory for post, contact the CTF organizers.");
        exit(ERR_NO_MALLOC);
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
    strncpy(post, pre_format, LEN_LOGMSG);
    strncat(post, __input, LEN_LOGMSG - strlen(post));
    post[LEN_LOGMSG - 1] = '\0';

    // use snprintf to format everything, unsafe!
    // vulnerable! unsafe due to user input potentially having format characters
    snprintf(logs_g[num_logs_g], nb < LEN_LOG ? nb : LEN_LOG, post, hostname,
             raw_time);

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
    puts("-- j@k3's PC --");
    puts("1. Sign In");
    if (__auth == 1) {
        puts("2. View Audit Log");
        puts("3. Exit");
    }
    printf("> ");
}

// vulnerable! this is where the hacker will ret2libc
// also, this function is responsible for generating logs
int login(char *__username, char *__password) {
    // getting the username and password
    printf("Username: ");
    fgets(__username, LEN_LOGMSG,
          stdin); // vulnerable! read size is greater than buffer size!
    printf("Password: ");
    fgets(__password, LEN_LOGMSG,
          stdin); // vulnerable! read size is greater than buffer size!

    // this makes the output nicer (this shouldn't affect solvability)
    __username[strlen(__username) - 1] = '\0';
    __password[strlen(__password) - 1] = '\0';

    // logging to the audit log
    char *message = malloc(sizeof(char) * LEN_LOGMSG);
    if (message == NULL) {
        puts("Couldn't allocate memory for message, contact the CTF "
             "organizers.");
        exit(ERR_NO_MALLOC);
    }

    // the `login` function isn't vulnerable, however passing in format
    // characters here makes this program vulnerable because of a logic error in
    // `log_entry`
    snprintf(message, LEN_LOGMSG, "Attempted login, username %s, password %s.",
             __username, __password);

    // logging the message
    log_entry(message, LEN_LOGMSG);
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
    printf("Welcome Jake.\n");

    return 1;
}

// vulnerable!
void vuln() {
    // setup username & password
    int auth = 0;
    char username[LEN_USERNAME]; // vulnerable! buffer overflow from login
    char password[LEN_PASSWORD]; // vulnerable! buffer overflow from login

    // main loop
    while (1) {
        int option = 0;

        // print menu
        menu(auth);

        // get choice
        fscanf(stdin, "%d", &option);
        getchar();

        // do choice
        switch (option) {
        case 1:
            // += so that the hacker doesn't have to log in and out repeatedly
            auth += login(username, password);
            break;
        case 2:
            if (auth == 0) {
                puts("Unauthorized.");
            } else {
                view_logs();
            }
            break;
        case 3:
            if (auth == 0) {
                puts("Unauthorized.");
            } else {
                goto LEAVE_VULN;
            }
            break;
        default:
            break;
        }
    }

LEAVE_VULN:
    return;
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // some flare
    ssh_login("netrunner2", "j@k3", IP_NETRUNNER2, IP_JAKE);

    // -- exploit --
    vuln();

    // cleanup
    for (int i = 0; i < MAX_LOGS; ++i) {
        if (logs_g[i] != NULL)
            free(logs_g[i]);
    }

    return 0;
}
