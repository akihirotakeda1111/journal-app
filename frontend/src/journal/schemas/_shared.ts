import { z } from "zod";
import { Side } from "../constants/side";
import { AmountRules } from "../constants/amountRules";

export const RecordedDateSchema = z
  .string()
  .min(1, "計上日は必須です")
  .regex(/^\d{4}-\d{2}-\d{2}$/, "YYYY-MM-DDの形式で入力してください");

export const SideSchema = z.enum([Side.DEBIT, Side.CREDIT]);

export const AmountApiSchema = z
  .number()
  .refine((n) => Number.isFinite(n), { message: "有効な金額を入力してください" })
  .min(AmountRules.MIN, `金額は${AmountRules.MIN}円以上を指定してください`)
  .max(AmountRules.MAX, `金額は${AmountRules.MAX}円以下を指定してください`);

export const AmountFormSchema = z.preprocess(
  (v) => {
    if (typeof v === "string") {
      if (/[^0-9]/.test(v) || v.trim() === "") return undefined;

      const n = Number(v);
      return Number.isFinite(n) ? n : undefined;
    }

    if (typeof v === "number") {
      return Number.isFinite(v) ? v : undefined;
    }

    return undefined;
  },
  AmountApiSchema.optional()
);
