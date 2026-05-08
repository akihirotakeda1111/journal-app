from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from journal.exceptions.journal_exceptions import BaseDomainError


def custom_domain_exception_handler(exc, context):
    """
    システム全体のエラーをキャッチし、統一されたHTTPレスポンスに変換するハンドラ
    """
    response = exception_handler(exc, context)

    if isinstance(exc, BaseDomainError):
        status_code = status.HTTP_400_BAD_REQUEST

        # 冪等性チェックのエラー
        if exc.code == "JOURNAL_ALREADY_EXISTS":
            status_code = status.HTTP_200_OK

        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": str(exc),
                }
            },
            status=status_code,
        )

    # 想定外のエラー
    return response
