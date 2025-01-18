# ret2libc1

>Difficulty: intermediate

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

A simple ret2libc, no ASLR nor canaries. Simple.

>If ASLR is mistakenly enabled, the challenge is still solvable because you can
>leak the address of `main`, then fix it after you enter in the password.

## Backstory

"It seems we've located Niko's PC online, it even has an insecure SSH login.
But be careful, I highly doubt Niko would *intentionally* allow this."

## Intended Solve

Because the `buffer` is a fraction of the size compared to what's being read, this challenge is automatically ret2libc.

The intended solve is as follows:

- use the prompt for the username to leak the stack canary
- enter in the password, stack canary, `rbp` and use a partial overwrite of the return address to redirect execution back to main
- from this loop, leak the addresses of the various functions
- ret2libc
