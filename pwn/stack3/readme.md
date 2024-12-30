# stack3

>Difficulty: intermediate

This is similar but quite different to the other stack challenges.
This time there is ASLR and stack canaries and the exploit is *relatively* hidden.

>The reason why this program is vulnerable to a ret2win or ret2libc is because the user input is combined with the format string
>before the formatting by `printf` happens. Therefore, if any user input contains format strings, they will get evaluated
>when all the other *intentional* format characters do as well.
>
>Some hackers might miss this, so it's a good chance to test their logic and ability to figure out what code is doing.

The intended exploit is as follows:

1. realize that the logging function is vulnerable (the user can input format characters into `__input` which get evaluated by `snprintf`)
1. sign in using the username and password from decompilation
1. leak the address of main to calculate the address of `win`
1. leak the stack canary
1. form a small rop chain using the vulnerable `login` function (buffer overflow)
1. ret2win

>Like the other stack challenges, ret2libc is possible and we might want to provide a flag that's worth more.

## Handouts

- program
