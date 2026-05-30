provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

data "aws_acm_certificate" "frontend" {
  provider = aws.virginia
  domain = "${var.domain_name}"
  statuses = ["ISSUED"]
}

resource "aws_cloudfront_origin_access_control" "oac" {
  name = "frontend-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior = "always"
  signing_protocol = "sigv4"
}

resource "aws_cloudfront_distribution" "frontend" {
  enabled = true
  default_root_object = "index.html"

  aliases = ["${var.project}.${var.domain_name}"]

  origin {
    domain_name = aws_s3_bucket.react.bucket_regional_domain_name
    origin_id = "s3-react"

    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    target_origin_id = "s3-react"
    viewer_protocol_policy = "redirect-to-https"

    allowed_methods = ["GET", "HEAD"]
    cached_methods = ["GET", "HEAD"]

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
  }

  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.frontend.arn
    ssl_support_method = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }
}
