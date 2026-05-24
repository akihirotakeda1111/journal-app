resource "aws_subnet" "public" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "${var.region}a"
    map_public_ip_on_launch = true
    tags = {
        Name = "${var.project}-public-subnet"
    }
}

resource "aws_subnet" "private_a" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "${var.region}a"
    tags = {
        Name = "${var.project}-private-subnet-a"
    }
}

resource "aws_subnet" "private_c" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.3.0/24"
    availability_zone = "${var.region}c"
    tags = {
        Name = "${var.project}-private-subnet-c"
    }
}