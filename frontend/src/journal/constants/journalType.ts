export const JournalType = {
  NORMAL: "NORMAL",
  CANCEL: "CANCEL",
} as const;

export const JournalTypeLabels = {
  [JournalType.NORMAL]: "通常",
  [JournalType.CANCEL]: "取消",
} as const;

export type JournalType = keyof typeof JournalType;
