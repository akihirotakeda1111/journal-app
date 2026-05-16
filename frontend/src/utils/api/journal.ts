import { apiClient } from "./client";
import { JournalWithLinesFormSchema, JournalWithLinesApiSchema } from "../../journal/schemas/journalWithLines";
import type { JournalWithLinesForm, JournalWithLinesApi } from "../../journal/types/journalWithLines";

export async function createJournal(data: JournalWithLinesForm): Promise<JournalWithLinesForm> {
  const validated = JournalWithLinesFormSchema.parse(data);
  const res = await apiClient.post("/journal/", validated);

  return res.data;
}

export async function reviseJournal(originalId: string, data: JournalWithLinesForm): Promise<JournalWithLinesForm> {
  const validated = JournalWithLinesFormSchema.parse(data);
  const res = await apiClient.post(`/journal/revise/${originalId}/`, validated);

  return res.data;
}

export async function fetchJournal(id: string): Promise<JournalWithLinesApi> {
  const res = await apiClient.get(`/journal/${id}/`);
  return JournalWithLinesApiSchema.parse(res.data);
}

export async function fetchJournalList(): Promise<JournalWithLinesApi[]> {
  const res = await apiClient.get("journal/list/");
  return JournalWithLinesApiSchema.array().parse(res.data);
}