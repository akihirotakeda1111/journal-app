import { z } from "zod";

export const MIN_AMOUNT = 1;
export const MAX_AMOUNT = 999_999_999_999;

export const JournalLineInputSchema = z.object({
  side: z.enum(["DEBIT", "CREDIT"]),
  accountId: z.string().min(1, "勘定科目を選択してください"),
  amount: z.number().int()
    .min(MIN_AMOUNT, `金額は${MIN_AMOUNT}円以上を指定してください`)
    .max(MAX_AMOUNT, `金額は${MAX_AMOUNT}円以下を指定してください`),
});

export const JournalLineOutputSchema = z.object({
  side: z.enum(["DEBIT", "CREDIT"]),
  accountId: z.string(),
  amount: z.number(),
});