import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { JournalWithLinesApi } from "../types/journalWithLines";

export function useJournalHistory(journalId: string) {
    const { data, error, isLoading } = useSWR<JournalWithLinesApi[]>(
        `/journal/${journalId}/history/`,
        fetcher
    );

    return {
        history: data ?? [],
        isLoading,
        error,
    };
}
