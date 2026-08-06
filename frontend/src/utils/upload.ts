export async function uploadToS3(
  url: string,
  file: File,
  metadata?: Record<string, string>
) {
  const headers: Record<string, string> = {
    "Content-Type": file.type,
  };

  if (metadata) {
    for (const [key, value] of Object.entries(metadata)) {
      headers[`x-amz-meta-${key}`] = value;
    }
  }

  const response = await fetch(url, {
    method: "PUT",
    body: file,
    headers,
  });

  if (!response.ok) {
    throw new Error(`S3 upload failed: ${response.status}`);
  }
}
