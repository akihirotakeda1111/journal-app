import { apiClient } from "./client";
import {
  JournalWithLinesFormSchema,
  JournalWithLinesApiSchema,
  type JournalWithLinesForm,
  type JournalWithLinesApi,
} from "@/journal/schemas";

export async function createJournal(data: JournalWithLinesForm): Promise<JournalWithLinesApi> {
  const validated = JournalWithLinesFormSchema.parse(data);
  const res = await apiClient.post("/journal/", validated);

  return JournalWithLinesApiSchema.parse(res.data);
}

export async function cancelJournal(originalId: string): Promise<JournalWithLinesApi> {
  const res = await apiClient.post(`/journal/cancel/${originalId}/`);

  return JournalWithLinesApiSchema.parse(res.data);
}

export async function reviseJournal(originalId: string, data: JournalWithLinesForm): Promise<JournalWithLinesApi> {
  const validated = JournalWithLinesFormSchema.parse(data);
  const res = await apiClient.post(`/journal/revise/${originalId}/`, validated);

  return JournalWithLinesApiSchema.parse(res.data);
}

export async function fetchJournal(id: string): Promise<JournalWithLinesApi> {
  const res = await apiClient.get(`/journal/${id}/`);
  return JournalWithLinesApiSchema.parse(res.data);
}

export async function fetchJournalList(): Promise<JournalWithLinesApi[]> {
  const res = await apiClient.get("journal/list/");
  return JournalWithLinesApiSchema.array().parse(res.data);
}
