# printf4

Basically the exact same as `printf3`, but there's no helping
`flag_ptr_ptr` this time. The hacker is supposed to either:

- transform a saved `rbp` into a gadget, or
- create a gadget within `buffer` and use that to alter `flag_ptr`

The intended exploit is as follows:
