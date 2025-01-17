# PWN Challenges

`nsjail` is built overtop `debian:bookworm-slim`, here's the [link](https://packages.debian.org/bookworm/libc-bin) for its `libc`.

There are four *sections* of challenges, with two challenges per section:

- **printf**: exploits using printf
- **overflow**: overflows of various kinds
- **ret2win**: overflows, specifically using ROP chains
- **expert**: really hard challenges, whatever they might be (or if we're even going to offer these)

The *ret2win* challenges are guaranteed to...

- have their exploit use code redirection to some form of `win` function
- an option to ret2libc and get a *root* flag instead of the provided *host* flag that's read by the `win` function

The *overflow* challenges may have a `win` function too, but their scope is far more limited.

## Sources

- <https://gist.github.com/jrelo/f5c976fdc602688a0fd40288fde6d886>
