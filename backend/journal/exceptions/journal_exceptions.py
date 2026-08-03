from utils.exceptions.application_errors import (
    ApplicationError,
    ApplicationValidationError,
    ConflictError,
    RecordNotFoundError,
)

# 後方互換のため ApplicationError のエイリアスとして維持
BaseDomainError = ApplicationError


class JournalNotFoundError(RecordNotFoundError):
    """Journalが存在しない場合"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal with ID {journal_id} not found.",
            code="JOURNAL_NOT_FOUND",
        )


class InvalidJournalIdError(ApplicationValidationError):
    """InvalidなJournal IDの場合"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Invalid journal ID format: {journal_id}",
            code="INVALID_JOURNAL_ID",
        )


class JournalAlreadyExistsError(ConflictError):
    """冪等性チェックに引っかかった（既に処理済み）場合のドメイン例外"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal {journal_id} is already processed.",
            code="JOURNAL_ALREADY_EXISTS",
        )


class CancelAlreadyExistsError(ConflictError):
    """取消仕訳がすでに存在する"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal {journal_id} is already cancelled.",
            code="CANCEL_ALREADY_EXISTS",
        )


class JournalAlreadyModifiedError(ConflictError):
    """仕訳が既に修正・取消されている"""

    def __init__(self, journal_id: str):
        super().__init__(
            message=f"Journal {journal_id} is already modified or cancelled.",
            code="JOURNAL_ALREADY_MODIFIED",
        )


class InvalidCancelTargetError(ApplicationValidationError):
    """CANCEL の対象が不正"""

    def __init__(self, journal_id: str, reason: str):
        super().__init__(
            message=f"Invalid cancel target {journal_id}: {reason}",
            code="INVALID_CANCEL_TARGET",
        )


class PeriodClosedError(ConflictError):
    """月次締め後のため操作不可"""

    def __init__(self, period: str):
        super().__init__(
            message=f"Period {period} is closed.",
            code="PERIOD_CLOSED",
        )


class EvidenceCreateError(ApplicationValidationError):
    """Evidenceの作成に失敗した場合"""

    def __init__(self, key: str, original_message: str):
        super().__init__(
            message=f"Failed to create evidence with key: {key}. Error: {original_message}",
            code="EVIDENCE_CREATE_FAILED",
        )


class EvidenceNotFoundError(RecordNotFoundError):
    """Evidenceが存在しない場合"""

    def __init__(self, evidence_id):
        super().__init__(
            message=f"Evidence with ID {evidence_id} not found.",
            code="EVIDENCE_NOT_FOUND",
        )
