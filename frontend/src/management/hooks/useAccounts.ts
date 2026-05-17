import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { AccountApi } from "../types/account";

export function useAccounts() {
  const { data, error, isLoading } = useSWR<AccountApi[]>(
    "/management/account/list/",
    fetcher
  );

  return {
    accounts: data ?? [],
    isLoading,
    error,
  };
}
