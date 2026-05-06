import { z } from "zod";
import { JournalLineInputSchema, JournalLineOutputSchema } from "../schemas/journalLine";

export type JournalLineInput = z.infer<typeof JournalLineInputSchema>;
export type JournalLineOutput = z.infer<typeof JournalLineOutputSchema>;
