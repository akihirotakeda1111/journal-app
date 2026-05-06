class BaseDomainError(Exception):
    """仕訳に関する業務エラーの基底クラス"""

    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code

    pass


class JournalAlreadyExistsError(BaseDomainError):
    """冪等性チェックに引っかかった（既に処理済み）場合のドメイン例外"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal {journal_id} is already processed.",
            code="JOURNAL_ALREADY_EXISTS",
        )

    pass


class CancelAlreadyExistsError(BaseDomainError):
    """取消仕訳がすでに存在する"""

    pass


class InvalidCancelTargetError(BaseDomainError):
    """CANCEL の対象が不正"""

    pass


class PeriodClosedError(BaseDomainError):
    """月次締め後のため操作不可"""

    pass
