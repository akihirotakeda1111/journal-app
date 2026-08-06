data "archive_file" "evidence_webhook_lambda" {
    type        = "zip"
    source_file = "${path.module}/lambda/lambda_function.py"
    output_path = "${path.module}/lambda/lambda_function.zip"
}

resource "aws_iam_role" "evidence_webhook_lambda" {
    name = "${var.project}-evidence-webhook-lambda-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
                Action = "sts:AssumeRole"
            }
        ]
    })

    tags = {
        Name = "${var.project}-evidence-webhook-lambda-role"
    }
}

resource "aws_iam_role_policy_attachment" "evidence_webhook_lambda_logs" {
    role       = aws_iam_role.evidence_webhook_lambda.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "evidence_webhook" {
    function_name = "${var.project}-evidence-webhook"
    role          = aws_iam_role.evidence_webhook_lambda.arn
    handler       = "lambda_function.lambda_handler"
    runtime       = "python3.12"
    timeout       = 30

    filename         = data.archive_file.evidence_webhook_lambda.output_path
    source_code_hash = data.archive_file.evidence_webhook_lambda.output_base64sha256

    environment {
        variables = {
            DJANGO_WEBHOOK_URL = coalesce(
                var.django_webhook_url,
                "https://api.${var.project}.${var.domain_name}/api/journal/evidence/webhook/"
            )
            WEBHOOK_SECRET = var.webhook_secret
        }
    }

    tags = {
        Name = "${var.project}-evidence-webhook"
    }
}

resource "aws_lambda_permission" "evidence_webhook_s3_invoke" {
    statement_id  = "AllowExecutionFromS3Bucket"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.evidence_webhook.function_name
    principal     = "s3.amazonaws.com"
    source_arn    = aws_s3_bucket.uploads.arn
}

resource "aws_s3_bucket_notification" "uploads_evidence_created" {
    bucket = aws_s3_bucket.uploads.id

    lambda_function {
        lambda_function_arn = aws_lambda_function.evidence_webhook.arn
        events              = ["s3:ObjectCreated:Put"]
        filter_prefix       = "evidence/"
    }

    depends_on = [aws_lambda_permission.evidence_webhook_s3_invoke]
}
