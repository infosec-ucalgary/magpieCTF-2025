# stack1

>Difficulty: easy

The hacker must abuse `strcpy` to overwrite the `admin` field of the `user_t` struct
in order to bypass the authentication check.

The intended exploit is as follows:

1. decompile the program to obtain the username and password
1. change either the username or password and overflow it into the `admin` field
1. choose option 3) for "admin sign in"
1. obtain the flag

>This is the only exploit possible as the `user_g` variable is located on the heap, away from everything else.

## Handouts

- program
