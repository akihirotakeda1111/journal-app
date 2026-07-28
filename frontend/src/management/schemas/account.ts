import { z } from "zod";

export const AccountApiSchema = z.object({
  id: z.string(),
  name: z.string(),
  type: z.string(),
});

export type AccountApi = z.infer<typeof AccountApiSchema>;
