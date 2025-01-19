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

## Sources

- <https://gist.github.com/jrelo/f5c976fdc602688a0fd40288fde6d886>
