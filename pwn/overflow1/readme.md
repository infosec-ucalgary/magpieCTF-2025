# overflow1

Author: oblivious_turnip

>Difficulty: easy (easy ret2libc)

- [ ] stack canaries
- [ ] ASLR
- ret2libc? yes

ret2libc is hypothetically possible in this challenge since the struct that gets
overwritten is on the stack.

Host flag: `magpieCTF{tony_hawk_loves_strcpy}`  
Root flag: `magpieCTF{mind_your_buffer_size}`

## Backstory

New email from <cors@nypd.gov>:

The cyberteam has discovered some unauthorized access to the NYPD's infrastructure,
we've matched the inbound IP addresses to *Jake*'s botnet. After your previous
success, we want you to see what you can find on these machines.

Additionally, take whatever you find with a grain of salt.

>Plot: the login password is base64 encoded "innocent",
>there is an *anomalous* username which is a sha1 hash for "edwardcors",
>and the password is base64 encoded "unexonorated".

>Also, there is a file called `suspect.txt` which hints to the fact that the
>the number of suspects should be 3, but is actually 4.

## Intended Solve

There are two exploits, ret2win and ret2libc:

Intended solve for ret2win:

1. Decompile the program (of course) and find the credentials to login & to win.
2. Overflow the `user_t user` struct on the stack to overwrite the username and code.
3. Execute the `win` function and get the flag.

Intended solve for ret2libc:

1. Do steps 1 and 2 of ret2win.
2. Use the fact that this challenge doens't have ASLR, therefore you can just go right into a rop chain
3. Leak the addresses of the imported functions of libc.
4. Find the correct version of libc, calculate its base address.
5. Spawn a shell and get `flag.root.txt`.

## Handouts

- program
