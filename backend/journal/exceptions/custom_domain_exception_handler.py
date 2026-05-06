# core/exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .journal_exceptions import BaseDomainError


def custom_domain_exception_handler(exc, context):
    """
    システム全体のエラーをキャッチし、統一されたHTTPレスポンスに変換するハンドラ
    """
    # まず、DRFの標準ハンドラに処理を任せる（404 Not Foundや401 Unauthorized等を処理）
    response = exception_handler(exc, context)

    # もし飛んできた例外が、私たちが定義した業務エラー（BaseDomainError）だった場合
    if isinstance(exc, BaseDomainError):
        # 業務エラーの種類（code）に応じてステータスコードを決定する
        status_code = status.HTTP_400_BAD_REQUEST  # デフォルトは400

        # 冪等性チェックのエラーなら「処理済み」として 200 OK に書き換える
        if exc.code == "JOURNAL_ALREADY_EXISTS":
            status_code = status.HTTP_200_OK

        # Viewの代わりに、ここで Response オブジェクトを生成して返す
        return Response(
            {
                "error": {
                    "code": exc.code,
                    "message": str(exc),
                    # "context": exc.context # 必要に応じて詳細情報を含める
                }
            },
            status=status_code,
        )

    # 想定外のエラー（システムクラッシュ等）は、そのままDRFに任せる（最終的に500エラーになる）
    return response
