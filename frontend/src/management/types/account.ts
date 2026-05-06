import { z } from "zod";
import { AccountOutputSchema } from "../schemas/account";

export type AccountOutput = z.infer<typeof AccountOutputSchema>;