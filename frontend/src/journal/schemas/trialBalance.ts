import { z } from "zod";
import { SideSchema } from "./_shared";
import { AccountType } from "@/management/constants/accountType";

export const TrialBalanceApiSchema = z.object({
  accountId: z.string(),
  accountName: z.string(),
  accountType: z.enum([
    AccountType.ASSET,
    AccountType.LIABILITY,
    AccountType.EQUITY,
    AccountType.REVENUE,
    AccountType.EXPENSE,
  ]),
  balance: z.number(),
  side: SideSchema,
});

export type TrialBalanceApi = z.infer<typeof TrialBalanceApiSchema>;
