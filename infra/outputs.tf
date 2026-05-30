output "cloudfront_domain" {
  value = aws_cloudfront_distribution.frontend.domain_name
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "django_ec2_public_dns" {
  value = aws_instance.django.public_dns
}
