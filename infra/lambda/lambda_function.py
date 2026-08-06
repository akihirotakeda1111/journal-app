import json
import os
import urllib.error
import urllib.parse
import urllib.request


def _post_webhook(bucket: str, key: str) -> None:
    url = os.environ["DJANGO_WEBHOOK_URL"]
    secret = os.environ["WEBHOOK_SECRET"]
    payload = json.dumps({"bucket": bucket, "key": key}).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {secret}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
        if status >= 500:
            raise RuntimeError(
                f"Django webhook returned {status} for s3://{bucket}/{key}"
            ) from exc
        return

    if status >= 500:
        raise RuntimeError(
            f"Django webhook returned {status} for s3://{bucket}/{key}"
        )


def lambda_handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        _post_webhook(bucket, key)

    return {"statusCode": 200, "body": json.dumps({"message": "ok"})}
