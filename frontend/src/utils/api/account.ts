import { apiClient } from "./client";
import { AccountApiSchema, type AccountApi } from "@/management/schemas";

export async function fetchAccountList(): Promise<AccountApi[]> {
  const res = await apiClient.get("/management/account/list/");

  return AccountApiSchema.array().parse(res.data);
}