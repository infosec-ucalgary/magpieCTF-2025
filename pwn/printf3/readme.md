# printf3

The flag is again located in the `.data` section, but this time there is
no helping `memcpy` function. The hacker must alter `flag_ptr` using
`flag_ptr_ptr` by function of `%n` format characters.

The intended exploit is as follows:

1. leak an `rbp`
1. use said leaked `rbp` to calculate the address of `buffer`
1. use `%n` to overwrite `flag_ptr` using `flag_ptr_ptr`
1. call `read_flag()`
1. simply print out the buffer again and get the flag
