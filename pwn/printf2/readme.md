# printf2

>Difficulty: hard

- [x] stack canaries
- [x] ASLR
- ret2libc? nope

## Backstory

something

## Intended Solve

The flag is again located in the `.data` section, but this time there is
no helping `memcpy` function. The hacker must alter `flag_ptr` using either:

- a saved `rbp` as a gadget
- putting the gadget into the buffer and printing to that stack variable (my solve does this)

The intended exploit is as follows:

1. leak an `rbp`
1. use said leaked `rbp` to calculate the address of `buffer` & `flag_ptr`
1. write the address of `flag_ptr` into the buffer and then use `%n` to write to this gadget to a different address
1. call `read_flag()`
1. read the flag off of the stack
1. win

>Side effects:  
>For whatever reason, after reading the flag, it appears that
>the contents of the stack (at least the data returned from `printf`)
>become *corrupted* and will include the payload I previously sent.
>I really don't know why this happens, but the challenge is still solvable despite this.

## Handouts

- program
- Dockerfile, or `libc.so.6` and the linker `ld-linux-x86_64.so.2`
