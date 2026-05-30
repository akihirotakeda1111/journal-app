resource "aws_s3_bucket" "react" {
    bucket = "${var.project}-react-s3-bucket"
    tags = {
        Name = "${var.project}-react-s3-bucket"
    }
}

resource "aws_s3_bucket_public_access_block" "react" {
    bucket = aws_s3_bucket.react.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "react" {
    bucket = aws_s3_bucket.react.id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Sid  = "AllowCloudFrontServicePrincipal"
                Effect = "Allow"
                Principal = {
                    Service = "cloudfront.amazonaws.com"
                }
                Action = "s3:GetObject"
                Resource = "${aws_s3_bucket.react.arn}/*"
                Condition = {
                    StringEquals = {
                        "AWS:SourceArn" = aws_cloudfront_distribution.frontend.arn
                    }
                }
            }
        ]
    })

    depends_on = [
        aws_s3_bucket_public_access_block.react
    ]
}