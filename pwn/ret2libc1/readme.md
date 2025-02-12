# ret2libc1

Author: oblivious_turnip

>Difficulty: intermediate

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

A simple ret2libc, with ASLR (might change) nor canaries. Simple.

>If ASLR is mistakenly enabled, the challenge is still solvable because you can
>leak the address of `main`, then fix it after you enter in the password.

Flag: `magpieCTF{c0rr8pt_1ns1d3r_c0nn3ct10n}`

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

The intended solve is as follows:

1. Decompile the binary to obtain the correct username and password.
2. Since there's no ASLR nor canaries, immediately execute a ROP chain.
3. ret2libc
