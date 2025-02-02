# PWN Challenges

`nsjail` is built overtop `debian:bookworm-slim`, here's the [link](https://packages.debian.org/bookworm/libc-bin) for its `libc`.

There are four *sections* of challenges, with two challenges per section:

- **printf**: exploits using printf
- **overflow**: overflows of various kinds
- **ret2libc**: exploits, specifically ret2libc
- **expert**: really hard challenges, whatever they might be (or if we're even going to offer these)

The *overflow* challenges are guaranteed to...

- have a user flag, which is given to participants that trigger the `win` function
- have a root flag, which is given to participants that spawn a shell via. ret2libc

>For ret2libc challenges, some of the functions don't appear in the right locations...
>despite the version of libc I'm using for testing being the exact same as the libc
>running in the container.  
>These are the same files, verified by sha1 hashes. These exploits are still possible,
>it's just really weird.

## Building

In a terminal run:

```sh
./pwn reset # cleans up, builds files, then challenges & images in that order
```

- `build [challenges...]` - builds all challenges and docker images
- `rebuild [challenges...]` - an alias of build
- `regenerate [challenges...]` - updates the Makefile, Dockerfile and header files of the challenges
- `clean` - removes all debug binaries and cleans up the docker images
- `libc` - pulls the linker and libc from the docker image
- `reset` - executes clean, regenerate and build, in that order

For building the images, the script expects to have [nsjail](https://github.com/google/nsjail) pre-built on your machine as a Docker image,
and named `nsjailcontainer`.

>Note:  
>The docker compose file is for testing purposes only, do not use it in a production setting.

## Sources

- <https://gist.github.com/jrelo/f5c976fdc602688a0fd40288fde6d886>
