import { useState } from "react";
import { requestPresignedUrl } from "@/utils/api/evidence";
import { uploadToS3 } from "@/utils/upload";
import { useEvidenceList } from "@/journal/hooks/useEvidenceList";

export function EvidenceUploader({ journalId }: { journalId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const { startPollingForKey, isPolling } = useEvidenceList(journalId);

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setUploadError(null);

    try {
      const { url, key } = await requestPresignedUrl(
        file.name,
        file.type,
        journalId
      );

      await uploadToS3(url, file, { journal_id: journalId });

      startPollingForKey(key);
      setFile(null);
    } catch (err) {
      console.error(err);
      setUploadError("ファイルのアップロードに失敗しました。");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*,application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
      />
      <button onClick={handleUpload} disabled={!file || uploading || isPolling}>
        {uploading ? "アップロード中..." : isPolling ? "登録中..." : "アップロード"}
      </button>
      {uploadError && (
        <span className="error-message" style={{ marginLeft: "8px" }}>
          {uploadError}
        </span>
      )}
    </div>
  );
}
