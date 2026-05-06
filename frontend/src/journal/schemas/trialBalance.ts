import { z } from "zod";

export const TrialBalanceOutputSchema = z.object({
  accountId: z.string(),
  accountName: z.string(),
  accountType: z.enum(["ASSET", "LIABILITY", "EQUITY", "REVENUE", "EXPENSE"]),
  balance: z.number(),
  side: z.enum(["DEBIT", "CREDIT"]),
});