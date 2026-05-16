import { z } from "zod";
import { Side } from "../constants/side";
import { AmountRules } from "../constants/amountRules";


export const JournalLineBaseSchema = z.object({
  side: z.enum([Side.DEBIT, Side.CREDIT]),
  accountId: z.string().min(1, "勘定科目を選択してください"),
});

export const JournalLineFormSchema = JournalLineBaseSchema.extend({
  side: z.enum([Side.DEBIT, Side.CREDIT]),
  accountId: z.string().min(1, "勘定科目を選択してください"),
  amount: z.preprocess((v) => {
    if (typeof v === "string") {
      if (/[^0-9]/.test(v) || v.trim() === "") return undefined;

      const n = Number(v);
      return Number.isFinite(n) ? n : undefined;
    }

    if (typeof v === "number") {
      return Number.isFinite(v) ? v : undefined;
    }

    return undefined;
  }, z.number().min(AmountRules.MIN, `金額は${AmountRules.MIN}円以上を指定してください`)
      .max(AmountRules.MAX, `金額は${AmountRules.MAX}円以下を指定してください`)
      .optional()
  ),
});

export const JournalLineApiSchema = JournalLineBaseSchema.extend({
  amount: z.number()
    .refine(n => Number.isFinite(n), { message: "有効な金額を入力してください" })
    .min(AmountRules.MIN, `金額は${AmountRules.MIN}円以上を指定してください`)
    .max(AmountRules.MAX, `金額は${AmountRules.MAX}円以下を指定してください`),
});