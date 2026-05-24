resource "aws_security_group" "ec2" {
    name        = "${var.project}-ec2-sg"
    description = "Allow SSH and HTTP"
    vpc_id      = aws_vpc.main.id

    ingress {
        description = "SSH"
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["${var.ssh_allowed_ip}/32"]
    }

    ingress {
        description = "HTTP"
        from_port   = 8000
        to_port     = 8000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "${var.project}-ec2-sg"
    }
}

resource "aws_security_group" "rds" {
    name        = "${var.project}-rds-sg"
    description = "Allow PostgreSQL from EC2"
    vpc_id      = aws_vpc.main.id

    ingress {
        description     = "PostgreSQL"
        from_port       = 5432
        to_port         = 5432
        protocol        = "tcp"
        security_groups = [aws_security_group.ec2.id]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "${var.project}-rds-sg"
    }
}
