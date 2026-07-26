import { apiClient } from "./api/client";

export async function uploadToS3(url: string, file: File) {
    const res = await apiClient.put(url, file, {
        headers: {
            "Content-Type": file.type,
        },
    });

    return res.data;
}
