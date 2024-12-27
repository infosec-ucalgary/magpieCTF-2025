# stack2

>Difficulty: easy

Similar to `stack1`, but this time the `user_g` variable is now on the stack. What the hacker is *supposed*
to do is; abuse `strcpy` to overflow the stack and overwrite the return address of `main` to `admin_login`.

The intended exploit is as follows:

1. decompile the program to obtain the username and password
1. change either the username or password, overflowing the struct to overwrite the return address of `main`
1. exit the loop
1. obtain the flag

This program **must not have** PIE nor stack canaries.

>The hacker could possibly ret2libc using this method, we might want to provide a flag worth additional
>points for this.

## Handouts

- program
