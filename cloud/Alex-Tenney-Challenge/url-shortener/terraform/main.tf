provider "aws" {
  region = "us-west-2"  # Adjust the region as needed
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("./id_ed25519.pub")
}

# 1. Create the S3 Flag Bucket (magpie2025-secret)
resource "aws_s3_bucket" "flag_bucket" {
  bucket = "magpie2025-secret-25"
}

resource "aws_s3_bucket_acl" "flag_bucket_acl" {
  bucket = aws_s3_bucket.flag_bucket.id
  acl    = "private"  # Will now work after fixing Object Ownership
}

# Add a file to the S3 bucket
resource "aws_s3_object" "flag_file" {
  bucket = aws_s3_bucket.flag_bucket.bucket  # Reference the bucket resource
  key    = "flag.txt"                    # The key (filename in the bucket)
  source = "../flag.txt"            # Path to the file on your local machine
}

# 2. Create IAM Role with read-only access to the flag and code S3 buckets
resource "aws_iam_role" "read_only_role" {
  name = "read-only-s3-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "s3_read_only_policy" {
  name        = "s3-read-only-policy"
  description = "Read-only access to flag and code S3 buckets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Fix 1: Allow listing **all** S3 buckets (fixes `aws s3 ls`)
      {
        "Effect": "Allow",
        "Action": "s3:ListAllMyBuckets",
        "Resource": "*"
      },
      # Fix 2: Allow listing **and** getting objects from magpie2025-secret
      {
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:ListBucket"],
        "Resource": [
          "arn:aws:s3:::magpie2025-secret-25",
          "arn:aws:s3:::magpie2025-secret-25/*"
        ]
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  policy_arn = aws_iam_policy.s3_read_only_policy.arn
  role       = aws_iam_role.read_only_role.name
}

# 3. Create EC2 Instance
resource "aws_security_group" "allow_tcp_5000" {
  name        = "allow-tcp-5000"
  description = "Allow TCP port 5000"

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 4. EC2 Instance Profile
resource "aws_iam_instance_profile" "ec2_role" {
  name = "ec2-read-only-profile"
  role = aws_iam_role.read_only_role.name
}

# 5. User Data to Unzip and Run Code on EC2 Instance
resource "aws_instance" "my_ec2_with_user_data" {
  ami           = "ami-0fb9d120e603b6bce"  # Replace with an actual AMI ID
  instance_type = "t2.micro"
  key_name = aws_key_pair.deployer.key_name

  provisioner "file" {
    source      = "../src/code-archive.zip"
    destination = "/home/ubuntu/code-archive.zip"

    connection {
      type        = "ssh"
      user        = "ubuntu"  
      private_key = file("./id_ed25519")  # Path to your private key for SSH access
      host        = self.public_ip  # Use the public IP of the instance
    }
  }

  # Upload the script to EC2 (but DO NOT auto-execute it)
  provisioner "file" {
    source      = "./startup.sh"   # Your local startup script
    destination = "/home/ubuntu/startup.sh"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("./id_ed25519")  # Your SSH private key
      host        = self.public_ip
    }
  }

  iam_instance_profile = aws_iam_instance_profile.ec2_role.name

  security_groups = [
    aws_security_group.allow_tcp_5000.name
  ]

  metadata_options {
    http_tokens   = "optional"  # Allow both IMDSv1 and IMDSv2
    http_endpoint = "enabled"   # Enable metadata endpoint (IMDS)
  }

  tags = {
    Name = "Magpie Cloud 1"
  }
}

output "ec2_public_ip" {
  value = aws_instance.my_ec2_with_user_data.public_ip
}
