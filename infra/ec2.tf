resource "aws_instance" "django" {
    ami = "ami-0c3fd0f5d33134a76"
    instance_type = "t3.small"
    subnet_id = aws_subnet.public.id
    vpc_security_group_ids = [aws_security_group.ec2.id]
    associate_public_ip_address = true
    key_name = aws_key_pair.app_key.key_name
    iam_instance_profile = aws_iam_instance_profile.ec2.name

    user_data = templatefile("${path.module}/user_data.sh", {
        db_host = aws_db_instance.postgres.address
        db_name = var.db_name
        db_user = var.db_user
        db_password = var.db_password
    })

    tags = {
        Name = "${var.project}-django-ec2"
    }
}

resource "aws_eip" "django" {
    instance = aws_instance.django.id
    domain = "vpc"
}

resource "aws_iam_policy" "s3_readonly" {
    name = "${var.project}-s3-readonly-policy"
    description = "Allow EC2 to read specific S3 bucket"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "s3:GetObject",
                    "s3:ListBucket"
                ]
                Resource = [
                    aws_s3_bucket.react.arn,
                    "${aws_s3_bucket.react.arn}/*"
                ]
            }
        ]
    })

    tags = {
        Name = "${var.project}-s3-readonly-iam-policy"
    }
}

resource "aws_iam_role" "ec2" {
    name = "${var.project}-ec2-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                    Service = "ec2.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })

    tags = {
        Name = "${var.project}-ec2-iam-role"
    }
}

resource "aws_iam_role_policy_attachment" "s3_readonly" {
    role = aws_iam_role.ec2.name
    policy_arn = aws_iam_policy.s3_readonly.arn
}

resource "aws_iam_policy" "uploads_s3_policy" {
    name = "${var.project}-uploads-s3-policy"
    description = "Allow EC2 to generate presigned URLs for file uploads"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Action = [
                    "s3:PutObject",
                    "s3:GetObject"
                ]
                Resource = "${aws_s3_bucket.uploads.arn}/*"
            }
        ]
  })
}

resource "aws_iam_role_policy_attachment" "uploads_s3_attach" {
    role = aws_iam_role.ec2.name
    policy_arn = aws_iam_policy.uploads_s3_policy.arn
}

resource "aws_iam_instance_profile" "ec2" {
    name = "${var.project}-ec2-instance-profile"
    role = aws_iam_role.ec2.name
}