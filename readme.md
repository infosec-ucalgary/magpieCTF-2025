# Magpies 2025 CTF

All the challenges for the 2025 magpies CTF.

Flag format: `magpieCTF{}`

The offered categories are:

- cloud
- crypto
- forensics
- misc
- osint
- pwn
- rev
- web

## Subfolder Structure

Here is the challenge folder structure:

```sh
./
    cloud/
        # code to build
        - readme.md # contains manifest of challenges
        - dist/ # contains all challenges (binaries mainly, or scripts)
                # to be given to the participants
                # sha1 signatures are good to provide
                # (really only for files or compiled binaries), but optional
            binaries...
        - challenge1/
            # challenge files...
            # source code... (if applicable)
            # code to build the challenge...(if applicable)
            # the file that contains the flag
            flag.txt # if applicable
            # file about the challenge (based off of readme.template.md)
            readme.md # contains info about the challenge
        - challenge2/
            ...
        ...
    pwn/
        ...
    rev/
        ...
    ...
```

The `readme.md` file in every category (i.e., `pwn/readme.md`) should have:

- a list of all the challenges in the directory
- any required building tools
- any required build instructions
- some resources if any (although this is mainly for you, the author)

## Building Challenges

For building, each challenge (or subsection) should have a tool, script,
whatever to build the challenge.

>For ease of use, if you can just have a script to automatically download
>all the tools and packages you need in order to build the challenges.

For challenges that are dockerized (primarily `pwn`, `rev`, binary exploitation challenges), we're using [nsjail](https://github.com/google/nsjail).

Additionally, the binary (if compiled) must be built inside of the container, then copied out into `category/dist/name_of_challenge` i.e., `pwn/dist/printf1`.

>Look at the script `pwn` in `pwn/` to see how all the binary exploitation
>challenges are built.
