FROM python:latest

WORKDIR /tmp

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    jupyter-notebook \
    openssh-server \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /run/sshd && \
    useradd -m magpie && echo "magpie:q8tt&#9P5^nCHb212ZD" | chpasswd && \
    useradd -m hawk && echo "hawk:q8xx&#9P5^nCHb212ZD" | chpasswd && \
    mkdir -p /home/magpie/.ssh /home/hawk/.ssh && \
    chmod 700 /home/magpie/.ssh /home/hawk/.ssh

COPY notebooks /home/hawk/notebooks

RUN ssh-keygen -A && \
    ssh-keygen -t ed25519 -f /home/magpie/.ssh/id_ed25519 -N "" && \
    cp /home/magpie/.ssh/id_ed25519.pub /home/magpie/.ssh/authorized_keys && \
    chown -R magpie:magpie /home/magpie/.ssh && chmod 600 /home/magpie/.ssh/authorized_keys && \
    mv /home/magpie/.ssh/id_ed25519 /home/hawk/.ssh/id_ed25519 && \
    chown -R hawk:hawk /home/hawk/.ssh && chmod 600 /home/hawk/.ssh/id_ed25519

RUN mkdir -p /home/magpie/.hidden && \
    echo "magpieCTF{f1nd_my_pr1v4t3_k3y}" > /home/magpie/.hidden/flag && \
    chown -R magpie:magpie /home/magpie/.hidden && \
    chmod 700 /home/magpie

EXPOSE 8888 22

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

CMD ["/usr/local/bin/start.sh"]
