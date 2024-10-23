import math

obf_flag = [
    0xFFFFFF99,
    0xFFFFFFA3,
    0xFFFFFFAD,
    0xFFFFFFB3,
    0xFFFFFFB0,
    0x7C,
    0x72,
    0x57,
    0x22,
    0x75,
    0x3F,
    0x3E,
    0x5B,
    0xFFFFFFF1,
    0xFFFFFFE7,
    0xFFFFFFC6,
    0xFFFFFF83,
    0x58,
    0x49,
    0x11,
    0xFFFFFFCF,
    0xFFFFFFD0,
    0xFFFFFFB7,
    0x67,
    0x7E,
    0xFFFFFFF4,
]
v3 = [0x13, 0x20, 0x25, 0x35, 0x54]
v4 = 42
flag_length = len(obf_flag)
decrypted_flag: list[str] = []
for i in range(flag_length):
    value = obf_flag[i] ^ (flag_length - 1)
    value = ~value
    v5 = int(math.pow(i + 1, 2))
    value = (value - v5) % 256
    char = value ^ v3[i % 5]
    decrypted_flag.append(chr(char))

decrypted_flag_str = "".join(decrypted_flag)
print("Decrypted Flag:", decrypted_flag_str)
