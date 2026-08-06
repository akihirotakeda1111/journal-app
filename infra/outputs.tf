output "cloudfront_domain" {
  value = aws_cloudfront_distribution.frontend.domain_name
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.frontend.id
}

output "react_s3_bucket" {
  value = aws_s3_bucket.react.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "django_ec2_public_dns" {
  value = aws_instance.django.public_dns
}

output "django_ec2_instance_id" {
  value = aws_instance.django.id
}

output "github_frontend_deploy_role_arn" {
  value = aws_iam_role.github_frontend_deploy.arn
}

output "github_backend_deploy_role_arn" {
  value = aws_iam_role.github_backend_deploy.arn
}

output "aws_region" {
  value = var.region
}

output "evidence_webhook_lambda_name" {
  value = aws_lambda_function.evidence_webhook.function_name
}

output "uploads_s3_bucket" {
  value = aws_s3_bucket.uploads.bucket
}
