import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { JournalWithLinesFormSchema } from "../schemas";
import type { JournalWithLinesForm } from "../types";
import { createJournal, reviseJournal } from "@/utils/api/journal";
import { useAccounts } from "@/management/hooks/useAccounts";
import { Side, SideLabels } from "../constants/side";
import { AmountRules } from "../constants/amountRules";
import { createJournalDefaultValues } from "../services/defaultValues";
import { calcDebitSum, calcCreditSum } from "../services/calc";

type JournalFormProps = {
  mode: "create" | "revise";
  originalId?: string;
  mutate: () => void;
  onDone: () => void;
};

export function JournalForm({ mode, originalId, mutate, onDone }: JournalFormProps) {
  const {
    register,
    control,
    handleSubmit,
    watch,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<JournalWithLinesForm>({
    resolver: zodResolver(JournalWithLinesFormSchema),
    defaultValues: createJournalDefaultValues(),
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "lines",
  });

  const { accounts } = useAccounts();

  const watchedLines = watch("lines");
  const debitSum = calcDebitSum(watchedLines);
  const creditSum = calcCreditSum(watchedLines);

  const onSubmit = async (data: JournalWithLinesForm) => {
    if (mode === "create") {
      await createJournal(data);
    } else {
      await reviseJournal(originalId!, data);
    }

    mutate();
    reset(createJournalDefaultValues());
    onDone();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="container">
      <h2>仕訳入力</h2>
      
      {/* ヘッダー情報 */}
      <div className="section row">
        <div>
          <label className="label">計上日</label>
          <input type="date" {...register("recordedDate")} className="input" />
          {errors.recordedDate && <p className="error-message">{errors.recordedDate.message}</p>}
        </div>
        <div>
          <label className="label">摘要（全体）</label>
          <input type="text" {...register("description")} className="input" />
        </div>
      </div>

      {/* 明細情報 */}
      <div className="section row">
        <div>
          <h3 className="block-title">{SideLabels[Side.DEBIT]}</h3>
          {fields.map((field, index) => {
            if (field.side !== Side.DEBIT) return null;
            return (
              <div key={field.id}>
                <div className="line-row">
                  <select {...register(`lines.${index}.accountId`)}  className="line-input">
                    {accounts?.map(account => (
                      <option key={account.id} value={account.id}>
                        {account.id} {account.name}
                      </option>
                    ))}
                  </select>
                  <input type="text" {...register(`lines.${index}.amount`)}
                    maxLength={AmountRules.MAX.toString().length} placeholder="金額" className="line-input" />
                  <button type="button" onClick={() => remove(index)} className="btn-remove">✕</button>
                </div>
                {errors.lines?.[index]?.accountId && <p className="error-message">{errors.lines?.[index]?.accountId.message}</p>}
                {errors.lines?.[index]?.amount && <p className="error-message">{errors.lines?.[index]?.amount.message}</p>}
              </div>
            );
          })}
          <button type="button" onClick={() => append({ side: Side.DEBIT, accountId: "", amount: 0 })} className="btn btn-link">
            + {SideLabels[Side.DEBIT]}を追加
          </button>
        </div>

        <div>
          <h3 className="block-title">{SideLabels[Side.CREDIT]}</h3>
          {fields.map((field, index) => {
            if (field.side !== Side.CREDIT) return null;
            return (
              <div key={field.id}>
                <div className="line-row">
                  <select {...register(`lines.${index}.accountId`)}  className="line-input">
                    {accounts?.map(account => (
                      <option key={account.id} value={account.id}>
                        {account.id} {account.name}
                      </option>
                    ))}
                  </select>
                  <input type="text" {...register(`lines.${index}.amount`)}
                    maxLength={AmountRules.MAX.toString().length} placeholder="金額" className="line-input" />
                  <button type="button" onClick={() => remove(index)} className="btn-remove">✕</button>
                </div>
                {errors.lines?.[index]?.accountId && <p className="error-message">{errors.lines?.[index]?.accountId.message}</p>}
                {errors.lines?.[index]?.amount && <p className="error-message">{errors.lines?.[index]?.amount.message}</p>}
              </div>
            );
          })}
          <button type="button" onClick={() => append({ side: Side.CREDIT, accountId: "", amount: 0 })} className="btn btn-link">
            + {SideLabels[Side.CREDIT]}を追加
          </button>
        </div>
      </div>

      {/* フッター情報 */}
      <div>
        <div>
          <div className="label">
            {SideLabels[Side.DEBIT]} {debitSum.toLocaleString()} / {SideLabels[Side.CREDIT]} {creditSum.toLocaleString()}
          </div>
          {errors.lines?.root && (
            <div className="error-message">{errors.lines.root.message}</div>
          )}
        </div>
        
        <button 
          type="submit" 
          disabled={isSubmitting}
          className="btn btn-primary"
        >
          {isSubmitting ? "送信中..." : "仕訳を登録する"}
        </button>
      </div>
    </form>
  );
};