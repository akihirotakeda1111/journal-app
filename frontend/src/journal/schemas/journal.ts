import { z } from "zod";
import { RecordedDateSchema } from "./_shared";

export const JournalBaseSchema = z.object({
  recordedDate: RecordedDateSchema,
  description: z.string().optional(),
});

const JournalServerFieldsSchema = z.object({
  id: z.string(),
  type: z.string(),
});

export const JournalFormSchema = JournalBaseSchema.extend({
  id: z.string().optional(),
});

export const JournalApiSchema = JournalBaseSchema.merge(JournalServerFieldsSchema);

export type JournalForm = z.infer<typeof JournalFormSchema>;
export type JournalApi = z.infer<typeof JournalApiSchema>;
