import { z } from "zod";
import { TrialBalanceOutputSchema } from "../schemas/trialBalance";

export type TrialBalanceOutput = z.infer<typeof TrialBalanceOutputSchema>;
