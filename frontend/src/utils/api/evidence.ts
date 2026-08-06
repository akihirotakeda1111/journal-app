import { apiClient } from "./client";
import { EvidenceApiSchema, type EvidenceApi } from "@/journal/schemas";

export async function requestPresignedUrl(
  filename: string,
  contentType: string,
  journalId: string
) {
  const res = await apiClient.post(
    `/journal/evidence/upload/`,
    JSON.stringify({
      filename,
      content_type: contentType,
      category: "evidence",
      journal_id: journalId,
    })
  );

  return res.data as Promise<{ url: string; key: string }>;
}

export async function fetchDownloadUrl(id: number) {
  const res = await apiClient.get(`journal/evidence/download/${id}/`);
  return res.data.url as string;
}

export async function fetchEvidenceList(journalId: string): Promise<EvidenceApi[]> {
  const res = await apiClient.get(`journal/evidence/list/${journalId}/`);
  return EvidenceApiSchema.array().parse(res.data);
}
