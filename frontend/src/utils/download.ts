export async function download(url: string) {
  const a = document.createElement("a");
  a.href = url;
  a.download = "";
  a.click();
}