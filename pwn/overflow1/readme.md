# overflow1

>Difficulty: easy

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

## Backstory

"We have discovered a hidden terminal claiming to be one of ours, but we've confirmed that it isn't.
We suspect the hacker named *Niko* created it and we have a hunch that it has something to do with
Cristina. Be careful."

## Intended Solve

Abuse `strcpy` and the massive buffer to overflow the `user_t` struct on the stack,
forging data to properly execute the `win` function.

## Handouts

- program
