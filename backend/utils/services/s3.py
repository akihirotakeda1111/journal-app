import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        endpoint = f"https://s3.{settings.AWS_S3_REGION}.amazonaws.com"

        if settings.AWS_ACCESS_KEY_ID:
            self.s3 = boto3.client(
                "s3",
                region_name=settings.AWS_S3_REGION,
                endpoint_url=endpoint,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
        else:
            self.s3 = boto3.client(
                "s3",
                region_name=settings.AWS_S3_REGION,
                endpoint_url=endpoint,
            )

        self.bucket = settings.AWS_S3_UPLOAD_BUCKET
