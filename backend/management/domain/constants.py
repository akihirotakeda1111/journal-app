class AccountType:
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

    LABELS = {
        ASSET: "資産",
        LIABILITY: "負債",
        EQUITY: "純資産",
        REVENUE: "収益",
        EXPENSE: "費用",
    }

    CHOICES = (
        (ASSET, LABELS[ASSET]),
        (LIABILITY, LABELS[LIABILITY]),
        (EQUITY, LABELS[EQUITY]),
        (REVENUE, LABELS[REVENUE]),
        (EXPENSE, LABELS[EXPENSE]),
    )
