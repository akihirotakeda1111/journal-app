import useSWR from "swr";
import { fetcher } from "@/utils/fetcher";
import type { AccountApi } from "../types/account";

export function useAccounts() {
  const { data, error, isLoading } = useSWR<AccountApi[]>(
    "/management/account/list/",
    fetcher
  );

  const addBlankData = [
    { id: "", name: "（未選択）", type: "" },
    ...(data ?? []),
  ];

  return {
    accounts: addBlankData,
    isLoading,
    error,
  };
}
