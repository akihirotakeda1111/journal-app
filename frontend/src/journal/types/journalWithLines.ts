import { z } from "zod";
import { JournalWithLinesInputSchema, JournalWithLinesOutputSchema } from "../schemas/journalWithLines";

export type JournalWithLinesInput = z.infer<typeof JournalWithLinesInputSchema>;
export type JournalWithLinesOutput = z.infer<typeof JournalWithLinesOutputSchema>;
