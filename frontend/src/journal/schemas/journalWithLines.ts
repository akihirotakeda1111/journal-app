import { z } from "zod";
import { JournalFormSchema, JournalApiSchema } from "./journal";
import { JournalLineFormSchema, JournalLineApiSchema } from "./journalLine";
import { Side, SideLabels } from "../constants/side";
import type { JournalLineForm } from "../types/journalLine";


export const JournalWithLinesFormSchema = JournalFormSchema.extend({
    lines: z.array(JournalLineFormSchema)
    .min(2, `${SideLabels[Side.DEBIT]}と${SideLabels[Side.CREDIT]}にそれぞれ1行以上必要です`),
}).superRefine((data, ctx) => {
  const lines = data.lines as unknown as JournalLineForm[];

  // 数値以外はエラー
  lines.forEach((l, i) => {
    if (l.amount === undefined) {
      ctx.addIssue({
        code: "custom",
        message: "金額を入力してください",
        path: ["lines", i, "amount"],
      });
      // 計算できないため処理終了
      return
    }
  });
  
  // 貸借合計値を計算
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

    // 一致しない場合エラー
  if (debitSum !== creditSum) {
    ctx.addIssue({
      code: "custom",
      message: `貸借合計が一致していません（${SideLabels[Side.DEBIT]}: ${debitSum} / ${SideLabels[Side.CREDIT]}: ${creditSum}）`,
      path: ["lines"],
    });
  }
});

export const JournalWithLinesApiSchema  = JournalApiSchema.extend({
  lines: z.array(JournalLineApiSchema),
});