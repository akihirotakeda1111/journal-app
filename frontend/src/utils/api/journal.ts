import { apiClient } from "./client";
import { JournalWithLinesInputSchema, JournalWithLinesOutputSchema } from "../../journal/schemas/journalWithLines";
import type { JournalWithLinesInput, JournalWithLinesOutput } from "../../journal/types/journalWithLines";

export async function createJournal(data: JournalWithLinesInput): Promise<JournalWithLinesInput> {
  const validated = JournalWithLinesInputSchema.parse(data);
  const res = await apiClient.post("/journal/", validated);

  return res.data;
}

export async function reviseJournal(originalId: string, data: JournalWithLinesInput): Promise<JournalWithLinesInput> {
  const validated = JournalWithLinesInputSchema.parse(data);
  const res = await apiClient.post(`/journal/revise/${originalId}/`, validated);

  return res.data;
}

export async function fetchJournal(id: string): Promise<JournalWithLinesOutput> {
  const res = await apiClient.get(`/journal/${id}/`);
  return JournalWithLinesOutputSchema.parse(res.data);
}

export async function fetchJournalList(): Promise<JournalWithLinesOutput[]> {
  const res = await apiClient.get("journal/list/");
  return JournalWithLinesOutputSchema.array().parse(res.data);
}