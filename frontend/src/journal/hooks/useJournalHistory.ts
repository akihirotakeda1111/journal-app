import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { JournalHistoryApi } from "../types";

export function useJournalHistory(journalId: string) {
    const { data, error, isLoading } = useSWR<JournalHistoryApi[]>(
        `/journal/${journalId}/history/`,
        fetcher
    );

    return {
        history: data ?? [],
        isLoading,
        error,
    };
}
