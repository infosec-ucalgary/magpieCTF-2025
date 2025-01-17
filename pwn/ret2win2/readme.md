# ret2win2

>Difficulty: hard

- [x] stack canaries
- [x] ASLR
- ret2libc? yes

## Backstory

something

## Intended Solve

Because the `buffer` is a fraction of the size compared to what's being read, this challenge is automatically ret2libc.

The intended solve is as follows:

- use the prompt for the username to leak the stack canary
- enter in the password, stack canary, `rbp` and use a partial overwrite of the return address to redirect execution back to main
- from this loop, leak the addresses of the various functions
- ret2libc
