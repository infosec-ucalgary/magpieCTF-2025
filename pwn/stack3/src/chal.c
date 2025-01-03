#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define FLAG "flag.txt"
#define FLAG_SIZE 128

#define TARGET_USERNAME "Cristina"
#define TARGET_PASSWORD "Crypto"
#define LEN_USERNAME 0x80
#define LEN_PASSWORD 0x80

#define LEN_HOSTNAME 0x80
#define LEN_TIME 0x80
#define LEN_PRE (LEN_HOSTNAME + LEN_TIME)
#define LEN_POST (LEN_USERNAME + LEN_PASSWORD + 0x180)
#define LEN_LOGS (LEN_PRE + LEN_POST)
#define MAX_LOGS 64

char *logs_g[MAX_LOGS] = {0};
int num_logs_g = 0;

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
    puts("-- NYPD Terminal v3 --");
    puts("1. Sign In");
    if (__auth == 1) {
        puts("2. View Audit Log");
    }
    puts("3. Exit");
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
        exit(-2);
    }

    // this function isn't vulnerable, because if __username or __password have
    // format characters, they won't get evaluated. Unlike the call in
    // `log_entry`
    snprintf(message, LEN_POST, "Attempted login, username %s, password %s.",
             __username, __password);

    log_entry(message);
    free(message);

    // "authentication"
    if (strncmp(__username, TARGET_USERNAME, strlen(TARGET_USERNAME)) != 0) {
        puts("Authentication failed.");
        return 0;
    }
    if (strncmp(__password, TARGET_PASSWORD, strlen(TARGET_PASSWORD)) != 0) {
        puts("Authentication failed.");
        return 0;
    }

    // logging on success
    printf("Authentication passed, welcome %s %s.\n", TARGET_USERNAME,
           TARGET_PASSWORD);

    return 1;
}

void win() {
    // open the file
    FILE *fd = fopen(FLAG, "r");
    if (fd == 0) {
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
}

int main(int argc, char **argv) {
    // setup io
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // setup username & password
    int auth = 0;
    char username[LEN_USERNAME]; // vulnerable! ret2win here
    char password[LEN_PASSWORD]; // vulnerable! ret2win here

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
            goto CASE_1;
        case 2:
            goto CASE_2;
        case 3:
            goto CASE_3;
        default:
            break;
        }

    CASE_1:
        auth = login(username, password);
        goto LOOP_END;
    CASE_2:
        if (auth == 0) {
            puts("Unauthorized.");
        } else {
            view_logs();
        }
        goto LOOP_END;
    CASE_3:
        goto LEAVE_MAIN;
    LOOP_END:
        continue;
    }

LEAVE_MAIN:
    // cleanup
    for (int i = 0; i < MAX_LOGS; ++i) {
        if (logs_g[i] != NULL)
            free(logs_g[i]);
    }

    return 0;
}
