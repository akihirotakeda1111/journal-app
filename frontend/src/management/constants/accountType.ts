export const AccountType = {
  ASSET: "ASSET",
  LIABILITY: "LIABILITY",
  EQUITY: "EQUITY",
  REVENUE: "REVENUE",
  EXPENSE: "EXPENSE",
} as const;

export const AccountTypeLabels = {
  [AccountType.ASSET]: "資産",
  [AccountType.LIABILITY]: "負債",
  [AccountType.EQUITY]: "純資産",
  [AccountType.REVENUE]: "収益",
  [AccountType.EXPENSE]: "費用",
} as const;

export type AccountType = keyof typeof AccountType;
