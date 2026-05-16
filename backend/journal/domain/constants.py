class AmountRules:
    MIN = 1
    MAX = 999_999_999_999


class JournalLineRules:
    MAX_ROW = 100


class JournalType:
    NORMAL = "NORMAL"
    CANCEL = "CANCEL"

    CHOICES = (
        (NORMAL, "通常"),
        (CANCEL, "取消"),
    )


class Side:
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

    CHOICES = (
        (DEBIT, "借方"),
        (CREDIT, "貸方"),
    )
