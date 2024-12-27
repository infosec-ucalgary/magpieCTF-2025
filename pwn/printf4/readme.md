# printf4

Basically the exact same as `printf3`, but there's no helping
`flag_ptr_ptr` this time. The hacker is supposed to either:

- transform a saved `rbp` into a gadget, or
- create a gadget within `buffer` and use that to alter `flag_ptr`

The intended exploit is as follows:

- something

>Originally, there was no switch statement here and the two cases were
>merged together, the reason why this exists is because there was no
>possible exploit, because you simply couldn't change the flag_ptr
>because %n writes (at most) a short.
>%hn, %hhn are valid while %jn, %ln and %lln are not.
