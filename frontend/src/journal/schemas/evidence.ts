import { z } from "zod";

export const EvidenceBaseSchema = z.object({
  key: z.string().min(1, "キーは必須です"),
  journalId: z.string().min(1, "IDは必須です"),
});

export const EvidenceFormSchema = EvidenceBaseSchema;

export const EvidenceApiSchema = EvidenceBaseSchema.extend({
  id: z.number(),
  uploadedAt: z.string(),
});

export type EvidenceForm = z.infer<typeof EvidenceFormSchema>;
export type EvidenceApi = z.infer<typeof EvidenceApiSchema>;
