# ret2libc2

>Difficulty: hard

- [x] stack canaries
- [x] ASLR
- ret2libc? yes

This is a harder ret2libc because:

1. the exploit is somewhat obscured
1. you have to deal with stack canaries
1. you have to deal with ASLR

For intermediate/advanced hackers, this is decently trivial.
But for this will be harder for beginners that aren't used to dealing with
these things.

## Backstory

"Nicely done soldier! However, that last computer, after inspection, was a dud.
We're hoping that this is the real one now, things line up better here now."

## Intended Solve

This is similar but quite different to the other stack challenges.
This time there is ASLR and stack canaries and the exploit is *relatively* hidden.

>The reason why this is intermediate is because the difficulty isn't in how to exploit the program,
>the title should give it away that you're meant to ret2libc. The main difficulty is realizing
>where in the program does the exploit live.

The intended exploit is as follows:

1. realize that the logging function is vulnerable (the user can input format characters into `__input` which get evaluated by `snprintf`)
1. sign in using the username and password from decompilation
1. leak `main`'s return address (and therefore `main`) and the stack canary
1. form a small rop chain using the vulnerable `login` function (buffer overflow)
1. ret2libc

## Handouts

- program
