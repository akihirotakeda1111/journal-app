import { z } from "zod";
import { TrialBalanceApiSchema } from "../schemas/trialBalance";

export type TrialBalanceApi = z.infer<typeof TrialBalanceApiSchema>;
