from .s3 import S3Service


class DownloadService(S3Service):
    def generate_presigned_get_url(self, key: str) -> dict:
        url = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": key,
            },
            ExpiresIn=300,
        )

        return {"url": url}
