import { z } from "zod";
import { JournalInputSchema, JournalOutputSchema } from "./journal";
import { JournalLineInputSchema, JournalLineOutputSchema } from "./journalLine";

export const JournalWithLinesInputSchema = JournalInputSchema.extend({
  lines: z.array(JournalLineInputSchema).min(2, "借方と貸方にそれぞれ1行以上必要です"),
}).superRefine((data, ctx) => {
  // 貸借一致のリアルタイム検証
  const debitSum = data.lines
    .filter((l) => l.side === "DEBIT")
    .reduce((sum, l) => sum + (l.amount || 0), 0);
  const creditSum = data.lines
    .filter((l) => l.side === "CREDIT")
    .reduce((sum, l) => sum + (l.amount || 0), 0);

  if (debitSum !== creditSum) {
    ctx.addIssue({
      code: "custom",
      message: `貸借合計が一致していません（借方: ${debitSum} / 貸方: ${creditSum}）`,
      path: ["lines"], // lines全体に対するエラーとして扱う
    });
  }
});

export const JournalWithLinesOutputSchema  = JournalOutputSchema.extend({
  lines: z.array(JournalLineOutputSchema),
});