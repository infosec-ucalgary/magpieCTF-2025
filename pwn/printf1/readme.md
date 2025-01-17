# printf1

>Difficulty: intermediate

The flag is located withtin the global `.data` section of the program, the hacker has to defeat ASLR and have the program copy the contents of `flag_buffer` into `buffer`.

The intended exploit is as follows:

1. leak the return address of `vuln` (which is `main`)
1. use this leak to calculate the address of `flag_buffer`, defeating ASLR
1. input the address of `flag_buffer` into the program, which will copy the contents of `flag_buffer` into `buffer`
1. the flag will be printed out to the screen

## Handouts

- program
