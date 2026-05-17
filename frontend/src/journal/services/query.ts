export function buildTrialBalanceQuery(start?: string, end?: string) {
  const params = new URLSearchParams();
  if (start) params.append("start", start);
  if (end) params.append("end", end);
  return `/journal/trial_balance/?${params.toString()}`;
}
