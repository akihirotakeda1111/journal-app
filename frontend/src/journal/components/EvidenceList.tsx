import { useEffect, useState } from "react";
import { fetchEvidenceList } from "@/utils/api/evidence";
import type { EvidenceApi } from "../schemas";
import { fetchDownloadUrl } from "@/utils/api/evidence";
import { download } from "@/utils/download";

export function EvidenceList({ journalId }: { journalId: string }) {
  const [items, setItems] = useState<EvidenceApi[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEvidenceList(journalId)
      .then(setItems)
      .finally(() => setLoading(false));
  }, [journalId]);

  const handleDownload = (id: number) => {
    fetchDownloadUrl(id).then(download);
  };

  if (loading) return <div>読み込み中...</div>;

  if (items.length === 0) return null;

  return (
    <div>
      <h3>証憑一覧</h3>
      <ul>
        {items.map((ev) => (
          <li key={ev.id}>
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
          </li>
        ))}
      </ul>
    </div>
  );
}
