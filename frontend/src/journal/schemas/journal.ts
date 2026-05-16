import { z } from "zod";

export const JournalBaseSchema = z.object({
  recordedDate: z.string()
    .min(1, "計上日は必須です")
    .regex(/^\d{4}-\d{2}-\d{2}$/, "YYYY-MM-DDの形式で入力してください"),
  description: z.string().optional(),
});

export const JournalFormSchema = JournalBaseSchema.extend({
  id: z.string().optional(),
});

export const JournalApiSchema = JournalBaseSchema.extend({
  id: z.string(),
  type: z.string(),
});