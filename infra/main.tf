resource "aws_key_pair" "app_key" {
    key_name   = "${var.project}-key"
    public_key = file("~/.ssh/id_rsa.pub")
}