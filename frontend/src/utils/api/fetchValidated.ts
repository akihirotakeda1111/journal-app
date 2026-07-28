import { apiClient } from "./client";
import type { z } from "zod";

export function createValidatedFetcher<T extends z.ZodType>(schema: T) {
  return async (url: string): Promise<z.output<T>> => {
    const res = await apiClient.get(url);
    return schema.parse(res.data);
  };
}

export function createValidatedArrayFetcher<T extends z.ZodType>(schema: T) {
  return async (url: string): Promise<z.output<T>[]> => {
    const res = await apiClient.get(url);
    return schema.array().parse(res.data);
  };
}
