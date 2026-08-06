import useSWR from "swr";
import { useCallback, useEffect, useState } from "react";
import { createValidatedArrayFetcher } from "@/utils/api/fetchValidated";
import { EvidenceApiSchema, type EvidenceApi } from "../schemas";

const fetchEvidence = createValidatedArrayFetcher(EvidenceApiSchema);

const POLL_INTERVAL_MS = 2000;
const POLL_TIMEOUT_MS = 30000;
export const PENDING_EVIDENCE_ID = -1;

export function useEvidenceList(journalId: string) {
  const [pollKey, setPollKey] = useState<string | null>(null);
  const [pollStartedAt, setPollStartedAt] = useState<number | null>(null);
  const [pollTimedOut, setPollTimedOut] = useState(false);

  const swrKey = journalId ? `/journal/evidence/list/${journalId}/` : null;

  const { data, error, isLoading, mutate } = useSWR<EvidenceApi[]>(
    swrKey,
    fetchEvidence,
    {
      refreshInterval: pollKey ? POLL_INTERVAL_MS : 0,
    }
  );

  useEffect(() => {
    if (!pollKey || !data) return;

    const found = data.some(
      (item) => item.key === pollKey && item.id !== PENDING_EVIDENCE_ID
    );
    const timedOut =
      pollStartedAt !== null && Date.now() - pollStartedAt >= POLL_TIMEOUT_MS;

    if (found) {
      setPollKey(null);
      setPollStartedAt(null);
      setPollTimedOut(false);
      void mutate();
    } else if (timedOut) {
      setPollKey(null);
      setPollStartedAt(null);
      setPollTimedOut(true);
    }
  }, [data, pollKey, pollStartedAt, mutate]);

  const startPollingForKey = useCallback(
    (key: string) => {
      setPollKey(key);
      setPollStartedAt(Date.now());
      setPollTimedOut(false);
      void mutate(
        (current) => {
          if (current?.some((item) => item.key === key)) {
            return current;
          }

          return [
            ...(current ?? []),
            {
              id: PENDING_EVIDENCE_ID,
              key,
              uploadedAt: new Date().toISOString(),
            },
          ];
        },
        { revalidate: false }
      );
      void mutate();
    },
    [mutate]
  );

  const isPolling = pollKey !== null;

  return {
    evidence: data ?? [],
    isLoading,
    error,
    mutate,
    startPollingForKey,
    isPolling,
    pollTimedOut,
    pendingKey: pollKey,
    pendingEvidenceId: PENDING_EVIDENCE_ID,
  };
}
