import useSWR from "swr";
import { createValidatedArrayFetcher } from "@/utils/api/fetchValidated";
import { AccountApiSchema, type AccountApi } from "../schemas";

const fetchAccounts = createValidatedArrayFetcher(AccountApiSchema);

export function useAccounts() {
  const { data, error, isLoading } = useSWR<AccountApi[]>(
    "/management/account/list/",
    fetchAccounts
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
