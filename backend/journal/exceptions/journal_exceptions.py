class BaseDomainError(Exception):
    """仕訳に関する業務エラーの基底クラス"""

    def __init__(self, message: str, code: str = None):
        super().__init__(message)
        self.code = code

    pass


class JournalNotFoundError(BaseDomainError):
    """Journalが存在しない場合"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal with ID {journal_id} not found.",
            code="JOURNAL_NOT_FOUND",
        )


class InvalidJournalIdError(BaseDomainError):
    """InvalidなJournal IDの場合"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Invalid journal ID format: {journal_id}",
            code="INVALID_JOURNAL_ID",
        )


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


class EvidenceCreateError(BaseDomainError):
    """Evidenceの作成に失敗した場合"""

    def __init__(self, key: str, original_message: str):
        super().__init__(
            message=f"Failed to create evidence with key: {key}. Error: {original_message}",
            code="EVIDENCE_CREATE_FAILED",
        )
