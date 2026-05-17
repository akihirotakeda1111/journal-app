import type { AccountApi } from "@/management/types/account"
import { Side } from "../constants/side";

export type HistoryLineApi = {
  side: Side;
  amount: number;
  account: AccountApi;
};

export type JournalHistoryApi = {
  id: string;
  recordedDate: string;
  description: string;
  type: string;
  lines: HistoryLineApi[];
};
