# printf2

Author: oblivious_turnip

>Difficulty: intermediate (hard if they don't know what to do)

- [x] stack canaries
- [x] ASLR
- ret2libc? nope

ret2libc isn't possible unless the hacker can escape the while loop
(which should be impossible unless they can somehow change `rip`)

Flag: `magpieCTF{printf_is_dangerous}`

## Backstory

"We've identified yet another zombie device belonging to *Niko*'s botnet.
This variant of malware isn't so... helpful this time around. Good luck soldier."

## Intended Solve

The flag is located in the global `.data` section again, but this time, the hacker
is supposed to use `%n` to overwrite the `flag_ptr` located on the stack to point
to somewhere that the hacker can access.

There are two methods of overwriting `flag_ptr`.

- use a saved `rbp` as a gadget
- writing a gadget into the buffer and using that to change `flag_ptr`

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

The reason why we're including the docker file is because the stack layout differs
between versions of libc. Since this is a beginner challenge, I guess we should give
this out.
