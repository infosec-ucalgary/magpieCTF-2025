import math

obf_flag = [
    0xA2,
    0x98,
    0x96,
    0x88,
    0x8B,
    0x47,
    0x49,
    0x6C,
    0x19,
    0x4E,
    0x2C,
    0x3F,
    0x60,
    0xD4,
    0xDC,
    0xFE,
    0x7D,
    0x56,
    0x1F,
    0x2D,
    0xF4,
    0xF2,
    0x84,
    0x9C,
    0x4A,
    0xC1,
    0x31,
    0xBC,
    0x6E,
    0x69,
    0x3C,
    0xC9,
    0x57,
    0x17,
    0x2F,
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

# checking for the flag
flag = "magpieCTF{kr1pt0_bl4ckm4rk3t_d34ls}"
if flag in decrypted_flag_str:
    print("MagpieCTF - black-market-binary : True")
    exit(0)
else:
    print("MagpieCTF - black-market-binary : False")
    exit(1)
