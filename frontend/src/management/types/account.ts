import { z } from "zod";
import { AccountApiSchema } from "../schemas/account";

export type AccountApi = z.infer<typeof AccountApiSchema>;