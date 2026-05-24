resource "aws_s3_bucket" "react" {
    bucket = "${var.project}-react-s3-bucket"
    tags = {
        Name = "${var.project}-react-s3-bucket"
    }
}

resource "aws_s3_bucket_public_access_block" "react" {
    bucket = aws_s3_bucket.react.id

    block_public_acls = false
    block_public_policy = false
    ignore_public_acls = false
    restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "react" {
    bucket = aws_s3_bucket.react.id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sid  = "PublicReadGetObject"
                Effect = "Allow"
                Principal = "*"
                Action = "s3:GetObject"
                Resource = "${aws_s3_bucket.react.arn}/*"
            }
        ]
    })

    depends_on = [
        aws_s3_bucket_public_access_block.react
    ]
}

resource "aws_s3_bucket_website_configuration" "react" {
    bucket = aws_s3_bucket.react.id

    index_document {
        suffix = "index.html"
    }

    error_document {
        key = "error.html"
    }
}