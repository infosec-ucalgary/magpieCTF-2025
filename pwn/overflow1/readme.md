# overflow1

Author: oblivious_turnip

>Difficulty: easy (easy ret2libc)

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

ret2libc is hypothetically possible in this challenge since the struct that gets
overwritten is on the stack.

Host flag: `magpieCTF{tony_hawk_loves_strcpy}`
Root flag: `magpieCTF{mind_your_buffer_size}`

## Backstory

"We have discovered a hidden terminal claiming to be one of ours, but we've confirmed that it isn't.
We suspect the hacker named *Niko* created it and we have a hunch that it has something to do with
Cristina. Be careful."

## Intended Solve

Abuse the fact that a) the buffer is larger than the size of the string within the struct,
and b) the fact that `strcpy` doesn't care how big the destination buffer is.

The hacker is supposed to overwrite the currently logged in user's username and code to
`cristina33` and `01843101` in order to win the challenge.

## Handouts

- program
