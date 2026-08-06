from uuid import uuid4
from .s3 import S3Service


class UploadService(S3Service):
    def generate_presigned_put_url(
        self,
        filename: str,
        content_type: str,
        category: str,
        metadata: dict | None = None,
    ) -> dict:
        ext = filename.split(".")[-1]
        key = f"{category}/{uuid4()}.{ext}"

        params = {
            "Bucket": self.bucket,
            "Key": key,
            "ContentType": content_type,
        }
        if metadata:
            params["Metadata"] = metadata

        url = self.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=300,
        )

        return {
            "url": url,
            "key": key,
        }
