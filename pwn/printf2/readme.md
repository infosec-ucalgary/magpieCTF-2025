# printf2

Author: oblivious_turnip

>Difficulty: medium (hard if they don't know what to do)

- [x] stack canaries
- [x] ASLR
- ret2libc? nope

ret2libc isn't possible unless the hacker can escape the while loop
(which should be impossible unless they can somehow change `rip`)

Flag: `magpieCTF{n3tr8nn3r_1s_c@p4bl3}`

## Backstory

New email from <cors@nypd.gov>:

It appears that *Jake* was using that zombie router to plan some sort of
*infiltration*, presumably into Christina's manor. The cyberteam
has identified yet another device (out of presumably hundreds) that
might have more clues as to what *Jake* was planning. Good luck.

>Plot:
>The buffer that's supposed to hold the flag contains: "xelcgb_vf_tbar", when unencrypted says:
>"krypto_is_gone".

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

## Handouts

- program
