#include <stdio.h>
#include <string.h>
#include <math.h>

int main() {
	char flag[] = "magpieCTF{sh1ft3d_s3crets}";
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

	printf("Bytes: ");
	for (int i = 0; i < v1; i++) {
		printf("0x%02X, ", obf[i]);
	}
	printf("\n");

	return 0;
}
