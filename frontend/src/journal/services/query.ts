export function buildTrialBalanceQuery(start_date?: string, end_date?: string) {
  const params = new URLSearchParams();
  if (start_date) params.append("start_date", start_date);
  if (end_date) params.append("end_date", end_date);
  return `/journal/trial_balance/?${params.toString()}`;
}
