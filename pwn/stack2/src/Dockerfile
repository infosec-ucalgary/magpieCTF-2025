FROM ubuntu:20.04

RUN apt-get update && apt-get -y install xinetd

RUN useradd -M ctf

WORKDIR /ctf

COPY xinetd.conf ./
COPY banner_fail ./
COPY flag.txt ./
COPY challenge.sh ./
COPY stack2 ./

RUN chmod +x challenge.sh

CMD ["xinetd", "-d", "-dontfork", "-f", "xinetd.conf"]
