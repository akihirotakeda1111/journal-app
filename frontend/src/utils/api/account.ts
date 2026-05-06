import { apiClient } from "./client";
import { AccountOutputSchema } from "../../management/schemas/account";
import type { AccountOutput } from "../../management/types/account";

export async function fetchAccountList(): Promise<AccountOutput[]> {
  const res = await apiClient.get("/management/account/list/");

  return AccountOutputSchema.array().parse(res.data);
}