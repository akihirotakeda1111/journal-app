import { apiClient } from "./api/client";

export const fetcher = (url: string) =>
  apiClient.get(url).then((res) => res.data);
