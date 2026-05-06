import { z } from "zod";
import { JournalInputSchema, JournalOutputSchema } from "../schemas/journal";

export type JournalInput = z.infer<typeof JournalInputSchema>;
export type JournalOutput = z.infer<typeof JournalOutputSchema>;