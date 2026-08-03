from rest_framework import status


class ApplicationError(Exception):
    """Service層で利用するアプリケーション例外の基底クラス。

    HTTPの概念を持ち込まず、View層（例外ハンドラ）が http_status を参照して
    適切なレスポンスに変換する。
    """

    default_code: str = "APPLICATION_ERROR"
    http_status: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code

    def __str__(self) -> str:
        return self.message


class ApplicationValidationError(ApplicationError):
    """入力値やビジネスルールの検証エラー（400）"""

    default_code = "VALIDATION_ERROR"
    http_status = status.HTTP_400_BAD_REQUEST


class RecordNotFoundError(ApplicationError):
    """対象リソースが存在しない（404）"""

    default_code = "RECORD_NOT_FOUND"
    http_status = status.HTTP_404_NOT_FOUND


class ForbiddenError(ApplicationError):
    """操作権限がない（403）"""

    default_code = "FORBIDDEN"
    http_status = status.HTTP_403_FORBIDDEN


class ConflictError(ApplicationError):
    """リソースの状態競合（409）"""

    default_code = "CONFLICT"
    http_status = status.HTTP_409_CONFLICT
