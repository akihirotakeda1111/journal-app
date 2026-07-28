import { uuidv7 } from "uuidv7";
import type { JournalWithLinesForm } from "../schemas";
import { Side } from "../constants/side";

export const createJournalDefaultValues = (): JournalWithLinesForm => ({
    id: uuidv7(),
    recordedDate: new Date().toISOString().split("T")[0],
    description: "",
    lines: [
      { side: Side.DEBIT, accountId: "", amount: 0 },
      { side: Side.CREDIT, accountId: "", amount: 0 },
    ],
  });