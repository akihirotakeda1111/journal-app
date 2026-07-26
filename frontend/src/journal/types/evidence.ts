import { z } from "zod";
import { EvidenceFormSchema, EvidenceApiSchema } from "../schemas/evidence";

export type EvidenceForm = z.infer<typeof EvidenceFormSchema>;
export type EvidenceApi = z.infer<typeof EvidenceApiSchema>;