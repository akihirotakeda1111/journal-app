import { z } from "zod";
import { Side } from "../constants/side";
import { AmountRules } from "../constants/amountRules";

export const JournalLineInputSchema = z.object({
  side: z.enum([Side.DEBIT, Side.CREDIT]),
  accountId: z.string().min(1, "勘定科目を選択してください"),
  amount: z.number().int()
    .min(AmountRules.MIN, `金額は${AmountRules.MIN}円以上を指定してください`)
    .max(AmountRules.MAX, `金額は${AmountRules.MAX}円以下を指定してください`),
});

export const JournalLineOutputSchema = z.object({
  side: z.enum([Side.DEBIT, Side.CREDIT]),
  accountId: z.string(),
  amount: z.number(),
});