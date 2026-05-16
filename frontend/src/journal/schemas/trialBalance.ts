import { z } from "zod";
import { Side } from "../constants/side";
import { AccountType } from "@/management/constants/accountType";

export const TrialBalanceOutputSchema = z.object({
  accountId: z.string(),
  accountName: z.string(),
  accountType: z.enum([
    AccountType.ASSET,
    AccountType.LIABILITY,
    AccountType.EQUITY,
    AccountType.REVENUE,
    AccountType.EXPENSE,
  ]),
  balance: z.number(),
  side: z.enum([Side.DEBIT, Side.CREDIT]),
});