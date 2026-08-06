import { fetchDownloadUrl } from "@/utils/api/evidence";
import { download } from "@/utils/download";
import { useEvidenceList } from "../hooks/useEvidenceList";

export function EvidenceList({ journalId }: { journalId: string }) {
  const {
    evidence,
    isLoading,
    pendingEvidenceId,
    pollTimedOut,
  } = useEvidenceList(journalId);

  const handleDownload = (id: number) => {
    fetchDownloadUrl(id).then(download);
  };

  if (isLoading) return <div>読み込み中...</div>;

  if (evidence.length === 0 && !pollTimedOut) return null;

  return (
    <div>
      <h3>証憑一覧</h3>
      {pollTimedOut && (
        <div className="error-message" style={{ marginBottom: "8px" }}>
          登録処理が完了しませんでした。しばらく待ってから再度ご確認ください。
        </div>
      )}
      <ul>
        {evidence.map((ev) => (
          <li key={ev.id === pendingEvidenceId ? ev.key : ev.id}>
            {ev.id === pendingEvidenceId ? (
              <>
                {ev.key}
                <span style={{ marginLeft: "8px", color: "#666" }}>登録中...</span>
              </>
            ) : (
              <>
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    handleDownload(ev.id);
                  }}
                  style={{ textDecoration: "underline", cursor: "pointer" }}
                >
                  {ev.key}
                </a>
                <span style={{ marginLeft: "8px", color: "#666" }}>
                  {new Date(ev.uploadedAt).toLocaleString()}
                </span>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
