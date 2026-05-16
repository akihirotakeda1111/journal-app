import { z } from "zod";
import { JournalLineFormSchema, JournalLineApiSchema } from "../schemas/journalLine";

export type JournalLineForm = z.input<typeof JournalLineFormSchema>;
export type JournalLineApi = z.output<typeof JournalLineApiSchema>;
