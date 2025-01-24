# printf1

Author: oblivious_turnip

>Difficulty: easy

- [x] stack canaries
- [x] ASLR
- ret2libc? nope

ret2libc isn't possible here because of the call to
`exit` in the `vuln` function.

Flag: `magpieCTF{aslr_isnt_foolproof}`

## Backstory

"We've identified a zombie device, belonging to the hacker *Niko*, it's your task to
break in and find whatever's on that machine."

## Intended Solve

The flag is located in the global `.data` section of the program,
the hacker has to leak the return address of `vuln` in order to calculate the
real address of `flag_buffer`. After which, the program will `memcpy` whatever
address that was entered into the program into the local `buffer` on the stack.

The intended exploit is as follows:

1. leak the return address of `vuln` (which is `main`)
1. use this leak to calculate the address of `flag_buffer`, defeating ASLR
1. input the address of `flag_buffer` into the program, which will copy the contents of `flag_buffer` into `buffer`
1. the flag will be printed out to the screen

## Handouts

- program
