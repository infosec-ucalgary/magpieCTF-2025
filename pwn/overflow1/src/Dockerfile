FROM nsjailcontainer AS base

# setup OS
RUN apt-get update
RUN apt-get install -y gcc make

# setup challenge
RUN groupadd -g 1001 magpie
RUN useradd -u 1001 magpie -g magpie
RUN mkdir /ctf
RUN chmod a-w /ctf
RUN chmod o+x /ctf

# intermediary image
FROM base AS build

# building the challenge in the container
# the `|| true` is for steps that might fail
WORKDIR /ctf
COPY . ./
RUN make clean || true
RUN make
RUN sha1sum /ctf/overflow1 > /ctf/overflow1.sha1.sig

# trimming the image
FROM base AS dist
COPY --from=build /ctf/overflow1 /ctf/overflow1
COPY --from=build /ctf/flag*.txt /ctf/

# final setup
EXPOSE 6201
CMD ["/bin/nsjail", \
    "-Ml", \
    "--hostname", "localhost", \
    "--port", "6201", \
    "--user", "1001", \
    "--group", "1001", \
    "--chroot", "/", \
    "-E", "TERM=xterm", \
    "--cwd", "/ctf", \
    "--", \
    "/ctf/overflow1"]
