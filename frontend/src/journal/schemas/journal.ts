import { z } from "zod";

export const JournalInputSchema = z.object({
  id: z.string().optional(),
  recordedDate: z.string().min(1, "計上日は必須です"),
  description: z.string().optional(),
});

export const JournalOutputSchema = z.object({
  id: z.string(),
  recordedDate: z.string(),
  description: z.string().nullable(),
  type: z.string(),
});