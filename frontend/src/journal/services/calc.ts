import type { JournalLineForm, TrialBalanceApi } from "../schemas";
import { Side } from "../constants/side";

export const calcDebitSum = (lines: JournalLineForm[]) =>
    lines
    .filter((l) => l.side === Side.DEBIT)
    .reduce((sum, l) => sum + (Number(l.amount) || 0), 0);

export const calcCreditSum = (lines: JournalLineForm[]) =>
    lines
    .filter((l) => l.side === Side.CREDIT)
    .reduce((sum, l) => sum + (Number(l.amount) || 0), 0);

export function calcBalances(balances: TrialBalanceApi[]) {
  return {
    debit: balances
      .filter((b) => b.side === Side.DEBIT)
      .reduce((sum, b) => sum + b.balance, 0),

    credit: balances
      .filter((b) => b.side === Side.CREDIT)
      .reduce((sum, b) => sum + b.balance, 0),
  };
}
