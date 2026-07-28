import { z } from "zod";
import { SideSchema, AmountApiSchema } from "./_shared";
import { JournalApiSchema } from "./journal";
import { AccountApiSchema } from "@/management/schemas/account";

export const HistoryLineApiSchema = z.object({
  side: SideSchema,
  amount: AmountApiSchema,
  account: AccountApiSchema,
});

export const JournalHistoryApiSchema = JournalApiSchema.extend({
  lines: z.array(HistoryLineApiSchema),
});

export type HistoryLineApi = z.infer<typeof HistoryLineApiSchema>;
export type JournalHistoryApi = z.infer<typeof JournalHistoryApiSchema>;
