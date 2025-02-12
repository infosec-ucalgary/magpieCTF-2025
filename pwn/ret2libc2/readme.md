# ret2libc2

Author: oblivious_turnip

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

Flag: `magpieCTF{l0gs_c@n_l3@k}`

## Backstory

New email from <cors@nypd.gov>:

Thanks to your previous exploit, we've uncovered that *Jake*'s PC
contained the layout of Cristina's manor! Very damning evidence, now
we need you to break into this next machine to find where *Jake* is
hiding out.

>Plot:
>You're hacking into Jake's PC. The password is "d3c31tfull3@d3r" and there's a file called
>`location.txt` which has the coordinates for London, UK.

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
1. create a ropchain using the buffer overflow in `login` and execute when leaving `vuln`
1. ret2libc

## Handouts

- program
