import "@/styles/trialBalance.css";
import { useMemo, useState } from "react";
import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { TrialBalanceApi } from "../types";
import { Side, SideLabels } from "../constants/side";
import { buildTrialBalanceQuery } from "../services/query";
import { calcBalances } from "../services/calc";

export const TrialBalance = ({ refreshKey }: { refreshKey: number }) => {
    const [start, setStart] = useState("");
    const [end, setEnd] = useState("");

    const query = useMemo(() => 
        buildTrialBalanceQuery(start, end) + `&refresh=${refreshKey}`, [start, end, refreshKey]);

    const { data: balances, error, isLoading } = useSWR<TrialBalanceApi[]>(query, fetcher);

    const { totalDebit, totalCredit, isBalanced } = useMemo(() => {
        if (!balances) return { totalDebit: 0, totalCredit: 0, isBalanced: true };

        const { debit, credit } = calcBalances(balances);

        return {
            totalDebit: debit,
            totalCredit: credit,
            isBalanced: debit === credit,
        };
    }, [balances]);

    return (
        <div className="tb-container">
            <div className="tb-header">
                <h2>残高試算表</h2>

                <div className="tb-filter">
                    <label>
                        開始日:
                        <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
                    </label>
                    <label>
                        終了日:
                        <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
                    </label>
                </div>
            </div>

            {isLoading && <div className="tb-loading">集計中...</div>}
            {error && <div className="tb-error">{error.message}</div>}
            {!balances || balances.length === 0 ? (
                <div className="tb-empty">集計対象のデータがありません。</div>
            ) : (
                <div className="tb-table-wrapper">
                    <table className="tb-table">
                        <thead>
                            <tr>
                                <th>科目コード</th>
                                <th>勘定科目</th>
                                <th className="tb-debit">{SideLabels[Side.DEBIT]}残高</th>
                                <th className="tb-credit">{SideLabels[Side.CREDIT]}残高</th>
                            </tr>
                        </thead>

                        <tbody>
                            {balances.map((row) => (
                                <tr key={row.accountId}>
                                    <td className="tb-code">{row.accountId}</td>
                                    <td>{row.accountName}</td>

                                    <td className="tb-debit">
                                        {row.side === Side.DEBIT ? row.balance.toLocaleString() : ""}
                                    </td>

                                    <td className="tb-credit">
                                        {row.side === Side.CREDIT ? row.balance.toLocaleString() : ""}
                                    </td>
                                </tr>
                            ))}
                        </tbody>

                        <tfoot>
                        <tr>
                            <td colSpan={2} className="tb-total-label">総合計</td>
                            <td className="tb-debit tb-total">{totalDebit.toLocaleString()}</td>
                            <td className="tb-credit tb-total">{totalCredit.toLocaleString()}</td>
                        </tr>
                        </tfoot>
                    </table>
                </div>
            )}

            {!isBalanced && (
                <div className="tb-alert">
                    {SideLabels[Side.DEBIT]}と{SideLabels[Side.CREDIT]}に差額 {Math.abs(totalDebit - totalCredit).toLocaleString()} があります。
                </div>
            )}

            {isBalanced && (balances?.length ?? 0) > 0 && (
                <div className="tb-ok">貸借一致</div>
            )}
        </div>
    );
};
