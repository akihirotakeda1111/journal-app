import { z } from "zod";

export const JournalLineInputSchema = z.object({
  side: z.enum(["DEBIT", "CREDIT"]),
  accountId: z.string().min(1, "勘定科目を選択してください"),
  amount: z.number().int().min(1, "金額は1円以上を指定してください"),
});

export const JournalLineOutputSchema = z.object({
  side: z.enum(["DEBIT", "CREDIT"]),
  accountId: z.string(),
  amount: z.number(),
});