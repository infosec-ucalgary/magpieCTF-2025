# ret2libc1

Author: oblivious_turnip

>Difficulty: intermediate

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

A simple ret2libc, with ASLR (might change) nor canaries. Simple.

>If ASLR is mistakenly enabled, the challenge is still solvable because you can
>leak the address of `main`, then fix it after you enter in the password.

Flag: `magpieCTF{ret2libc_is_fun}`

## Backstory

New email from <cors@nypd.gov>:

The cyberteam has located *Jake*'s PC online, it even has an insecure SSH login.
But be careful, I highly doubt *Jake* would intentionally allow this.

Becareful of what you mind find.

>Plot:
>You're hacking into Jake's PC. The password is "inn0c3nc3" and there's a file called
>`ip_range.txt` which hints to the fact that the previous login in `overflow1` and `overflow2`
>was from within the NYPD.
>Also, the last connected IP was from Edward Cors, suggesting something isn't right.

## Intended Solve

Because the `buffer` is a fraction of the size compared to what's being read, this challenge is automatically ret2libc.

The intended solve is as follows:

- use the prompt for the username to leak the stack canary
- enter in the password, stack canary, `rbp` and use a partial overwrite of the return address to redirect execution back to main
- from this loop, leak the addresses of the various functions
- ret2libc
