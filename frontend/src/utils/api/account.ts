import { apiClient } from "./client";
import { AccountApiSchema } from "@/management/schemas/account";
import type { AccountApi } from "@/management/types/account";

export async function fetchAccountList(): Promise<AccountApi[]> {
  const res = await apiClient.get("/management/account/list/");

  return AccountApiSchema.array().parse(res.data);
}