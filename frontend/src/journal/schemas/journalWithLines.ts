import { z } from "zod";
import { JournalInputSchema, JournalOutputSchema } from "./journal";
import { JournalLineInputSchema, JournalLineOutputSchema } from "./journalLine";
import { Side, SideLabels } from "../constants/side";

export const JournalWithLinesInputSchema = JournalInputSchema.extend({
  lines: z.array(JournalLineInputSchema)
    .min(2, `${SideLabels[Side.DEBIT]}と${SideLabels[Side.CREDIT]}にそれぞれ1行以上必要です`),
}).superRefine((data, ctx) => {
  // 貸借一致のリアルタイム検証
  const debitSum = data.lines
    .filter((l) => l.side === Side.DEBIT)
    .reduce((sum, l) => sum + (l.amount || 0), 0);
  const creditSum = data.lines
    .filter((l) => l.side === Side.CREDIT)
    .reduce((sum, l) => sum + (l.amount || 0), 0);

  if (debitSum !== creditSum) {
    ctx.addIssue({
      code: "custom",
      message: `貸借合計が一致していません（${SideLabels[Side.DEBIT]}: ${debitSum} / ${SideLabels[Side.CREDIT]}: ${creditSum}）`,
      path: ["lines"], // lines全体に対するエラーとして扱う
    });
  }
});

export const JournalWithLinesOutputSchema  = JournalOutputSchema.extend({
  lines: z.array(JournalLineOutputSchema),
});