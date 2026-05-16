export const Side = {
  DEBIT: "DEBIT",
  CREDIT: "CREDIT",
} as const;

export const SideLabels = {
  [Side.DEBIT]: "借方",
  [Side.CREDIT]: "貸方",
} as const;

export type Side = keyof typeof Side;
