import React from "react";
import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { JournalWithLinesOutput } from "./types/journalWithLines";
import { Side, SideLabels } from "./constants/side";
import { JournalType, JournalTypeLabels } from "./constants/journalType";

interface Props {
    journalId: string;
    onClose: () => void;
}

export const JournalHistoryModal: React.FC<Props> = ({ journalId, onClose }) => {
    const { data: history, error, isLoading } = useSWR<JournalWithLinesOutput[]>(
        `/journal/${journalId}/history/`,
        fetcher
    );

    return (
        <div className="modal-overlay">
            <div className="modal-container">
            
                {/* モーダルヘッダー */}
                <div className="modal-header">
                    <h3 className="modal-title">仕訳の変更履歴</h3>
                    <button onClick={onClose} className="modal-close">✕ 閉じる</button>
                </div>

                {/* モーダルコンテンツ（スクロール可能領域） */}
                <div className="modal-body">
                    {isLoading && <div>履歴を読み込み中...</div>}
                    {error && <div className="error-message">{error.message}</div>}
                    
                    {/* タイムライン形式での描画 */}
                    {history && (
                        <div className="timeline">
                            {history.map((journal, index) => {
                                const isFirst = index === 0;
                                const isLatest = index === history.length - 1;
                                const isCancel = journal.type === JournalType.CANCEL;

                                let badgeClass = "badge badge-blue";
                                let label = isFirst ? "最初の入力" : "修正（黒）";

                                if (isCancel) {
                                    badgeClass = "badge badge-red";
                                    label = `${JournalTypeLabels[JournalType.CANCEL]}（赤）`;
                                }
                                if (isLatest) {
                                    badgeClass = "badge badge-green";
                                    label = "現在の有効な仕訳";
                                }

                                return (
                                    <div key={journal.id} className="timeline-item">
                                        <div className="timeline-marker"></div>
                                    
                                        <div className="timeline-card">
                                            <div className="flex justify-between items-center" style={{ marginBottom: "0.5rem" }}>
                                                <span className={badgeClass}>{label}</span>
                                                <span className="text-xs" style={{ color: "#888", fontFamily: "monospace" }}>
                                                    ID: {journal.id.split("-")[0]}...
                                                </span>
                                            </div>
                                    
                                            <div style={{ fontWeight: "bold", marginBottom: "0.5rem", color: "#ddd" }}>
                                                {journal.recordedDate} - {journal.description || "（摘要なし）"}
                                            </div>
                                    
                                            {/* 明細の簡易表示 */}
                                            {journal.lines.map((l, i) => (
                                                <div key={i} className={`flex justify-between ${l.side === Side.DEBIT ? "line-debit" : "line-credit"}`}>
                                                    <span>
                                                        {l.side === Side.DEBIT ? `(${SideLabels[Side.DEBIT]})` : `(${SideLabels[Side.CREDIT]})`} {l.accountId}
                                                    </span>
                                                    <span>
                                                        {l.amount.toLocaleString()}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};