FROM nsjailcontainer

# setup OS
RUN apt-get update
RUN apt-get install -y gcc make

# setup challenge
ARG USERNAME=magpie
RUN useradd -m $USERNAME
RUN chmod a-w /home/$USERNAME
RUN chmod o+x /home/$USERNAME

# building the challenge in the container
# the || true is for steps that might fail
WORKDIR /home/$USERNAME
COPY . ./
RUN make clean || true
RUN make
RUN rm Makefile *.c

EXPOSE 6201

CMD ["bin/nsjail", \
    "-Ml", \
    "--hostname", "localhost", \
    "--port", "6201", \
    "--user", "1001", \
    "--group", "1001", \
    "--chroot", "/", \
    "-E", "TERM=xterm", \
    "--cwd", "/home/$USERNAME", \
    "--", \
    "/home/$USERNAME/printf1"]
