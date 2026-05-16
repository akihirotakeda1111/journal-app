import { z } from "zod";
import { JournalWithLinesFormSchema, JournalWithLinesApiSchema } from "../schemas/journalWithLines";

export type JournalWithLinesForm = z.input<typeof JournalWithLinesFormSchema>;
export type JournalWithLinesApi = z.output<typeof JournalWithLinesApiSchema>;
