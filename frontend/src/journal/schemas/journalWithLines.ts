import { z } from "zod";
import { JournalFormSchema, JournalApiSchema } from "./journal";
import { JournalLineFormSchema, JournalLineApiSchema } from "./journalLine";
import { Side, SideLabels } from "../constants/side";

type JournalLineForm = z.input<typeof JournalLineFormSchema>;

export const JournalWithLinesFormSchema = JournalFormSchema.extend({
  lines: z
    .array(JournalLineFormSchema)
    .min(2, `${SideLabels[Side.DEBIT]}と${SideLabels[Side.CREDIT]}にそれぞれ1行以上必要です`),
}).superRefine((data, ctx) => {
  const lines = data.lines as JournalLineForm[];

  lines.forEach((l, i) => {
    if (l.amount === undefined) {
      ctx.addIssue({
        code: "custom",
        message: "金額を入力してください",
        path: ["lines", i, "amount"],
      });
      return;
    }
  });

  const toNum = (v: JournalLineForm["amount"]): number => {
    if (typeof v === "number" && Number.isFinite(v)) return Math.trunc(v);
    const n = Number(v);
    return Number.isFinite(n) ? Math.trunc(n) : 0;
  };

  const debitSum = lines
    .filter((l) => l.side === Side.DEBIT)
    .reduce((sum, l) => sum + toNum(l.amount), 0);

  const creditSum = lines
    .filter((l) => l.side === Side.CREDIT)
    .reduce((sum, l) => sum + toNum(l.amount), 0);

  if (debitSum !== creditSum) {
    ctx.addIssue({
      code: "custom",
      message: `貸借合計が一致していません（${SideLabels[Side.DEBIT]}: ${debitSum} / ${SideLabels[Side.CREDIT]}: ${creditSum}）`,
      path: ["lines"],
    });
  }
});

export const JournalWithLinesApiSchema = JournalApiSchema.extend({
  lines: z.array(JournalLineApiSchema),
});

export type JournalWithLinesForm = z.input<typeof JournalWithLinesFormSchema>;
export type JournalWithLinesApi = z.output<typeof JournalWithLinesApiSchema>;
