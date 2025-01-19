# expert1

>Difficulty: expert

This is going to be a ropchain using printf.

>Originally, there was no switch statement here and the two cases were
>merged together, the reason why this exists is because there was no
>possible exploit, because you simply couldn't change the flag_ptr
>because %n writes (at most) a short.
>%hn, %hhn are valid while %jn, %ln and %lln are not.
