# stack2

>Difficulty: medium

Backstory:

something.

## Intended Solve

The `win` function has some stack vars which the hacker can't possibly get right, therefore, they
have to jump inside of the function with a valid, but fake `rbp` in order for the flag to be read correctly.

Additionally, there is also a ret2libc. Instead of using `puts` to leak the addresses of functions in
the `got`, they will use `printf`.

## Handouts

- program
