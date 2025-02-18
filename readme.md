# Magpies 2025 CTF

All the challenges for the 2025 magpies CTF.

Flag format: `magpieCTF{...}`

The offered categories are:

- cloud (1)
- crypto (6)
- forensics (?)
- misc (0)
- osint (0)
- pwn (6)
- rev (?)
- web (?)

## Subfolder Structure

Here is the challenge folder structure:

```sh
./
    - cloud/
        - readme.md # contains manifest of challenges and other details
        - challenge1/
            - dist/ # contains all challenges (binaries mainly, or scripts)
                    # to be given to the participants
                    # sha1 signatures should be calculated for
                    # comparison
                - binaries...
            - src/    # source code... (if applicable)
                - chal.c
                - Makefile
                - Dockerfile
                - flag.txt # if applicable
                ...
            - solve/  # code to solve the challenge (if applicable)
                ...
            # code to build the challenge... (if applicable)
            - readme.md # file about the challenge (based off of readme.template.md)
        - challenge2/
            ...
        ...
    - pwn/
        ...
    - rev/
        ...
    ...
```

The `readme.md` file in every category (i.e., `pwn/readme.md`) should have:

- a list of all the challenges in the directory
- any required building tools
- any required build instructions
- some resources if any (although this is mainly for you, the author)

There should be a `readme.md` file in every single challenge folder (i.e., `pwn/printf1/readme.md`),
this should be based off of the file `readme.template.md` in the root folder of this repo.

>All readme files for the challenges **should have the flag in them**.

## Building Challenges

For building, each challenge (or subsection) should have a tool, script, and
whatever else required to build the challenge. (If applicable.)

>For ease of use, if you can just have a script to automatically download
>all the tools and packages you need in order to build the challenges.

For challenges that are dockerized (primarily `pwn`, `rev`, binary exploitation challenges), we're using [nsjail](https://github.com/google/nsjail).

Additionally, the binary (if compiled) must be;

1. built inside of the container (`nsjail`)
2. then copied out into `category/challenge/dist/...` i.e., `pwn/printf1/dist/printf1`
3. a sha1 hash of the binary should be included in `dist/` i.e., `pwn/printf1/dist/printf1.sha1.sig`

>Look at the script `pwn` in `pwn/` to see how all the binary exploitation
>challenges are built.
