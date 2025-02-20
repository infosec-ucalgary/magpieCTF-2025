#!/bin/bash
set -ex  # Exit on error, print commands

echo "Starting Cyber URL Checker setup on EC2..."

# Step 1: Remove conflicting/unofficial Docker packages
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    sudo apt-get remove -y $pkg || true
done

# Step 2: Update package lists & install dependencies (NON-INTERACTIVE)
export DEBIAN_FRONTEND=noninteractive  # Prevent interactive prompts
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl gnupg unzip

# Step 3: Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Step 4: Add Docker’s official APT repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 5: Update package lists again and install Docker (NON-INTERACTIVE)
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 6: Enable and start Docker service
sudo systemctl enable docker
sudo systemctl start docker
# sudo usermod -aG docker ubuntu  # Allow 'ubuntu' user to run Docker without sudo

# Step 7: Verify Docker installation
docker --version

# Step 8: Prepare application directory
cd /home/ubuntu
rm -rf app
mkdir app

# Step 9: Extract the Flask app from the ZIP archive
if [ -f "/home/ubuntu/code-archive.zip" ]; then
    unzip /home/ubuntu/code-archive.zip -d /home/ubuntu/app
else
    echo "ERROR: code-archive.zip not found!"
    exit 1
fi

# Step 10: Navigate to the app source directory
cd /home/ubuntu/app/src || exit

# Step 11: Build the Docker container for the Flask app
sudo docker build -t cyber-url-checker .

# Step 12: Stop and remove any existing container
sudo docker stop cyber-url-checker || true
sudo docker rm cyber-url-checker || true

# Step 13: Run the Flask app inside Docker
sudo docker run -d -p 5000:5000 --name cyber-url-checker cyber-url-checker

echo "Yippee! Flask app is now running inside Docker on port 5000!"
