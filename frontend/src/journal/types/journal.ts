import { z } from "zod";
import { JournalFormSchema, JournalApiSchema } from "../schemas/journal";

export type JournalForm = z.infer<typeof JournalFormSchema>;
export type JournalApi = z.infer<typeof JournalApiSchema>;