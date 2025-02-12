# overflow2

Author: oblivious_turnip

>Difficulty: easy (hard ret2libc)

- [ ] stack canaries (to make it easier)
- [x] ASLR (they can leak the return address, they can suffer)
- ret2libc? yes

ret2libc is hypothetically possible because you could hypothetically create a rop-chain
using the vulnerable format string.

Host flag: `magpieCTF{h3@p_0r_b8ff3r_0v3rfL0w}`  
Root flag: `magpieCTF{s3c0nd_3ntr@nc3}`

## Backstory

New email from <cors@nypd.gov>:

After you hacked the first terminal, it appears that you triggered a deadman's
switch, spawning a new "*admin*" NYPD terminal. We need you to break into
this *terminal* and find out what it contains.

Additionally, it is prudent of me to inform you that Jake is a pathological liar.
And everything he says should not be trusted. After all, it is in a criminals's
nature.

>Plot: the login password is base64 encoded "innocent",
>there is an *anomalous* username which is sha1 hash for "edwardcors",
>and the password is base64 encoded "unexonorated".

>Also, there is a file called `vocabulary_profiling.txt` which points to two things:
>a) the hacker wasn't the first one to have entered into the machine and b)
>the name of the file should hint at two different speakers.

## Intended Solve

The exploit isn't quite obvious, what happens is there are two malloc chunks allocated,
one to edit the contents of a user, the other stores a format string for `printf`.

>Note:  
>If these two chunks aren't allocated in the order of buffer -> format string, then the ret2win exploit is impossible! (but not ret2libc.)

Intended solve for ret2win:

1. Realize that the malloc chunks are (memory-wise) allocated side-by-side and are vulnerable to buffer overflows.
2. Overflow the `g_format` buffer to include more format characters than intendended and leak the flag off of the stack.

Intended solve for ret2libc:

1. Perform the same steps as in ret2win.
2. Remember that you can use `%n` to write memory.
3. Use `printf` to write a ropchain on the stack and then ret2libc.

## Handouts

- program
