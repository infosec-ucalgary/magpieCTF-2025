# overflow2

Author: oblivious_turnip

>Difficulty: easy (hard ret2libc)

- [ ] stack canaries (to make it easier)
- [x] ASLR (they can leak the return address, they can suffer)
- ret2libc? yes

ret2libc is hypothetically possible because you could hypothetically create a rop-chain
using the vulnerable format string.

Host flag: `magpieCTF{i_love_insecure_format_strings}`
Root flag: `magpieCTF{printf_can_create_rop_chains}`

## Backstory

"It seems that the hacker *Niko* has made another fake terminal, again including our case files! We need you to hack into the terminal and see what you can find."

## Intended Solve

The exploit isn't quite obvious, what happens is there are two malloc chunks allocated,
one to edit the contents of a user, the other stores a format string for `printf`.

The idea here is that in the `edit_user` function, the hacker overflows the `g_edit_buffer`
malloc chunk into the `g_format` chunk to include more format characters than intended,
leaking the flag off of the stack.

## Handouts

- program
