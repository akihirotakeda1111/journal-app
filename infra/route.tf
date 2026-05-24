resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.main.id
    tags = {
        Name = "${var.project}-igw"
    }
}

resource "aws_eip" "nat_eip" {
    domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
    allocation_id = aws_eip.nat_eip.id
    subnet_id = aws_subnet.public.id

    tags = {
        Name = "${var.project}-nat"
    }
}

resource "aws_route_table" "public" {
    vpc_id = aws_vpc.main.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }
    tags = {
        Name = "${var.project}-public-rt"
    }
}

resource "aws_route_table_association" "public" {
    subnet_id = aws_subnet.public.id
    route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
    vpc_id = aws_vpc.main.id
    route {
        cidr_block     = "0.0.0.0/0"
        nat_gateway_id = aws_nat_gateway.nat.id
    }
    tags = {
        Name = "${var.project}-private-rt"
    }
}

resource "aws_route_table_association" "private_a" {
    subnet_id      = aws_subnet.private_a.id
    route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_c" {
    subnet_id      = aws_subnet.private_c.id
    route_table_id = aws_route_table.private.id
}