FROM python:3.9-slim
WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        jupyter-notebook \
        openssh-server \
        && apt-get clean && \
        rm -rf /var/lib/apt/lists/*

# Setup SSH
RUN mkdir /run/sshd

# Create users
RUN useradd -m -s /bin/bash ckrypto && \
    useradd -m -s /bin/bash rhash && \
    echo "ckrypto:m4gp13_n0_br3ach_2024!" | chpasswd && \
    echo "rhash:pr0f_h4sh_1933!" | chpasswd

# Setup SSH directories
RUN mkdir -p /home/ckrypto/.ssh /home/rhash/.ssh && \
    chmod 700 /home/ckrypto/.ssh /home/rhash/.ssh

# Setup research environment
RUN mkdir -p /home/rhash/notebooks /home/rhash/.local/share/research_data && \
    mkdir -p /home/rhash/.config/backup_system/.keys

# Copy notebook
COPY notebooks /home/rhash/notebooks

# Generate and configure SSH keys
RUN ssh-keygen -A && \
    ssh-keygen -t ed25519 -f /home/ckrypto/.ssh/id_ed25519 -N "" && \
    cp /home/ckrypto/.ssh/id_ed25519.pub /home/ckrypto/.ssh/authorized_keys && \
    chown -R ckrypto:ckrypto /home/ckrypto/.ssh && \
    chmod 600 /home/ckrypto/.ssh/authorized_keys && \
    mv /home/ckrypto/.ssh/id_ed25519 /home/rhash/.local/share/research_data/.research_backup && \
    chown -R rhash:rhash /home/rhash && \
    chmod 600 /home/rhash/.local/share/research_data/.research_backup

# Setup flag
RUN mkdir -p /home/ckrypto/.private && \
    echo "magpieCTF{cryp70_k3y_4cc3ss_gr4nt3d}" > /home/ckrypto/.private/partnership_agreement && \
    chown -R ckrypto:ckrypto /home/ckrypto/.private && \
    chmod 700 /home/ckrypto/.private

# Change ssh port
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Expose required ports
EXPOSE 8888 2222

# Copy and configure startup script
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN chmod a-w /home/rhash && chmod a-w /home/ckrypto && chmod a-w /home/rhash/notebooks/notebook.ipynb && \
    chmod a-w /home/rhash/notebooks

CMD ["/usr/local/bin/start.sh"]
