import { z } from "zod";
import { SideSchema, AmountFormSchema, AmountApiSchema } from "./_shared";

export const JournalLineBaseSchema = z.object({
  side: SideSchema,
  accountId: z.string().min(1, "勘定科目を選択してください"),
});

export const JournalLineFormSchema = JournalLineBaseSchema.extend({
  amount: AmountFormSchema,
});

export const JournalLineApiSchema = JournalLineBaseSchema.extend({
  amount: AmountApiSchema,
});

export type JournalLineForm = z.input<typeof JournalLineFormSchema>;
export type JournalLineApi = z.output<typeof JournalLineApiSchema>;
