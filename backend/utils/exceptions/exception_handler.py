import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from utils.exceptions.application_errors import ApplicationError

logger = logging.getLogger(__name__)

GENERIC_ERROR_MESSAGE = "An unexpected error occurred."
GENERIC_ERROR_CODE = "INTERNAL_SERVER_ERROR"

# 冪等性チェックなど、HTTPステータスをクラス定義から上書きする例外コード
STATUS_CODE_OVERRIDES: dict[str, int] = {
    "JOURNAL_ALREADY_EXISTS": status.HTTP_200_OK,
}


def custom_exception_handler(exc, context):
    """DRFの exception_handler を拡張し、ApplicationError を標準JSONに変換する。"""
    if isinstance(exc, ApplicationError):
        status_code = STATUS_CODE_OVERRIDES.get(exc.code, exc.http_status)
        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": str(exc),
                }
            },
            status=status_code,
        )

    response = exception_handler(exc, context)

    if response is not None:
        return response

    logger.exception(
        "Unhandled exception in API view",
        exc_info=exc,
        extra={"view": context.get("view"), "request": context.get("request")},
    )
    return Response(
        {
            "error": {
                "code": GENERIC_ERROR_CODE,
                "message": GENERIC_ERROR_MESSAGE,
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
