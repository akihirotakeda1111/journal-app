import { z } from "zod";

export const AccountOutputSchema = z.object({
  id: z.string(),
  name: z.string(),
  type: z.string(),
});