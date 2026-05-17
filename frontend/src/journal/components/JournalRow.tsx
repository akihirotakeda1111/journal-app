import React, { useState } from "react";
import { cancelJournal } from "@/utils/api/journal";
import type { JournalWithLinesApi } from "../types";
import { JournalForm } from "./JournalForm";
import { JournalHistoryModal } from "./JournalHistoryModal";
import { Side } from "../constants/side";

interface Props {
  journal: JournalWithLinesApi;
  onMutate: () => void;
}

export const JournalRow: React.FC<Props> = ({ journal, onMutate }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [isHistoryOpen, setIsHistoryOpen] = useState(false);

    const debitLines = journal.lines.filter((l) => l.side === Side.DEBIT);
    const creditLines = journal.lines.filter((l) => l.side === Side.CREDIT);

    const handleCancel = async () => {
        await cancelJournal(journal.id);
        onMutate()
    };

    return (
        <div key={journal.id} className="row-container">
            {/* ヘッダー */}
            <div className="row-header">
                <div className="row-header-left">
                    <span className="row-header-date">{journal.recordedDate}</span>
                    <span className="row-header-desc">{journal.description || "（摘要なし）"}</span>
                </div>
                <div className="row-header-left">
                    <span className="row-header-id">ID: {journal.id}</span>
                    <button
                        onClick={() => setIsHistoryOpen(true)}
                        className="btn btn-history"
                    >
                        履歴
                    </button>
                    <button
                        onClick={() => setIsEditing(!isEditing)}
                        className={`btn ${isEditing ? "btn-edit-active" : "btn-edit"}`}
                    >
                        {isEditing ? "キャンセル" : "訂正"}
                    </button>
                    <button
                        onClick={handleCancel}
                        className="btn btn-cancel"
                    >
                        取消
                    </button>
                </div>
            </div>

            {/* 明細 */}
            <div className="row-body">
                {/* 借方 (DEBIT) - 左側 */}
                <div className="row-col">
                    <table className="row-table">
                        <tbody>
                            {debitLines.map((line, idx) => (
                            <tr key={idx}>
                                <td className="debit">{line.accountId}</td>
                                <td className="debit">{line.amount.toLocaleString()}</td>
                            </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* 貸方 (CREDIT) - 右側 */}
                <div className="row-col">
                    <table className="row-table">
                        <tbody>
                            {creditLines.map((line, idx) => (
                            <tr key={idx}>
                                <td className="credit">{line.accountId}</td>
                                <td className="credit">{line.amount.toLocaleString()}</td>
                            </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            {isEditing && (
                <div className="edit-area">
                    <h4>
                        修正仕訳データの入力
                    </h4>
                    <JournalForm
                        mode="revise"
                        originalId={journal.id}
                        mutate={onMutate}
                        onDone={() => setIsEditing(false)}
                    />
                </div>
            )}
            {isHistoryOpen && (
                <JournalHistoryModal 
                    journalId={journal.id} 
                    onClose={() => setIsHistoryOpen(false)} 
                />
            )}
        </div>
    );
};