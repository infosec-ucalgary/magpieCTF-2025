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

The idea here is that in the `edit_user` function, the hacker overflows the `g_edit_buffer`
malloc chunk into the `g_format` chunk to include more format characters than intended,
leaking the flag off of the stack.

## Handouts

- program
