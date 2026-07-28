import useSWR from "swr";
import { createValidatedArrayFetcher } from "@/utils/api/fetchValidated";
import {
  JournalHistoryApiSchema,
  type JournalHistoryApi,
} from "../schemas";

const fetchHistory = createValidatedArrayFetcher(JournalHistoryApiSchema);

export function useJournalHistory(journalId: string) {
  const { data, error, isLoading } = useSWR<JournalHistoryApi[]>(
    `/journal/${journalId}/history/`,
    fetchHistory
  );

  return {
    history: data ?? [],
    isLoading,
    error,
  };
}
