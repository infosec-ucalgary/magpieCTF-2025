#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

int CC(int *securityLevel) {
  printf("Failed to pick the lock! Trying to get the code...\n");
  for (int i = 0; i < 3; i++) {
    printf("Searching for clues... Attempt %d\n", i + 1);
  }
  printf("No luck! Where could I find the code?.\n");
  return 0;
}

void FF() {
  printf("You are stealthily performing the heist...\n");
  for (int i = 0; i < 5; i++) {
    printf("Moving to the next area...\n");
    sleep(1);
  }
  printf("The heist is complete! You successfully stole the valuables.\n");
}

void GG(int *toolsAvailable) {
  *toolsAvailable += 1;
  printf("You gathered an additional tool. Total tools now: %d\n",
         *toolsAvailable);
}

int HH() { return rand() % 2; }

int A(int a, int b) {
  printf("Calculating the optimal path with tools %d and %d...\n", a, b);
  return a + b;
}

void B(const char *message) { printf("%s\n", message); }

int C(int value) {
  printf("Setting up the operation value: %d\n", value);
  return value;
}

float D(float num) {
  printf("Preparing the cash: $%.2f\n", num * 1.05);
  return num * 2;
}

void E(int *x, int *y) {
  printf("Swapping the vault codes...\n");
  int temp = *x;
  *x = *y;
  *y = temp;
  printf("Codes swapped: Code 1 is now %d, Code 2 is now %d\n", *x, *y);
}

int F() {
  int amount = rand() % 1000;
  printf("Calculating the random amount: $%d\n", amount);
  return amount;
}

void G(int number) {
  if (number > 0) {
    printf("Validating the amount: $%d\n", number);
  } else {
    printf("Error: Invalid amount!\n");
  }
}

int H(char c) { return (int)c; }

void DD() {
  printf("You are hiding behind the vault...\n");
  for (int i = 0; i < 3; i++) {
    printf("Holding your breath... %d seconds...\n", (i + 1) * 2);
    sleep(2);
  }
  printf("You are safe for now!\n");
}

void EE() { printf("You have successfully escaped with the loot!\n"); }

const char *I(const char *str) { return str; }

void J(int n) {
  printf("Checking the getaway vehicle status with code: %d\n", n);
}

void K(const char *errorMessage) { printf("Error: %s\n", errorMessage); }

int L(const char *str) { return strlen(str); }

int PP() {
  char flag[] = "magpieCTF{s4mpl3_fl4g}";
  unsigned char obf[50];
  int v1 = strlen(flag);
  int v2 = 15;
  int v3[5] = {0x13, 0x20, 0x25, 0x35, 0x54};
  int v4 = 42;

  for (int i = 0; i < v1; i++) {
    int v5 = (int)(pow(i + 1, 2));
    obf[i] = (flag[i] ^ v3[i % 5]);
    obf[i] = (obf[i] + v5) % 256;
    obf[i] = ~obf[i];
    obf[i] = obf[i] ^ (v1 - 1);
  }
  obf[v1] = '\0';
  printf("Obfuscated flag: %s\n", obf);
  return 0;
}

int M(int a, int b) { return (a > b) ? a : b; }

int N(int a, int b, int c) { return (a < b && a < c) ? a : (b < c ? b : c); }

void O(int n) {
  printf("Counting down to the heist: %d...\n", n);
  for (int i = n; i > 0; i--) {
    printf("%d...\n", i);
    sleep(1);
  }
  printf("Go!\n");
}

void P(int num) { printf("Recording the stolen amount: $%d\n", num); }

void AA(int securityLevel, int toolsAvailable) {
  printf("Security Level: %d | Tools Available: %d\n", securityLevel,
         toolsAvailable);
}

void Q(int *arr, int size) {
  printf("Array of stolen items:\n");
  for (int i = 0; i < size; i++) {
    printf("Item %d: $%d\n", i + 1, arr[i]);
  }
  printf("\n");
}

double R(double num) { return num * num; }

int ZZ() {
  char code[] = {0x99, 0xA3, 0xAD, 0xB3, 0xB0, 0x7C, 0x72, 0x57, 0x22,
                 0x75, 0x3F, 0x3E, 0x5B, 0xF1, 0xE7, 0xC6, 0x83, 0x58,
                 0x49, 0x11, 0xCF, 0xD0, 0xB7, 0x67, 0x7E, 0xF4};
  printf("Decrypting the vault security code...\n");
  printf("Warning: This operation is highly sensitive!\n");

  for (int i = 0; i < sizeof(code); i++) {
    printf("Character %d: 0x%X (Attempting to decode...)\n", i, code[i]);
  }

  printf("Decryption failed! The vault remains secure. You need more clues!\n");
  return 0;
}
const char *S(const char *str1, const char *str2) { return str1; }

int BB(int *securityLevel) {
  int success = rand() % 2;
  if (success) {
    *securityLevel = *securityLevel > 1 ? *securityLevel - 1 : 0;
    printf("You successfully disabled a security system!\n");
  } else {
    printf("Failed to disable the security system!\n");
  }
  return success;
}

void T(int n) { printf("Performing action T with value: %d\n", n); }

void gameLoop() {
  int securityLevel = 5;
  int toolsAvailable = 3;
  char choice;

  printf("Welcome to the Bank Heist!\n");
  AA(securityLevel, toolsAvailable);

  while (securityLevel > 0) {
    printf("\nChoose an action:\n");
    printf("1. Disable Security\n");
    printf("2. Pick Lock\n");
    printf("3. Hide\n");
    printf("4. Gather Tools\n");
    printf("5. Perform Heist\n");
    printf("6. Escape\n");
    printf("7. Check Status\n");
    printf("8. Decrypt code\n");
    printf("9. Exit Game\n");

    choice = getchar();
    getchar();

    switch (choice) {
    case '1':
      if (toolsAvailable > 0) {
        BB(&securityLevel);
        toolsAvailable--;
      } else {
        printf("You don't have any tools left to disable the security!\n");
      }
      break;
    case '2':
      if (toolsAvailable > 0) {
        CC(&securityLevel);
        toolsAvailable--;
      } else {
        printf("You don't have any tools left to pick the lock!\n");
      }
      break;
    case '3':
      DD();
      break;
    case '4':
      GG(&toolsAvailable);
      break;
    case '5':
      FF();
      return;
    case '6':
      EE();
      return;
    case '7':
      AA(securityLevel, toolsAvailable);
      break;
    case '8':
      ZZ();
      break;
    case '9':
      printf("Exiting game...\n");
      return;
    default:
      printf("Invalid choice! Please try again.\n");
    }
  }
}

int main() {
  srand(time(NULL));
  gameLoop();

  return 0;
}
