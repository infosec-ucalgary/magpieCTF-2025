#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <math.h>

int securityLevel = 5;  
int toolsAvailable = 3; 
int cluesFound = 0;

int bypassSecurity(int *securityLevel) {
    printf("You hack into the security system...\n");
    sleep(1);
    if (*securityLevel > 0) {
        *securityLevel -= 1;
        printf("Security bypassed! Remaining security level: %d\n", *securityLevel);
    } else {
        printf("The system is fully compromised. You have access...\n");
    }
    return *securityLevel;
}

void hideFromSurveillance() {
    printf("You duck into the shadows, avoiding a roaming security drone...\n");
    for (int i = 0; i < 3; i++) {
        printf("Waiting for %d seconds...\n", (i + 1) * 2);
        sleep(2);
    }
    printf("Surveillance passed. You’re still undetected.\n");
}

void gatherTools() {
    toolsAvailable += 1;
    printf("You find a new tool in a hidden compartment. Tools left: %d\n", toolsAvailable);
}

void investigateKryptoFiles() {
    printf("You open Christina Krypto’s encrypted file...\n");
    printf("The file seems to be a banking application masquerading as a decoy...\n");
    printf("But something's off. It’s hiding something, something big...\n");
    printf("It’s all obfuscated. It looks like Krypto was up to something far more sinister.\n");

    cluesFound++;
    printf("Clue found: Hidden encryption within the code.\n");
}

void decryptFiles() {
    printf("Decrypting the hidden files...\n");
    if (cluesFound == 0) {
        printf("You need more clues to decrypt the files!\n");
    } else {
        printf("Decrypting with the tools you’ve gathered...\n");

        int i;
        unsigned char encryptedData[] = {0x1F, 0x4D, 0x30, 0x7E, 0x55, 0x2A, 0x11, 0x6F};

        printf("Attempting decryption...\n");

        for (i = 0; i < sizeof(encryptedData); i++) {
            printf("Decrypting byte %d: 0x%X -> 0x%X\n", i, encryptedData[i], encryptedData[i] ^ 0xFF);
        }
        printf("Decryption failed! You need to crack the final layer.\n");
    }
}

int scrambleData() {
    char flag[] = "magpieCTF{s4mpl3_fl4g}";
    unsigned char obf[50];
    int v1 = strlen(flag);
    int v3[5] = {0x13, 0x20, 0x25, 0x35, 0x54};

    for (int i = 0; i < v1; i++) {
        int v5 = (int)(pow(i + 1, 2));
        obf[i] = (flag[i] ^ v3[i % 5]);        
        obf[i] = (obf[i] + v5) % 256;           
        obf[i] = ~obf[i];                       
        obf[i] = obf[i] ^ (v1 - 1);            
    }
    obf[v1] = '\0'; 

    printf("Encrypted data stored. Continue investigation to decrypt it.\n");
    return 0;
}

void gameLoop() {
    char choice;

    printf("Welcome to the Krypto investigation...\n");
    printf("You’ve entered Christina Krypto’s hidden terminal, attempting to uncover her illegal activities.\n");
    printf("The city is a dark, rainy labyrinth. Everything is digital, encrypted, and dangerous.\n");
    printf("Security Level: %d | Tools Available: %d | Clues Found: %d\n", securityLevel, toolsAvailable, cluesFound);

    while (securityLevel > 0) {
        printf("\nChoose your next action:\n");
        printf("1. Bypass Security Systems\n");
        printf("2. Investigate Krypto's Encrypted Files\n");
        printf("3. Hide from Surveillance\n");
        printf("4. Gather More Tools\n");
        printf("5. Attempt to Crack the Encryption\n");
        printf("6. Escape the Network\n");
        printf("7. Check Your Progress\n");
        printf("8. Decrypt Final Clue\n");
        printf("9. Exit Investigation\n");

        choice = getchar();
        getchar(); 

        switch (choice) {
            case '1':
                bypassSecurity(&securityLevel);
                break;
            case '2':
                investigateKryptoFiles();
                break;
            case '3':
                hideFromSurveillance();
                break;
            case '4':
                gatherTools();
                break;
            case '5':
                printf("Cracking the encryption... You’re getting closer...\n");
                break;
            case '6':
                printf("You’ve backed out. The case is still open.\n");
                return;
            case '7':
                printf("Security Level: %d | Tools Available: %d | Clues Found: %d\n", securityLevel, toolsAvailable, cluesFound);
                break;
            case '8':
                scrambleData();
                break;
            case '9':
                printf("You’ve decided to pull out. Investigation terminated.\n");
                return;
            default:
                printf("Invalid option! Try again.\n");
        }
    }
    printf("Security systems are online again. You failed to crack the case...\n");
}

int main() {
    srand(time(NULL));
    gameLoop();
    return 0;
}
