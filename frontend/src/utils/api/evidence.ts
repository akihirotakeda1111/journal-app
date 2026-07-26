import { apiClient } from "./client";
import { EvidenceFormSchema, EvidenceApiSchema } from "@/journal/schemas/evidence";
import type { EvidenceForm, EvidenceApi } from "@/journal/types/evidence";

export async function requestPresignedUrl(filename: string, contentType: string) {
  const res = await apiClient.post(`/journal/evidence/upload/`, JSON.stringify({ filename, content_type: contentType, category: "evidence", }));

  return res.data as Promise<{ url: string; key: string }>;
}

export async function fetchDownloadUrl(id: number) {
  const res = await apiClient.get(`journal/evidence/download/${id}/`);
  return res.data.url as string;
}

export async function create(data: EvidenceForm): Promise<EvidenceForm> {
  const validated = EvidenceFormSchema.parse(data);
  const res = await apiClient.post(`/journal/evidence/${validated.journalId}/`, validated);

  return res.data;
}

export async function fetchEvidenceList(journalId: string): Promise<EvidenceApi[]> {
  const res = await apiClient.get(`journal/evidence/list/${journalId}/`);
  return EvidenceApiSchema.array().parse(res.data);
}
