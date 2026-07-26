import { useState } from "react";
import { requestPresignedUrl, create } from "@/utils/api/evidence";
import { uploadToS3 } from "@/utils/upload";

export function EvidenceUploader({ journalId }: { journalId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      const { url, key } = await requestPresignedUrl(file.name, file.type);

      await uploadToS3(url, file);

      await create({key, journalId});

      alert("アップロード完了");
    } catch (err) {
      console.error(err);
      alert("アップロード失敗");
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
      <button onClick={handleUpload} disabled={!file || uploading}>
        {uploading ? "アップロード中..." : "アップロード"}
      </button>
    </div>
  );
}
