import { z } from "zod";

export const EvidenceBaseSchema = z.object({
  key: z.string().min(1, "キーは必須です"),
});

export const EvidenceFormSchema = EvidenceBaseSchema.extend({
  journalId: z.string().min(1, "IDは必須です"),
});

export const EvidenceApiSchema = EvidenceBaseSchema.extend({
  id: z.number(),
  uploadedAt: z.string(),
});
