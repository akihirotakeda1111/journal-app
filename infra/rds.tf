resource "aws_db_subnet_group" "postgres" {
    name = "${var.project}-postgres-subnet-group"
    subnet_ids = [
        aws_subnet.private_a.id,
        aws_subnet.private_c.id
    ]
    tags = {
        Name = "${var.project}-postgres-subnet-group"
    }
}

resource "aws_db_instance" "postgres" {
    identifier = "${var.project}-postgres-instance"
    engine = "postgres"
    engine_version = "18.3"
    instance_class = "db.t3.micro"
    allocated_storage = 20

    db_name = var.db_name
    username = var.db_user
    password = var.db_password

    publicly_accessible = false
    skip_final_snapshot = true

    db_subnet_group_name = aws_db_subnet_group.postgres.name
    vpc_security_group_ids = [aws_security_group.rds.id]

    tags = {
        Name = "${var.project}-postgres-instance"
    }
}